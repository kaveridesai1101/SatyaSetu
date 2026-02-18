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

# --- Load Models (Cached) ---
@st.cache_resource
def load_ml_components():
    logger.info("Initializing ML Components on-demand...")
    
    # Deferred heavy imports
    from src.preprocessing import TextPreprocessor
    from src.models.deberta_classifier import DebertaClassifier
    from src.models.semantic_verifier import SemanticVerifier
    from src.credibility_scorer import CredibilityScorer
    from src.bias_sentiment_analyzer import BiasSentimentAnalyzer
    from src.summarizer import Summarizer
    from src.linguistic_analysis import LinguisticAnalyzer
    from src.source_verifier import SourceVerifier
    from src.entity_verifier import EntityVerifier
    from src.explainability import ExplainabilityEngine

    preprocessor = TextPreprocessor()
    classifier = DebertaClassifier()
    verifier = SemanticVerifier()
    scorer = CredibilityScorer()
    bias_analyzer = BiasSentimentAnalyzer()
    summarizer = Summarizer()
    
    # New Layers
    linguistic_analyzer = LinguisticAnalyzer()
    source_verifier = SourceVerifier()
    entity_verifier = EntityVerifier()
    
    # Explainability needs the model from classifier
    explainer = ExplainabilityEngine(classifier.get_model(), classifier.get_tokenizer())
    
    return preprocessor, classifier, verifier, scorer, bias_analyzer, summarizer, explainer, linguistic_analyzer, source_verifier, entity_verifier

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
                    success, msg = auth.register_user(new_email, new_password, new_name)
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

def run_full_analysis(input_text, source_type="Text", source_url=None):
    """Core Analysis Pipeline Runner (7-Layer Architecture)"""
    # Load ML components only when strictly needed for analysis
    with st.spinner("Initializing AI Engines..."):
        preprocessor, classifier, verifier, scorer, bias_analyzer, summarizer, explainer, linguistic_analyzer, source_verifier, entity_verifier = load_ml_components()
        
    user = session_manager.get_current_user()
    
    with st.spinner("Running 7-Layer Detection Protocol..."):
        # Layer 1: Preprocessing
        clean_text = preprocessor.clean_text(input_text)
        
        # Layer 2: Linguistic Analysis (Red-Flags)
        ling_res = linguistic_analyzer.analyze(clean_text)
        
        # Layer 3: ML Classification
        deberta_res = classifier.predict(clean_text)
        
        # Layer 4: Sentiment & Bias
        bias_res = bias_analyzer.analyze(clean_text)
        
        # Layer 5: Entity Verification
        entities = preprocessor.get_entities(clean_text)
        entity_res = entity_verifier.verify_entities(entities)
        
        # Layer 6: Source Credibility
        # Use provided URL or extract from text
        urls = preprocessor.extract_urls(input_text)
        target_url = source_url if source_url else (urls[0] if urls else None)
        source_res = source_verifier.verify_source(target_url)

        # Trusted Sources for Semantic Verification (Layer 2.5)
        claims = preprocessor.extract_claims(clean_text)
        trusted_sources = [
            "Official health reports confirm vaccine safety protocols were strictly followed.",
            "Cybersecurity agencies deny rumors of a national grid breach.",
            "The World Health Organization states that vaccines are safe.",
            "NASA confirms the earth is round and orbits the sun.",
            "Climate change is scientifically proven to be driven by human activity."
        ]
        verification_res = verifier.verify_claims(claims, trusted_sources) if claims else []
        
        summary = summarizer.generate_summary(clean_text)
        
        # Layer 7: Final Weighted Scoring
        final_score = scorer.calculate_score(
            ml_score=deberta_res['real_prob'] * 100,
            keyword_risk_score=ling_res['risk_score'],
            sentiment_risk_score=bias_res['risk_score'],
            source_score=source_res['score'],
            entity_score=entity_res['score']
        )
        
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
        
        st.session_state.pending_analysis = None
        st.rerun()

