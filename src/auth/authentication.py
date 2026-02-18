"""
Authentication Module for VeriSense
Handles user registration, login, and password hashing
"""

import bcrypt
import re
import random
import time
from typing import Optional, Tuple
from email_validator import validate_email, EmailNotValidError
from src.integrations.mongodb_handler import MongoDBHandler
from src.utils.mail_handler import MailHandler

class Authentication:
    def __init__(self):
        self.db = MongoDBHandler()
        self.mail = MailHandler()
        self.pending_otps = {} # {email: {"code": "123456", "expires": timestamp}}
    
    def validate_email_format(self, email: str) -> Tuple[bool, str]:
        """Validate email format"""
        try:
            # Validate and normalize email
            valid = validate_email(email)
            return True, valid.email
        except EmailNotValidError as e:
            return False, str(e)
    
    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength
        Requirements: At least 8 characters, 1 uppercase, 1 lowercase, 1 number
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r"[A-Z]", password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r"[a-z]", password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r"\d", password):
            return False, "Password must contain at least one number"
        
        return True, "Password is strong"
    
    def hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(
            password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )
    
    def register_user(self, name: str, email: str, password: str, confirm_password: str) -> Tuple[bool, str]:
        """
        Register a new user
        Returns: (success: bool, message: str)
        """
        # Validate inputs
        if not name or len(name.strip()) < 2:
            return False, "Name must be at least 2 characters long"
        
        # Validate email
        email_valid, email_result = self.validate_email_format(email)
        if not email_valid:
            return False, f"Invalid email: {email_result}"
        
        email = email_result  # Use normalized email
        
        # Check if passwords match
        if password != confirm_password:
            return False, "Passwords do not match"
        
        # Validate password strength
        pwd_valid, pwd_message = self.validate_password_strength(password)
        if not pwd_valid:
            return False, pwd_message
        
        # Check if user already exists
        if self.db.get_user_by_email(email):
            return False, "Email already registered"
        
        # Hash password
        password_hash = self.hash_password(password)
        
        # Create user
        user_data = {
            "name": name.strip(),
            "email": email,
            "password_hash": password_hash
        }
        
        success = self.db.create_user(user_data)
        
        if success:
            return True, "Account created successfully"
        else:
            return False, "Failed to create account. Please try again."
    
    def login_user(self, email: str, password: str) -> Tuple[bool, Optional[dict], str]:
        """
        Authenticate user login and trigger OTP
        Returns: (success: bool, user_data: dict or None, message: str)
        """
        # Validate email format
        email_valid, email_result = self.validate_email_format(email)
        if not email_valid:
            return False, None, "Invalid email format"
        
        email = email_result
        
        # Get user from database
        user = self.db.get_user_by_email(email)
        
        if not user:
            return False, None, "Invalid credentials"
        
        # Verify password
        if not self.verify_password(password, user["password_hash"]):
            return False, None, "Invalid credentials"
        
        # Handle OTP
        otp_code = self.generate_otp(email)
        self.mail.send_otp(email, otp_code)
        
        user_data = {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "otp_required": True
        }
        
        return True, user_data, "OTP sent to your email"

    def generate_otp(self, email: str) -> str:
        """Generate a 6-digit OTP valid for 5 minutes"""
        otp = f"{random.randint(100000, 999999)}"
        self.pending_otps[email] = {
            "code": otp,
            "expires": time.time() + 300 # 5 minutes
        }
        return otp

    def verify_otp(self, email: str, code: str) -> Tuple[bool, str]:
        """Verify the 6-digit code"""
        if email not in self.pending_otps:
            return False, "OTP not found for this email"
        
        data = self.pending_otps[email]
        if time.time() > data["expires"]:
            del self.pending_otps[email]
            return False, "OTP has expired"
        
        if data["code"] != code:
            return False, "Invalid verification code"
        
        # Success
        del self.pending_otps[email]
        return True, "Verification successful"

    def get_pending_otp(self, email: str) -> Optional[str]:
        """Get the pending OTP for UI preview (Sandbox Mode only)"""
        if email in self.pending_otps:
            return self.pending_otps[email]["code"]
        return None
