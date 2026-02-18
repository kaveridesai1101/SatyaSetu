"""
Reusable UI Components for VeriSense
"""

import streamlit as st
import plotly.graph_objects as go
import config

def load_css():
    """Load custom CSS"""
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def header_section(show_nav=False):
    """Render application header"""
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"## 🛡️ {config.APP_TITLE}")
        st.caption(config.APP_SUBTITLE)
    
    if show_nav:
        with col2:
            pass # Nav items handled in sidebar or explicit buttons usually

def credibility_gauge(score: float):
    """Futuristic Cyber Credibility Gauge"""
    
    # Neon Theme Colors
    color = "#14B8A6" # Neon Teal
    if score < 40:
        color = "#EF4444" # Neon Red
    elif score < 70:
        color = "#F59E0B" # Neon Amber
        
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = score,
        number = {'font': {'color': '#FFFFFF', 'family': 'Outfit', 'size': 44}},
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Confidence Index", 'font': {'color': '#14B8A6', 'family': 'Outfit', 'size': 20}},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#94A3B8"},
            'bar': {'color': color},
            'bgcolor': "rgba(30, 41, 59, 0.4)",
            'borderwidth': 1,
            'bordercolor': "rgba(148, 163, 184, 0.1)",
            'steps': [
                {'range': [0, 100], 'color': 'rgba(15, 23, 42, 0.5)'}],
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=320, 
        margin=dict(l=40, r=40, t=60, b=20),
        font={'family': "Inter"}
    )
    st.plotly_chart(fig, use_container_width=True)

def result_card(title, value, type="neutral"):
    """Glassmorphic Cyber Result Card"""
    accent_color = "#14B8A6"
    
    if type == "success":
        accent_color = "#10B981"
    elif type == "danger":
        accent_color = "#EF4444"
    elif type == "warning":
        accent_color = "#F59E0B"
        
    st.markdown(
        f"""
        <div class="glass-card" style="border-top: 3px solid {accent_color};">
            <p style="margin: 0; font-size: 0.75rem; color: #94A3B8; font-weight: 600; text-transform: uppercase; letter-spacing: 0.1em;">{title}</p>
            <h3 style="margin: 8px 0 0 0; color: #FFFFFF; font-family: 'Outfit', sans-serif; font-weight: 700;">{value}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

def similarity_breakdown(verified_claims):
    """Render list of verified claims"""
    if not verified_claims:
        st.info("No verifiable claims detected.")
        return

    for claim in verified_claims:
        icon = "✅" if claim['status'] == 'Verified' else "⚠️" if claim['status'] == 'Related' else "❓"
        with st.expander(f"{icon} {claim['claim'][:60]}..."):
            st.markdown(f"**Claim:** {claim['claim']}")
            st.markdown(f"**Match:** {claim['match_source']}")
            st.markdown(f"**Similarity:** {int(claim['similarity_score']*100)}%")

def shap_plot_placeholder(shap_values):
    """
    Render SHAP plot. 
    Note: Full SHAP JS visualization in Streamlit is tricky without components.
    We will use a static matplotlib plot for stability or text highlighting.
    """
    import shap
    import matplotlib.pyplot as plt
    
    if shap_values is None:
        st.warning("Interpretation unavailable.")
        return
        
    try:
        # Create a matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 3))
        # shap.plots.text is interactive and hard to embed static
        # shap.plots.bar is easier
        shap.plots.bar(shap_values[0], show=False)
        st.pyplot(plt.gcf())
        plt.clf()
    except Exception as e:
        st.error("Could not render explanation plot.")
