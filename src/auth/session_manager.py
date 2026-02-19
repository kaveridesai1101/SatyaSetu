"""
Session Manager for VeriSense
Manages Streamlit session state for user authentication
"""

import streamlit as st
from datetime import datetime, timedelta
from typing import Optional

def init_session_state():
    """Initialize session state variables"""
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

def set_page(page_name: str):
    """Set the current page"""
    st.session_state.page = page_name

def login(user_data: dict):
    """Log in a user"""
    st.session_state.authenticated = True
    st.session_state.user = user_data
    st.session_state.login_time = datetime.now()
    st.session_state.page = "dashboard"

def logout():
    """Log out the current user"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.login_time = None
    st.session_state.analysis_result = None
    st.session_state.page = "landing"

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
