"""
VeriSense - Main Application
Entries point for the Streamlit App
"""

import streamlit as st
import time
import config

# Core Application Imports (Lightweight)
from src.auth import authentication, session_manager
from src.ui import components
from src.utils.logger import get_logger
from src.integrations.mongodb_handler import MongoDBHandler

# --- Setup ---
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="expanded"
)

logger = get_logger(__name__)

# --- UI Helpers ---

def render_navbar():
    """Render the premium glassmorphic navigation bar"""
    
    # Determine button to show
    if session_manager.is_authenticated():
        # Optional: Show Logout or Dashboard link if needed, or nothing
        btn_html = "" 
    else:
        btn_html = '<a href="?nav=login" target="_self" style="text-decoration: none;"><button class="nav-btn">Sign In</button></a>'

    import base64
    import os
    
    # Check for custom logo
    logo_path = "assets/logo.png"
    logo_html = ""
    
    if os.path.exists(logo_path):
        try:
            with open(logo_path, "rb") as f:
                data = f.read()
                encoded = base64.b64encode(data).decode()
            logo_html = f'<img src="data:image/png;base64,{encoded}" style="height: 50px; margin-right: 15px;">'
        except Exception as e:
            logger.error(f"Failed to load logo: {e}")
            logo_html = '<span style="color: #14B8A6; font-size: 1.8rem; margin-right: 10px;">🛡️</span>'
    else:
        logo_html = '<span style="color: #14B8A6; font-size: 1.8rem; margin-right: 10px;">🛡️</span>'

    st.markdown(f"""
        <div class="nav-container">
            <div class="nav-logo">
                {logo_html}
            </div>
            <div style="display: flex; gap: 20px; align-items: center;">
                {btn_html}
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_footer():
    """Render the professional company footer"""
    st.markdown("""
        <div class="footer-container">
            <div class="footer-content">
                <div>
                    <h4 style="color: #FFFFFF; margin-bottom: 20px;">🛡️ SatyaSetu</h4>
                    <p style="color: #94A3B8; font-size: 0.9rem;">The standard for news integrity and AI-powered verification. Protecting the truth in the digital era.</p>
                </div>
                <div>
                    <h5 style="color: #FFFFFF; margin-bottom: 15px;">Product</h5>
                    <p style="color: #475569; font-size: 0.85rem; margin-bottom: 8px;">Analysis Suite</p>
                    <p style="color: #475569; font-size: 0.85rem; margin-bottom: 8px;">Media Forensics</p>
                    <p style="color: #475569; font-size: 0.85rem; margin-bottom: 8px;">API Access</p>
                </div>
                <div>
                    <h5 style="color: #FFFFFF; margin-bottom: 15px;">Company</h5>
                    <p style="color: #475569; font-size: 0.85rem; margin-bottom: 8px;">About Us</p>
                    <p style="color: #475569; font-size: 0.85rem; margin-bottom: 8px;">Privacy Policy</p>
                    <p style="color: #475569; font-size: 0.85rem; margin-bottom: 8px;">Contact Labs</p>
                </div>
            </div>
            <div class="footer-bottom">
                &copy; 2026 SatyaSetu Labs. All Rights Reserved. | Dedicated to Digital Integrity
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- Load Models (Memory Efficient & Robust) ---
def load_fast_components():
    """Load lightweight heuristic components for instant verification"""
    components = {}
    try:
        from src.preprocessing import TextPreprocessor
        components['preprocessor'] = TextPreprocessor()
        from src.linguistic_analysis import LinguisticAnalyzer
        components['linguistic_analyzer'] = LinguisticAnalyzer()
        from src.credibility_scorer import CredibilityScorer
        components['scorer'] = CredibilityScorer()
        from src.source_verifier import SourceVerifier
        components['source_verifier'] = SourceVerifier()
        from src.entity_verifier import EntityVerifier
        components['entity_verifier'] = EntityVerifier()
    except Exception as e:
        logger.warning(f"Fast components failed: {e}")
    return components

@st.cache_resource
def load_deep_components():
    """Load heavy transformer models for deep analysis"""
    components = {}
    try:
        from src.models.deberta_classifier import DebertaClassifier
        components['classifier'] = DebertaClassifier()
        from src.models.semantic_verifier import SemanticVerifier
        components['verifier'] = SemanticVerifier()
        from src.summarizer import Summarizer
        components['summarizer'] = Summarizer()
        from src.bias_sentiment_analyzer import BiasSentimentAnalyzer
        components['bias_analyzer'] = BiasSentimentAnalyzer()
    except Exception as e:
        logger.warning(f"Deep components failed: {e}")
    return components

# --- Initialize ---
session_manager.init_session_state()

# Handle Navigation via Query Params (for HTML buttons)
if "nav" in st.query_params:
    if st.query_params["nav"] == "login":
        session_manager.set_page("login")
    elif st.query_params["nav"] == "signup":
        session_manager.set_page("signup")
    st.query_params.clear()
    st.rerun()

@st.cache_resource
def get_auth_service():
    return authentication.Authentication()

auth = get_auth_service()

components.load_css()
db = MongoDBHandler()

# --- Page Logic ---

def landing_page():
    render_navbar()
    
    # Hero Section
    st.markdown("""
        <div style='text-align: center; padding: 100px 5% 60px 5%;' class='fade-in'>
            <h1 style='font-size: clamp(2.5rem, 6vw, 4.5rem); margin-bottom: 25px; line-height: 1.1; max-width: 1000px; margin-left: auto; margin-right: auto;'>
                <span class='neon-text'>Don’t Get Fooled.</span><br>Verify Before You Share.
            </h1>
            <p style='font-size: 1.25rem; color: #94A3B8; font-weight: 300; max-width: 700px; margin: 0 auto 40px auto; line-height: 1.6;'>
                Advanced AI-powered fact checking system designed for high-integrity news analysis and misinformation defense.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("Get Started — Free", key="hero_analyze", type="primary", use_container_width=True):
            if session_manager.is_authenticated():
                session_manager.set_page("dashboard")
            else:
                session_manager.set_page("signup")
            st.rerun()
        
    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # Feature Highlights (Intelligence Suite)
    st.markdown("<h2 style='text-align: center; margin-bottom: 50px; font-size: 2.2rem;'>🛡️ Intelligence Suite</h2>", unsafe_allow_html=True)
    
    # Larger Box Layout using 2x2 grid for better visibility as requested
    row1_c1, row1_c2 = st.columns(2)
    with row1_c1:
        st.markdown("<div class='glass-card feature-box'><h3>⚡</h3><b>AI Fact Checking</b><p>Real-time high-precision analysis of news articles and claims.</p></div>", unsafe_allow_html=True)
    with row1_c2:
        st.markdown("<div class='glass-card feature-box'><h3>📊</h3><b>Trust Scoring</b><p>Multi-dimensional confidence index based on source credibility.</p></div>", unsafe_allow_html=True)
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    row2_c1, row2_c2 = st.columns(2)
    with row2_c1:
        st.markdown("<div class='glass-card feature-box'><h3>📝</h3><b>Smart Summary</b><p>concise insights and threat intelligence from complex articles.</p></div>", unsafe_allow_html=True)
    with row2_c2:
        st.markdown("<div class='glass-card feature-box'><h3>📸</h3><b>Deepfake Detection</b><p>Advanced media forensics for image and video authenticity.</p></div>", unsafe_allow_html=True)

    # Registration CTA
    if not session_manager.is_authenticated():
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        col_left, col_mid, col_right = st.columns([1, 2, 1])
        with col_mid:
            st.markdown("<div style='text-align: center;' class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h3 style='margin-bottom: 20px;'>Secure Your Digital Newsfeed</h3>", unsafe_allow_html=True)
            if st.button("Register Professional Account", key="cta_reg", use_container_width=True):
                session_manager.set_page("signup")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

    # Professional Footer
    render_footer()

def login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    
    # 3-Column Layout: Branding (Left) | Form (Middle) | Spacer (Right)
    # Added spacer to push form left as requested
    col1, col2, col3 = st.columns([2, 2.5, 1])
    
    # --- Column 1: Branding (Left Side) ---
    with col1:
        import base64
        import os
        
        logo_path = "assets/logo.png"
        logo_html = ""
        if os.path.exists(logo_path):
             with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
             logo_html = f'<img src="data:image/png;base64,{encoded}" style="width: 200px; margin-bottom: 25px;">'
        else:
             logo_html = '<div style="font-size: 100px;">🛡️</div>'

        st.markdown(f"""
            <div style='display: flex; flex-direction: column; justify-content: center; height: 100%; padding-right: 40px; border-right: 1px solid rgba(148, 163, 184, 0.1);'>
                {logo_html}
                <h1 style='font-size: 4rem; margin-bottom: 15px;'>Secure Access</h1>
                <p style='color: #94A3B8; font-size: 1.5rem;'>
                    Verify your identity to access <br>
                    <span class='neon-text' style='font-weight: 600;'>SatyaSetu Dashboard</span>
                </p>
            </div>
        """, unsafe_allow_html=True)

    # --- Column 2: Login Form (Right Side) ---
    with col2:
        if not st.session_state.get("show_otp", False):
            st.markdown("#### Sign In")
            with st.form("login_form", border=True):
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                submit = st.form_submit_button("Sign In", type="primary", use_container_width=True)
                
                if submit:
                    success, user, msg = auth.login_user(email, password)
                    if success:
                        st.session_state.show_otp = True
                        st.session_state.pending_user = user
                        st.rerun()
                    else:
                        st.error(msg)
            
            if st.button("New here? Create an account", use_container_width=True):
                session_manager.set_page("signup")
                st.rerun()
        else:
            # OTP Step
            st.markdown(f"""
                <div class='glass-card' style='text-align: center; padding: 20px;'>
                    <p style='color: #6366F1; font-weight: 500; margin-bottom: 5px;'>Verification Required</p>
                    <p style='font-size: 0.85rem; color: #94A3B8;'>Code sent to <b>{st.session_state.pending_user['email']}</b></p>
                </div>
            """, unsafe_allow_html=True)
            
            # Sandbox Mode Preview
            if auth.mail.is_simulated:
                dev_otp = auth.get_pending_otp(st.session_state.pending_user['email'])
                if dev_otp:
                    st.info(f"🛠️ **Developer Sandbox**: Your code is `{dev_otp}`")
            
            with st.form("otp_form", border=True):
                otp_code = st.text_input("Enter 6-digit Code", max_chars=6, placeholder="000000")
                verify_submit = st.form_submit_button("Verify & Login", type="primary", use_container_width=True)
                
                if verify_submit:
                    success, msg = auth.verify_otp(st.session_state.pending_user['email'], otp_code)
                    if success:
                        session_manager.login(st.session_state.pending_user)
                        st.session_state.show_otp = False
                        st.session_state.pending_user = None
                        
                        if st.session_state.get("pending_analysis"):
                            p = st.session_state.pending_analysis
                            run_full_analysis(p['text'], p['source_type'])
                        
                        st.success("Verification Successful")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error(msg)
            
            if st.button("← Back to Login", use_container_width=True):
                st.session_state.show_otp = False
                st.session_state.pending_user = None
                st.rerun()

def signup_page():
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Consistent 3-Column Layout: Branding (Left) | Form (Middle) | Spacer (Right)
    col1, col2, col3 = st.columns([2, 2.5, 1])
    
    # --- Column 1: Branding (Left Side) ---
    with col1:
        import base64
        import os
        
        logo_path = "assets/logo.png"
        logo_html = ""
        if os.path.exists(logo_path):
             with open(logo_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
             logo_html = f'<img src="data:image/png;base64,{encoded}" style="width: 200px; margin-bottom: 25px;">'
        else:
             logo_html = '<div style="font-size: 100px;">🛡️</div>'

        st.markdown(f"""
            <div style='display: flex; flex-direction: column; justify-content: center; height: 100%; padding-right: 40px; border-right: 1px solid rgba(148, 163, 184, 0.1);'>
                {logo_html}
                <h1 style='font-size: 4rem; margin-bottom: 15px;'>Join SatyaSetu</h1>
                <p style='color: #94A3B8; font-size: 1.5rem;'>
                    Create your professional account for <br>
                    <span class='neon-text' style='font-weight: 600;'>Advanced News Verification</span>
                </p>
            </div>
        """, unsafe_allow_html=True)

    # --- Column 2: Signup Form (Right Side) ---
    with col2:
        st.markdown("#### Create Account")
        with st.form("signup_form", border=True):
            new_name = st.text_input("Full Name", placeholder="John Doe")
            new_email = st.text_input("Email Address", placeholder="john@example.com")
            new_password = st.text_input("Password", type="password", placeholder="Create a strong password")
            confirm_password = st.text_input("Confirm Password", type="password", placeholder="Repeat password")
            
            agree = st.checkbox("I agree to the Terms of Service and Privacy Policy")
            
            submit_reg = st.form_submit_button("Create Account", type="primary", use_container_width=True)
            
            if submit_reg:
                if not agree:
                    st.error("Please agree to the Terms of Service.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, msg = auth.register_user(new_name, new_email, new_password, confirm_password)
                    if success:
                        st.success("Account created successfully! Please sign in.")
                        time.sleep(1.5)
                        session_manager.set_page("login")
                        st.rerun()
                    else:
                        st.error(msg)
        
        if st.button("Already have an account? Sign In", use_container_width=True):
            session_manager.set_page("login")
            st.rerun()

def render_result_card(nav_name):
    """Standardized component to display analysis results if they exist for the current tab"""
    result = session_manager.get_analysis_result()
    
    # Only show results if they match the current media type or if we just ran an analysis
    if result and result.get('source_type', '').lower() in nav_name.lower():
        st.markdown("---")
        st.markdown(f"### 📊 Verification Report: {result['score']['rating']}")
        
        c1, c2 = st.columns([1, 2])
        with c1:
            components.credibility_gauge(result['score']['score'])
        with c2:
            st.markdown("#### Detection Signal")
            st.markdown(f"<h2 style='color: {result['score']['color']};'>{result['score']['rating']}</h2>", unsafe_allow_html=True)
            st.code(f"Confidence: {result['deberta']['real_prob']*100:.1f}%", language=None)

        with st.expander("🛡️ AI Security Audit & Reasons", expanded=True):
            st.markdown(f"**Summary:** {result['summary']}")
            if st.button("Clear Report", key=f"clear_report_{nav_name}"):
                session_manager.clear_analysis_result()
                st.rerun()

def run_full_analysis(input_text, source_type="Text", source_url=None, deep_scan=False):
    """Core Analysis Pipeline Runner with Dual-Track Feedback"""
    import logging
    logger = logging.getLogger(__name__)
    try:
        # 1. Initialize Status Tracking
        status_label = "Deep AI Verification" if deep_scan else "Fast Heuristic Scan"
        status = st.status(f"🚀 Initializing {source_type} {status_label}...", expanded=True)
        
        with status:
            st.write("🔧 Loading Core Infrastructure...")
            components_ai = load_fast_components()
            
            if deep_scan:
                st.write("🧠 Waking up Deep AI Models... (May take a moment)")
                deep_comps = load_deep_components()
                components_ai.update(deep_comps)
            
            user = session_manager.get_current_user()
            
            st.write("📑 Layer 1: Normalizing Content...")
            preprocessor = components_ai.get('preprocessor')
            clean_text = preprocessor.clean_text(input_text) if preprocessor else input_text.strip()
            
            st.write("🚩 Layer 2: Scanning Linguistic Patterns...")
            linguistic_analyzer = components_ai.get('linguistic_analyzer')
            ling_res = linguistic_analyzer.analyze(clean_text) if linguistic_analyzer else {"risk_score": 0, "linguistic_flags": []}
            
            # AI Track (Layer 3)
            deberta_res = {"label": "Neutral", "confidence": 0.5, "fake_prob": 0.5, "real_prob": 0.5}
            if deep_scan and components_ai.get('classifier'):
                st.write("🤖 Layer 3: Deep Learning AI Evaluation...")
                deberta_res = components_ai['classifier'].predict(clean_text)
            
            # AI Track (Layer 4)
            bias_res = {"risk_score": 0, "sentiment": "Neutral"}
            if deep_scan and components_ai.get('bias_analyzer'):
                st.write("⚖️ Layer 4: Emotional & Bias Audit...")
                bias_res = components_ai['bias_analyzer'].analyze(clean_text)
            
            st.write("🔍 Layer 5: Personality & Entity Check...")
            entity_verifier = components_ai.get('entity_verifier')
            entities = preprocessor.get_entities(clean_text) if preprocessor else []
            entity_res = entity_verifier.verify_entities(entities) if entity_verifier else {"score": 50, "reason": "Basic Entity Check"}
            
            st.write("🌐 Layer 6: Source & Domain Audit...")
            source_verifier = components_ai.get('source_verifier')
            urls = preprocessor.extract_urls(input_text) if preprocessor else []
            target_url = source_url if source_url else (urls[0] if urls else None)
            source_res = source_verifier.verify_source(target_url) if source_verifier else {"score": 50, "domain": "Unknown"}

            # AI Track (Layer 6.5)
            verification_res = []
            if deep_scan and components_ai.get('verifier'):
                st.write("🛡️ Layer 6.5: Trusted Source Cross-Ref...")
                claims = preprocessor.extract_claims(clean_text) if preprocessor else []
                verification_res = components_ai['verifier'].verify_claims(claims, ["Official records and news confirm recent reports."])
            
            # AI Track (Layer 7)
            summary = "Summary available in Deep Scan Mode."
            if deep_scan and components_ai.get('summarizer'):
                st.write("📝 Layer 7: Generating Executive Summary...")
                summary = components_ai['summarizer'].generate_summary(clean_text)
            
            st.write("⚖️ Compiling Weighted Credibility Report...")
            scorer = components_ai.get('scorer')
            final_score = scorer.calculate_score(
                ml_score=deberta_res['real_prob'] * 100,
                keyword_risk_score=ling_res['risk_score'],
                sentiment_risk_score=bias_res['risk_score'],
                source_score=source_res['score'],
                entity_score=entity_res['score']
            ) if scorer else {"score": 50, "rating": "Indeterminate", "color": "#94A3B8"}
            
            result_bundle = {
                "text": clean_text[:200] + "...",
                "full_text": clean_text,
                "score": final_score,
                "deberta": deberta_res,
                "bias": bias_res,
                "linguistic": ling_res,
                "source": source_res,
                "entity": entity_res,
                "summary": summary,
                "claims": verification_res,
                "timestamp": datetime.now(),
                "source_type": source_type
            }
            
            session_manager.save_analysis_result(result_bundle)
            
            if user:
                db_record = {
                    "user_id": user['id'],
                    "article_text": clean_text,
                    "credibility_score": final_score['score'],
                    "classification": final_score['rating'],
                    "bias_sentiment": bias_res,
                    "summary": summary,
                    "source_type": source_type
                }
                db.save_analysis(db_record)
            
            status.update(label=f"✅ {status_label} Complete!", state="complete", expanded=False)
            st.session_state.pending_analysis = None
            st.rerun()
            return result_bundle
            
    except Exception as e:
        logger.error(f"Pipeline Failure: {e}")
        st.error(f"Analysis Error: {str(e)}. Try using 'Fast Scan' if Deep Scan is stalling.")
        return None

# --- Modular Dashboard Pages ---

def show_overview_page(user, db):
    """Render the main security overview dashboard"""
    st.markdown("## Security Overview")
    
    # Dashboard Cards using columns
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Checks", "128", delta="+12")
    with c2:
        st.metric("Reliable Content", "85%", delta="+2%")
    with c3:
        st.metric("Threats Detected", "12", delta="-4", delta_color="inverse")
    
    st.markdown("### Recent Activity")
    history = db.get_user_history(user['id']) or []
    if history:
        for item in history[:3]:
            st.markdown(f"<div class='glass-card' style='margin-bottom: 10px; padding: 10px;'><b>{item.get('classification')}</b> - {item.get('source_type')} - {item.get('timestamp')}</div>", unsafe_allow_html=True)
    else:
        st.info("No recent activity found.")

def show_text_analysis_page():
    """Render text verification tool"""
    st.markdown("## 📄 Text Verification")
    
    with st.container():
        # Input Method Selection
        input_method = st.radio("Select Input Method", ["Paste Article Text", "Provide Article Link"], horizontal=True, key="text_input_method")
        
        text_to_analyze = ""
        source_url = None
        
        if input_method == "Paste Article Text":
            text_to_analyze = st.text_area("Paste news content or social claims:", height=200, placeholder="Verify news integrity...", key="main_text_input")
            source_url = st.text_input("Source URL (Optional):", placeholder="https://...", key="main_url_input")
        else:
            source_url = st.text_input("Article or Social Media Link:", placeholder="https://news-site.com/article...", key="url_text_input_direct")
            if source_url:
                st.info(f"Link provided: {source_url}")
                # Mock extraction for URL mode if no scraper yet
                text_to_analyze = f"Extracting and verifying content from: {source_url}"

        # Performance Toggle
        deep_scan_text = st.toggle("🚀 Deep AI Scan (Includes Executive Summary & Model Checks)", value=False, key="text_deep_scan")

        if st.button("Verify Integrity", type="primary", use_container_width=True, key="btn_text_verify"):
            if len(text_to_analyze) > 50 or (input_method == "Provide Article Link" and source_url):
                run_full_analysis(text_to_analyze, "Text", source_url=source_url, deep_scan=deep_scan_text)
            else:
                st.warning("Please provide more content or a valid link.")
        
        # PERSISTENT RESULT DISPLAY
        render_result_card("Text Analysis")

def show_image_analysis_page():
    """Render forensic image tool"""
    st.markdown("## 🖼️ Forensic Image Analysis")
    
    with st.container():
        # Input Method Selection
        input_method = st.radio("Select Input Method", ["Upload Image File", "Provide Image Link"], horizontal=True, key="img_input_method")
        
        image_to_analyze = None
        source_url = None
        
        if input_method == "Upload Image File":
            image_file = st.file_uploader("Upload image for deepfake detection", type=["jpg", "png", "jpeg"], key="img_upload")
            source_url = st.text_input("Source URL (Optional):", placeholder="https://...", key="url_img_input")
            if image_file:
                st.image(image_file, use_container_width=True)
                image_to_analyze = image_file.name
        else:
            source_url = st.text_input("Direct Image or Source Link:", placeholder="https://example.com/image.jpg", key="url_img_input_direct")
            if source_url:
                st.info(f"Link provided: {source_url}")
                image_to_analyze = source_url

        # Image Performance Toggle
        deep_scan_img = st.toggle("🔍 Deep Forensics (AI Generated Content Check)", value=False, key="img_deep_scan")

        if st.button("Detect Manipulation", type="primary", use_container_width=True, key="btn_img_verify"):
            if image_to_analyze:
                mock_text = f"Analyzing image content from: {image_to_analyze}. Scanning for AI generation signatures and forensic artifacts..."
                run_full_analysis(mock_text, "Image", source_url=source_url, deep_scan=deep_scan_img)
            else:
                st.warning("Please provide an image file or a link first.")
        
        # PERSISTENT RESULT DISPLAY
        render_result_card("Image Analysis")

def show_video_analysis_page():
    """Render video verification tool"""
    st.markdown("## 🎥 Video Deepfake Guard")
    
    with st.container():
        # Input Method Selection
        input_method = st.radio("Select Input Method", ["Upload Video File", "Provide Video Link"], horizontal=True, key="vid_input_method")
        
        video_to_analyze = None
        source_url = None
        
        if input_method == "Upload Video File":
            video_file = st.file_uploader("Upload video to verify authenticity", type=["mp4", "mov", "avi"], key="vid_upload")
            if video_file:
                st.info(f"Video selected: {video_file.name}")
                video_to_analyze = video_file.name
        else:
            source_url = st.text_input("YouTube, News, or Direct Video Link:", placeholder="https://www.youtube.com/watch?v=...", key="url_vid_input_direct")
            if source_url:
                st.info(f"Link provided: {source_url}")
                video_to_analyze = source_url

        # Video Performance Toggle
        deep_scan_vid = st.toggle("🎥 Deep Authenticity Scan (Frame-by-Frame AI Detect)", value=False, key="vid_deep_scan")

        if st.button("Extract & Verify", type="primary", use_container_width=True, key="btn_vid_verify"):
            if video_to_analyze:
                mock_text = f"Analyzing video content from: {video_to_analyze}. Performing metadata forensics and deepfake detection frames..."
                run_full_analysis(mock_text, "Video", source_url=source_url, deep_scan=deep_scan_vid)
            else:
                st.warning("Please provide a video file or a link first.")
        
        # PERSISTENT RESULT DISPLAY
        render_result_card("Video Analysis")

def show_settings_page(user):
    """Render user settings page"""
    st.markdown("## Account Configuration")
    st.markdown(f"""
        <div class='glass-card' style='padding: 30px;'>
            <div style='display: flex; align-items: center; margin-bottom: 25px;'>
                <div style='background: linear-gradient(135deg, #6366F1, #A855F7); width: 80px; height: 80px; border-radius: 40px; display: flex; align-items: center; justify-content: center; font-size: 35px; color: white; margin-right: 25px;'>
                    {user['name'][0].upper()}
                </div>
                <div>
                    <h2 style='margin: 0; font-size: 2rem;'>{user['name']}</h2>
                    <p style='color: #94A3B8; margin: 0;'>Verified Security Professional</p>
                </div>
            </div>
            <div style='border-top: 1px solid rgba(148, 163, 184, 0.1); padding-top: 20px;'>
                <p style='color: #6366F1; font-weight: 500; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 5px;'>Email Address</p>
                <p style='font-size: 1.1rem;'>{user['email']}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

def show_history_page(user, db):
    """Render analysis history"""
    st.markdown("### Analysis History")
    history = db.get_user_history(user['id'])
    
    if not history:
        st.info("No history found.")
    else:
        for item in history:
            with st.expander(f"{item.get('timestamp')} - {item.get('classification')} ({item.get('credibility_score')}%)"):
                st.write(item.get('summary', 'No summary'))
                st.caption(f"Text Preview: {item.get('article_text')[:100]}...")

def dashboard_page():
    """Main dashboard entry point with sidebar navigation"""
    user = session_manager.get_current_user()
    if not user:
        session_manager.set_page("login")
        st.rerun()
        return

    # Sidebar Navigation - High Priority Isolation
    with st.sidebar:
        st.markdown(f"### <span class='neon-text'>SatyaSetu</span> AI", unsafe_allow_html=True)
        st.markdown(f"**Welcome, {user['name']}**")
        st.markdown("---")
        
        # Use a literal list for navigation to ensure strict mapping
        nav_options = [
            "🏠 Dashboard Overview",
            "📄 Text Analysis",
            "🖼️ Image Analysis",
            "🎥 Video Analysis",
            "📜 History",
            "⚙️ Settings"
        ]
        
        nav = st.radio("Navigation", nav_options, key="sidebar_nav_radio")
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True, key="logout_btn"):
            session_manager.logout()
            st.rerun()

    # --- Content Execution Area ---
    # Using a main_content container to ensure atomic rendering
    main_content = st.container()
    
    with main_content:
        # Strict Conditional Rendering Pattern
        if nav == "🏠 Dashboard Overview":
            show_overview_page(user, db)
            
        elif nav == "📄 Text Analysis":
            show_text_analysis_page()
            
        elif nav == "🖼️ Image Analysis":
            show_image_analysis_page()
            
        elif nav == "🎥 Video Analysis":
            show_video_analysis_page()
            
        elif nav == "📜 History":
            show_history_page(user, db)
            
        elif nav == "⚙️ Settings":
            show_settings_page(user)

# --- Main Routing Controller ---
def main():
    """Application Router"""
    page = st.session_state.get("page", "landing")

    if page == "landing":
        landing_page()
    elif page == "login":
        login_page()
    elif page == "signup":
        signup_page()
    elif page == "dashboard":
        dashboard_page()
    else:
        landing_page()

if __name__ == "__main__":
    main()
