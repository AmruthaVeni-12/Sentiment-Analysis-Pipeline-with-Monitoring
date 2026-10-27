import streamlit as st
from src.ui.styles import render_footer

def render():
    # Hero Box with strong contrast
    st.markdown("""
    <div class="hero-box">
        <h1 style="margin: 0 0 10px 0; color: #ffffff;">
            How <span class="gold-accent">Sentiment</span> Relates to Movie Reviews
        </h1>
        <p style="color: #f1f5f9; font-size: 1.1rem; margin: 0; line-height: 1.7;">
            Movie critiques express nuanced emotional reception that simple binary ratings (like or dislike) cannot capture. 
            CinePulse translates written audience opinions into an <b>accurate 5-star sentiment scale</b>, mapping textual nuance into structured, quantifiable film scores.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 5-Tier Sentiment Scale
    st.markdown("<h3>⭐ The 5-Point Sentiment Scale</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#cbd5e1; font-size:0.95rem; margin-bottom: 16px;'>Every review submitted to CinePulse is classified into one of five distinct sentiment tiers:</p>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown("""
        <div class="tier-box" style="border-top: 3px solid #dc2626;">
            <div style="font-weight:700; color:#ef4444; font-size:1rem;">★ 1 Star</div>
            <span class="badge-pill badge-vneg">Very Negative</span>
            <div style="font-size:0.85rem; color:#cbd5e1; margin-top:6px;">Severe critical failure, unwatchable, incoherent.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="tier-box" style="border-top: 3px solid #ea580c;">
            <div style="font-weight:700; color:#f97316; font-size:1rem;">★★ 2 Stars</div>
            <span class="badge-pill badge-neg">Negative</span>
            <div style="font-size:0.85rem; color:#cbd5e1; margin-top:6px;">Disappointing, weak script, poor pacing.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="tier-box" style="border-top: 3px solid #ca8a04;">
            <div style="font-weight:700; color:#eab308; font-size:1rem;">★★★ 3 Stars</div>
            <span class="badge-pill badge-neu">Neutral</span>
            <div style="font-size:0.85rem; color:#cbd5e1; margin-top:6px;">Average popcorn flick, passable, mixed reaction.</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="tier-box" style="border-top: 3px solid #2563eb;">
            <div style="font-weight:700; color:#60a5fa; font-size:1rem;">★★★★ 4 Stars</div>
            <span class="badge-pill badge-pos">Positive</span>
            <div style="font-size:0.85rem; color:#cbd5e1; margin-top:6px;">Compelling story, solid acting, highly recommended.</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown("""
        <div class="tier-box" style="border-top: 3px solid #16a34a;">
            <div style="font-weight:700; color:#4ade80; font-size:1rem;">★★★★★ 5 Stars</div>
            <span class="badge-pill badge-vpos">Very Positive</span>
            <div style="font-size:0.85rem; color:#cbd5e1; margin-top:6px;">Masterpiece, brilliant direction, exceptional cinema.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Core Application Workflow
    st.markdown("<h3>🎯 How the Application Works</h3>", unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div class="app-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">✍️</div>
            <h4 style="margin: 0 0 8px 0; color: #ffffff; font-size: 1.15rem;">1. Post Reviews</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0;">
                Submit movie details and your review. The model assigns a 1-to-5 star score and saves it to the persistent database.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
        <div class="app-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">🔍</div>
            <h4 style="margin: 0 0 8px 0; color: #ffffff; font-size: 1.15rem;">2. Film Search & Justify</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0;">
                Search any title to view aggregate star ratings, all user postings, and an automated 4–5 sentence rating justification.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown("""
        <div class="app-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">⚡</div>
            <h4 style="margin: 0 0 8px 0; color: #ffffff; font-size: 1.15rem;">3. Live Sentiment Studio</h4>
            <p style="color: #cbd5e1; font-size: 0.95rem; margin: 0;">
                Test arbitrary review sentences to view immediate 5-class probability distributions, confidence metrics, and latency.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(render_footer(), unsafe_allow_html=True)