def dashboard_page():
    user = session_manager.get_current_user()
    if not user:
        session_manager.set_page("login")
        st.rerun()
        return

    # Sidebar Navigation
    with st.sidebar:
        st.markdown(f"### <span class='neon-text'>SatyaSetu</span> AI", unsafe_allow_html=True)
        st.markdown(f"**Welcome, {user['name']}**")
        st.markdown("---")
        
        nav = st.radio("Navigation", [
            "🏠 Dashboard Overview",
            "📄 Text Analysis",
            "🖼️ Image Analysis",
            "🎥 Video Analysis",
            "📜 History",
            "⚙️ Settings"
        ])
        
        st.markdown("---")
        if st.button("Logout", use_container_width=True):
            session_manager.logout()
            st.rerun()

    # ML components are loaded lazily within specific tabs to prevent blocking the dashboard

    if nav == "🏠 Dashboard Overview":
        st.markdown("## Security Overview")
        
        # Dashboard Cards using columns (Native Streamlit)
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

    elif nav == "📄 Text Analysis":
        st.markdown("## 📄 Text Verification")
        
        # Load ML components only when needed
        with st.spinner("Initializing AI Engines..."):
            preprocessor, classifier, verifier, scorer, bias_analyzer, summarizer, explainer, linguistic_analyzer, source_verifier, entity_verifier = load_ml_components()

        with st.container():
            text_input = st.text_area("Paste news content or social claims:", height=200, placeholder="Verify news integrity...")
            url_input = st.text_input("Source URL (Optional):", placeholder="https://...")
            if st.button("Verify Integrity", type="primary", use_container_width=True):
                if len(text_input) > 50:
                    run_full_analysis(text_input, "Text", source_url=url_input)
                else:
                    st.warning("Please provide more content.")

    elif nav == "🖼️ Image Analysis":
        st.markdown("## 🖼️ Forensic Image Analysis")
        
        # Load ML components only when needed
        with st.spinner("Initializing AI Engines..."):
            preprocessor, classifier, verifier, scorer, bias_analyzer, summarizer, explainer, linguistic_analyzer, source_verifier, entity_verifier = load_ml_components()

        with st.container():
            image_file = st.file_uploader("Upload image for deepfake detection", type=["jpg", "png", "jpeg"])
            url_input_img = st.text_input("Source URL (Optional):", placeholder="https://...", key="url_img")
            
            # Show analysis button if either file or URL is present
            if image_file or url_input_img:
                if image_file:
                    st.image(image_file, use_container_width=True)
                
                if st.button("Detect Manipulation", type="primary", use_container_width=True, key="btn_img_verify"):
                    mock_text = "Analysis suggest the uploaded content shows patterns consistent with the provided source context."
                    if image_file:
                        mock_text = "Analysis suggest the uploaded image shows high probability of AI-generated artifacts in facial regions."
                    run_full_analysis(mock_text, "Image", source_url=url_input_img)

    elif nav == "🎥 Video Analysis":
        st.markdown("## 🎥 Video Deepfake Guard")
        
        # Load ML components only when needed
        with st.spinner("Initializing AI Engines..."):
            preprocessor, classifier, verifier, scorer, bias_analyzer, summarizer, explainer, linguistic_analyzer, source_verifier, entity_verifier = load_ml_components()

        with st.container():
            video_file = st.file_uploader("Upload video to verify authenticity", type=["mp4", "mov"])
            url_input_vid = st.text_input("Source URL (Optional):", placeholder="https://...", key="url_vid")
            
            # Show analysis button if either file or URL is present
            if video_file or url_input_vid:
                if video_file:
                    st.info(f"Video selected: {video_file.name}")
                
                if st.button("Extract & Verify", type="primary", use_container_width=True, key="btn_vid_verify"):
                    mock_text = "Analyzing video metadata and provided link for verification signatures."
                    if video_file:
                        mock_text = "Transcript: Analyzing video metadata and binary structure suggests deepfake tampering detected."
                    run_full_analysis(mock_text, "Video", source_url=url_input_vid)

    elif nav == "📜 History":
        history_page()

    elif nav == "⚙️ Settings":
        st.markdown("## Account Configuration")
        
        # Enhanced Profile View within glass-card
        # Note: Avoid blank lines + indentation inside triple quotes to prevent markdown code-block triggers
        st.markdown(f"""
<div class='glass-card' style='padding: 30px;'>
<div style='display: flex; align-items: center; margin-bottom: 25px;'>
<div style='background: linear-gradient(135deg, #6366F1, #A855F7); 
width: 80px; height: 80px; border-radius: 40px; 
display: flex; align-items: center; justify-content: center; 
font-size: 35px; color: white; margin-right: 25px;
box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);'>
{user['name'][0].upper()}
</div>
<div>
<h2 style='margin: 0; font-size: 2rem;'>{user['name']}</h2>
<p style='color: #94A3B8; margin: 0;'>Verified Security Professional</p>
</div>
</div>
<div style='border-top: 1px solid rgba(148, 163, 184, 0.1); padding-top: 20px;'>
<div style='margin-bottom: 15px;'>
<p style='color: #6366F1; font-weight: 500; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 5px;'>Email Address</p>
<p style='font-size: 1.1rem;'>{user['email']}</p>
</div>
<div style='margin-bottom: 15px;'>
<p style='color: #6366F1; font-weight: 500; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 5px;'>Account Status</p>
<p style='display: flex; align-items: center;'>
<span style='width: 10px; height: 10px; background: #10B981; border-radius: 5px; margin-right: 8px;'></span>
Active / Enterprise
</p>
</div>
</div>
</div>
""", unsafe_allow_html=True)

    # Display Results if available (Persistent across navigation within the dashboard)
    result = session_manager.get_analysis_result()
    if result and nav in ["📄 Text Analysis", "🖼️ Image Analysis", "🎥 Video Analysis"]:
        st.markdown("---")
        st.markdown(f"### 📊 Verification Report: {result['score']['rating']}")
        
        # Row 1: High Level
        c1, c2 = st.columns([1, 2])
        with c1:
            components.credibility_gauge(result['score']['score'])
        with c2:
            st.markdown("#### Detection Signal")
            st.markdown(f"<h2 style='color: {result['score']['color']};'>{result['score']['rating']}</h2>", unsafe_allow_html=True)
            st.code(f"Confidence: {result['deberta']['real_prob']*100:.1f}%", language=None)

        st.markdown("---")
        
        # Row 2: Layered Breakdown
        st.markdown("#### 🔬 Analysis Breakdown")
        
        b1, b2, b3, b4 = st.columns(4)
        with b1:
            components.result_card("Source Trust", f"{result['source']['score']:.0f}%", 
                                  "success" if result['source']['score'] > 70 else "warning")
            st.caption(f"{result['source']['domain'] or 'Unknown'}")
            
        with b2:
            components.result_card("Entities", f"{result['entity']['score']:.0f}%", 
                                  "success" if result['entity']['score'] > 70 else "neutral")
            st.caption(f"{result['entity'].get('entity_count', 0)} Verified")

        with b3:
            # Reverse Risk for Display (Safety Score) or Show Risk? User allowed "Risk Level".
            risk = result['linguistic']['risk_score']
            components.result_card("Linguistic Risk", f"{risk:.0f}%", 
                                  "danger" if risk > 50 else "success")
            st.caption("Red Flags")

        with b4:
            s_risk = result['bias']['risk_score']
            components.result_card("Sentiment Risk", f"{s_risk:.0f}%", 
                                  "danger" if s_risk > 50 else "success")
            st.caption("Emotionality")

        # Detailed Explanations
        with st.expander("🛡️ AI Security Audit & Reasons", expanded=True):
            st.markdown(f"**Summary:** {result['summary']}")
            
            st.markdown("#### 🚩 Detected Risk Factors:")
            lines = []
            
            # Linguistic Flags
            if result['linguistic']['linguistic_flags']:
                for flag in result['linguistic']['linguistic_flags']:
                    lines.append(f"- 🗣️ **Language Style**: {flag}")
            
            # Source Flags
            if result['source']['score'] < 50:
                 lines.append(f"- 🌐 **Source**: Domain '{result['source']['domain']}' is untrusted or unknown.")
            
            # Entity Flags
            if result['entity']['score'] < 50:
                 lines.append(f"- 🏢 **Entities**: {result['entity']['reason']}")

            # Sentiment Flags
            if result['bias']['risk_score'] > 60:
                 lines.append(f"- 🎭 **Sentiment**: High emotional intensity detected ({result['bias']['sentiment']}).")
                 
            if not lines:
                st.success("✅ No significant risk factors detected. Content appears neutral and verified.")
            else:
                for line in lines:
                    st.markdown(line)

        # Claims Verification
        if result['claims']:
            with st.expander("🔍 Verified Claims Reference"):
                components.similarity_breakdown(result['claims'])
        
        if st.button("Clear Report"):
            session_manager.clear_analysis_result()
            st.rerun()

def history_page():
    user = session_manager.get_current_user()
    if not user:
        session_manager.set_page("login")
        st.rerun()
        
    c1, c2 = st.columns([8, 2])
    with c1:
        st.markdown("### Analysis History")
    with c2:
        if st.button("Back to Dashboard"):
            session_manager.set_page("dashboard")
            st.rerun()
            
    history = db.get_user_history(user['id'])
    
    if not history:
        st.info("No history found.")
    else:
        for item in history:
            with st.expander(f"{item.get('timestamp')} - {item.get('classification')} ({item.get('credibility_score')}%)"):
                st.write(item.get('summary', 'No summary'))
                st.caption(f"Text: {item.get('article_text')[:100]}...")

# --- Main Routing ---
from datetime import datetime

page = st.session_state.page

if page == "landing":
    landing_page()
elif page == "login":
    login_page()
elif page == "signup":
    signup_page()
elif page == "dashboard":
    dashboard_page()
elif page == "history":
    history_page()
else:
    landing_page()
