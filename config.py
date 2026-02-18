"""
SatyaSetu Configuration Module
Central configuration for the application
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB Configuration
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME = "verisense"
USERS_COLLECTION = "users"
NEWS_LOGS_COLLECTION = "news_logs"

# Google Fact Check API
GOOGLE_FACTCHECK_API_KEY = os.getenv("GOOGLE_FACTCHECK_API_KEY", "")
FACTCHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

# Model Configuration
MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", "./models")
DEBERTA_MODEL_NAME = "microsoft/deberta-v3-base"
SBERT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
SPACY_MODEL = "en_core_web_sm"

# Credibility Scoring Weights
WEIGHTS = {
    "deberta_classification": 0.45,
    "semantic_verification": 0.25,
    "fact_check_api": 0.20,
    "bias_sentiment": 0.10
}

# Classification Thresholds
CREDIBILITY_THRESHOLDS = {
    "high": 70,      # Above 70 = Likely Real
    "medium": 40,    # 40-70 = Questionable
    "low": 0         # Below 40 = Likely Fake
}

# Branding
APP_TITLE = "SatyaSetu"
APP_SUBTITLE = "Cybersecurity for News Integrity"

# UI Theme - Cybersecurity SaaS (Dark Navy & Neon Teal)
COLORS = {
    "primary": "#14B8A6",        # Neon Teal (Accent)
    "secondary": "#0D9488",      # Darker Teal
    "accent": "#2DD4BF",         # Bright Mint
    "background": "#0F172A",     # Deep Navy 900
    "background_alt": "#111827", # Navy 950
    "card_bg": "rgba(30, 41, 59, 0.7)", # Glassmorphic Navy
    "text": "#F8FAFC",           # White/Slate 50
    "text_muted": "#94A3B8",     # Slate 400
    "white": "#FFFFFF",
    "success": "#10B981",        # Emerald
    "warning": "#F59E0B",        # Amber
    "danger": "#EF4444",         # Red
    "border": "rgba(148, 163, 184, 0.2)",
    "glow": "0 0 20px rgba(20, 184, 166, 0.4)",
    "gradient": "linear-gradient(135deg, #0F172A 0%, #111827 100%)"
}

# API Timeouts
REQUEST_TIMEOUT = 10  # seconds

# Session Configuration
SESSION_TIMEOUT = 3600  # 1 hour in seconds

# Debug Mode
DEBUG_MODE = os.getenv("DEBUG_MODE", "False") == "True"
