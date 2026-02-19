"""
Session Manager for VeriSense
Manages Streamlit session state for user authentication
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Optional

def init_session_state(cookie_manager=None):
    """Initialize session state variables and handle auto-login from cookies"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if "user" not in st.session_state:
        st.session_state.user = None
    
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    
    if "login_time" not in st.session_state:
        st.session_state.login_time = None
    
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None

    if "show_otp" not in st.session_state:
        st.session_state.show_otp = False
    
    if "pending_user" not in st.session_state:
        st.session_state.pending_user = None

    if "pending_analysis" not in st.session_state:
        st.session_state.pending_analysis = None
        
    if "logout_triggered" not in st.session_state:
        st.session_state.logout_triggered = False

    # Handle Auto-Login from Cookies (if not currently logging out)
    if cookie_manager and not st.session_state.authenticated and not st.session_state.logout_triggered:
        token = cookie_manager.get("satya_session_token")
        if token:
            try:
                from src.integrations.mongodb_handler import MongoDBHandler
                db = MongoDBHandler()
                # Find user by session token or ID stored in token
                user = db.get_user_by_id(token) # Simplified: token is user ID for now
                if user:
                    user_data = {
                        "id": str(user["_id"]),
                        "name": user["name"],
                        "email": user["email"]
                    }
                    # Silent login
                    st.session_state.authenticated = True
                    st.session_state.user = user_data
                    st.session_state.login_time = datetime.now()
                    if st.session_state.page == "landing":
                        st.session_state.page = "dashboard"
                    st.rerun()
            except Exception as e:
                print(f"Auto-login failed: {e}")

def set_page(page_name: str):
    """Set the current page"""
    st.session_state.page = page_name

def login(user_data: dict, cookie_manager=None):
    """Log in a user and set persistent cookie"""
    st.session_state.authenticated = True
    st.session_state.user = user_data
    st.session_state.login_time = datetime.now()
    st.session_state.page = "dashboard"

    st.session_state.logout_triggered = False

    if cookie_manager:
        # Set persistent session cookie (30 days)
        cookie_manager.set("satya_session_token", user_data['id'], key="set_login_cookie")

def logout(cookie_manager=None):
    """Log out the current user and clear cookies"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.login_time = None
    st.session_state.analysis_result = None
    st.session_state.page = "landing"
    
    st.session_state.logout_triggered = True
    
    if cookie_manager:
        cookie_manager.delete("satya_session_token", key="delete_logout_cookie")

def is_authenticated() -> bool:
    """Check if user is authenticated"""
    return st.session_state.get("authenticated", False)

def get_current_user() -> Optional[dict]:
    """Get current logged-in user"""
    return st.session_state.get("user", None)

def require_auth():
    """Redirect to login if not authenticated"""
    if not is_authenticated():
        st.session_state.page = "login"
        st.rerun()

def check_session_timeout(timeout_seconds: int = 3600):
    """
    Check if session has timed out
    Default: 1 hour (3600 seconds)
    """
    if is_authenticated() and st.session_state.login_time:
        elapsed = datetime.now() - st.session_state.login_time
        if elapsed > timedelta(seconds=timeout_seconds):
            logout()
            return True
    return False

def save_analysis_result(result: dict):
    """Save analysis result to session"""
    st.session_state.analysis_result = result

def get_analysis_result() -> Optional[dict]:
    """Get saved analysis result"""
    return st.session_state.get("analysis_result", None)

def clear_analysis_result():
    """Clear saved analysis result"""
    st.session_state.analysis_result = None
