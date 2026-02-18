"""
MongoDB Integration Handler
Handles database connections and CRUD operations for Users and News Logs
"""

import pymongo
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
import certifi
from datetime import datetime
from bson.objectid import ObjectId
from typing import Optional, List, Dict, Any
import config
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MongoDBHandler:
    _instance = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one database connection"""
        if cls._instance is None:
            cls._instance = super(MongoDBHandler, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize MongoDB connection with JSON fallback"""
        self.use_fallback = False
        try:
            # Check if URI is default/placeholder
            if "localhost" in config.MONGODB_URI or "username" in config.MONGODB_URI:
                logger.warning("MongoDB URI not configured. Using local JSON fallback.")
                self.use_fallback = True
                self._init_fallback()
                return

            self.client = MongoClient(
                config.MONGODB_URI, 
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=3000
            )
            # Verify connection
            self.client.admin.command('ping')
            self.db = self.client[config.DB_NAME]
            self.users = self.db[config.USERS_COLLECTION]
            self.news_logs = self.db[config.NEWS_LOGS_COLLECTION]
            logger.info("Successfully connected to MongoDB Atlas")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            logger.warning("Switching to local JSON fallback mode.")
            self.use_fallback = True
            self._init_fallback()

    def _init_fallback(self):
        """Initialize local JSON storage"""
        import json
        import os
        self.local_db_path = "local_db.json"
        if not os.path.exists(self.local_db_path):
            with open(self.local_db_path, "w") as f:
                json.dump({"users": [], "news_logs": []}, f)

    def _read_local_db(self):
        import json
        try:
            with open(self.local_db_path, "r") as f:
                return json.load(f)
        except:
            return {"users": [], "news_logs": []}

    def _write_local_db(self, data):
        import json
        with open(self.local_db_path, "w") as f:
            json.dump(data, f, indent=4, default=str)

    def get_user_by_email(self, email: str) -> Optional[Dict]:
        if self.use_fallback:
            data = self._read_local_db()
            for user in data["users"]:
                if user["email"] == email:
                    return user
            return None
        if self.users is None: return None
        return self.users.find_one({"email": email})

    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        if self.use_fallback:
            data = self._read_local_db()
            for user in data["users"]:
                if str(user.get("_id")) == str(user_id):
                    return user
            return None
        if self.users is None: return None
        try:
            return self.users.find_one({"_id": ObjectId(user_id)})
        except:
            return None

    def create_user(self, user_data: Dict) -> bool:
        user_data["created_at"] = datetime.utcnow()
        user_data["last_login"] = datetime.utcnow()
        
        if self.use_fallback:
            try:
                data = self._read_local_db()
                # Simulate ObjectId
                user_data["_id"] = str(ObjectId())
                data["users"].append(user_data)
                self._write_local_db(data)
                return True
            except Exception as e:
                logger.error(f"Fallback create error: {e}")
                return False

        if self.users is None: return False
        try:
            self.users.insert_one(user_data)
            return True
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False

    def update_last_login(self, user_id: Any):
        if self.use_fallback:
            return # Skip update for local json for simplicity
            
        if self.users:
            self.users.update_one(
                {"_id": user_id},
                {"$set": {"last_login": datetime.utcnow()}}
            )

    def save_analysis(self, analysis_data: Dict) -> bool:
        if "timestamp" not in analysis_data:
            analysis_data["timestamp"] = datetime.utcnow()
            
        if self.use_fallback:
            try:
                data = self._read_local_db()
                analysis_data["_id"] = str(ObjectId())
                analysis_data["user_id"] = str(analysis_data["user_id"])
                data["news_logs"].append(analysis_data)
                self._write_local_db(data)
                return True
            except Exception as e:
                logger.error(f"Fallback save error: {e}")
                return False

        if self.news_logs is None: return False
        try:
            if "user_id" in analysis_data and isinstance(analysis_data["user_id"], str):
                analysis_data["user_id"] = ObjectId(analysis_data["user_id"])
            self.news_logs.insert_one(analysis_data)
            return True
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            return False

    def get_user_history(self, user_id: str, limit: int = 50) -> List[Dict]:
        if self.use_fallback:
            data = self._read_local_db()
            user_logs = [
                log for log in data["news_logs"] 
                if str(log.get("user_id")) == str(user_id)
            ]
            # Sort by timestamp desc (simple string sort for fallback)
            user_logs.sort(key=lambda x: str(x.get("timestamp")), reverse=True)
            return user_logs[:limit]

        if self.news_logs is None: return []
        try:
            cursor = self.news_logs.find(
                {"user_id": ObjectId(user_id)}
            ).sort("timestamp", pymongo.DESCENDING).limit(limit)
            results = []
            for doc in cursor:
                doc["_id"] = str(doc["_id"])
                doc["user_id"] = str(doc["user_id"])
                results.append(doc)
            return results
        except Exception as e:
            logger.error(f"Error fetching history: {e}")
            return []
