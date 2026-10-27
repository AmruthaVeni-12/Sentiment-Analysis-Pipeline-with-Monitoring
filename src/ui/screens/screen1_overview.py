import streamlit as st
from src.ui.styles import render_footer

def render():
    # Hero Banner
    st.markdown("""
    <div class="hero-banner">
        <h1 style="margin: 0 0 10px 0;">
            How <span class="gradient-text">Sentiment</span> Relates to Movie Reviews
        </h1>
        <p style="color: #cbd5e1; font-size: 1.05rem; margin: 0; max-width: 850px; line-height: 1.6;">
            Movie critiques express complex emotional nuances that binary classification (thumbs up or thumbs down) completely flattens. 
            Our NLP engine translates nuanced language into an <b>accurate 5-star sentiment scale</b>, mapping subjective audience opinions directly into actionable metrics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # 5-Tier Sentiment Scale
    st.markdown("<h3>⭐ The 5-Point Sentiment Spectrum</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94a3b8; font-size:0.9rem; margin-bottom: 16px;'>Every review submitted to CinePulse is classified into one of five calibrated sentiment tiers:</p>", unsafe_allow_html=True)

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown("""
        <div class="tier-card" style="border-top: 3px solid #ef4444;">
            <div class="tier-title" style="color:#ef4444;">★ 1 Star</div>
            <span class="pill-badge pill-vneg">Very Negative</span>
            <div class="tier-desc">Critical disaster, unwatchable, incoherent storyline.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="tier-card" style="border-top: 3px solid #f97316;">
            <div class="tier-title" style="color:#f97316;">★★ 2 Stars</div>
            <span class="pill-badge pill-neg">Negative</span>
            <div class="tier-desc">Fails expectations, weak script, formulaic execution.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="tier-card" style="border-top: 3px solid #eab308;">
            <div class="tier-title" style="color:#eab308;">★★★ 3 Stars</div>
            <span class="pill-badge pill-neu">Neutral</span>
            <div class="tier-desc">Average popcorn flick, passable acting, forgettable.</div>
        </div>
        """, unsafe_allow_html=True)
    with c4:
        st.markdown("""
        <div class="tier-card" style="border-top: 3px solid #3b82f6;">
            <div class="tier-title" style="color:#3b82f6;">★★★★ 4 Stars</div>
            <span class="pill-badge pill-pos">Positive</span>
            <div class="tier-desc">Strong direction, engaging narrative, highly recommended.</div>
        </div>
        """, unsafe_allow_html=True)
    with c5:
        st.markdown("""
        <div class="tier-card" style="border-top: 3px solid #10b981;">
            <div class="tier-title" style="color:#10b981;">★★★★★ 5 Stars</div>
            <span class="pill-badge pill-vpos">Very Positive</span>
            <div class="tier-desc">Masterpiece, breathtaking visuals, phenomenal acting.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Core Application Features
    st.markdown("<h3>🎯 How the Application Works</h3>", unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">✍️</div>
            <h4 style="margin: 0 0 8px 0; color: #f8fafc; font-size: 1.05rem;">1. Post Reviews</h4>
            <p style="color: #94a3b8; font-size: 0.88rem; margin: 0;">
                Input film metadata, director, cast, and your 3–4 line critique. The AI instantly scores the review and saves it to the central film database.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">🔍</div>
            <h4 style="margin: 0 0 8px 0; color: #f8fafc; font-size: 1.05rem;">2. Film Search & Justify</h4>
            <p style="color: #94a3b8; font-size: 0.88rem; margin: 0;">
                Look up any film to see the aggregate star rating, individual audience critiques, and an automated 4–5 sentence justification explaining the score.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_f3:
        st.markdown("""
        <div class="glass-card" style="height: 100%;">
            <div style="font-size: 1.8rem; margin-bottom: 8px;">⚡</div>
            <h4 style="margin: 0 0 8px 0; color: #f8fafc; font-size: 1.05rem;">3. Live Sentiment Studio</h4>
            <p style="color: #94a3b8; font-size: 0.88rem; margin: 0;">
                Test arbitrary review sentences in real-time to inspect confidence gauges, class probabilities, and sub-millisecond inference speeds.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(render_footer(), unsafe_allow_html=True)
