import streamlit as st
import plotly.express as px
import pandas as pd
from src.ui.styles import render_footer

def render():
    st.markdown("## 🎬 Screen 1: How Sentiment is Related to Movie Reviews")
    st.markdown("---")

    # Wireframe Main Box: "how sentiment is related to movie reviews"
    st.markdown("""
    <div class="metric-card">
        <h3>💡 Understanding the Sentiment Spectrum in Cinema</h3>
        <p>
            Movie reviews represent subjective audience critiques rich in qualitative sentiment, emotional intensity, and nuanced linguistic nuances. 
            In natural language processing (NLP), <b>sentiment classification</b> translates these qualitative textual signals into quantitative ratings.
        </p>
        <p>
            Rather than reducing complex opinions to a crude binary (positive vs. negative), our system structures sentiment into an 
            <b>ordinal 5-tier classification</b> mirroring the universal 1-to-5 star rating convention:
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown("""
        <div style="background:#2a1215; border:1px solid #d32f2f; border-radius:8px; padding:12px; text-align:center;">
            <h4>⭐ 1 Star</h4>
            <span class="rating-badge badge-very-neg">Very Negative</span>
            <p style="font-size:0.8rem; margin-top:8px;">Severe flaws, unwatchable, critical failure</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="background:#26121e; border:1px solid #c2185b; border-radius:8px; padding:12px; text-align:center;">
            <h4>⭐⭐ 2 Stars</h4>
            <span class="rating-badge badge-neg">Negative</span>
            <p style="font-size:0.8rem; margin-top:8px;">Below expectations, formulaic, weak execution</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="background:#271b0e; border:1px solid #f57c00; border-radius:8px; padding:12px; text-align:center;">
            <h4>⭐⭐⭐ 3 Stars</h4>
            <span class="rating-badge badge-neutral">Neutral</span>
            <p style="font-size:0.8rem; margin-top:8px;">Mixed reception, average, serviceable popcorn flick</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div style="background:#0f2038; border:1px solid #1976d2; border-radius:8px; padding:12px; text-align:center;">
            <h4>⭐⭐⭐⭐ 4 Stars</h4>
            <span class="rating-badge badge-pos">Positive</span>
            <p style="font-size:0.8rem; margin-top:8px;">Strong acting, engaging narrative, highly recommended</p>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        st.markdown("""
        <div style="background:#0f2716; border:1px solid #2e7d32; border-radius:8px; padding:12px; text-align:center;">
            <h4>⭐⭐⭐⭐⭐ 5 Stars</h4>
            <span class="rating-badge badge-very-pos">Very Positive</span>
            <p style="font-size:0.8rem; margin-top:8px;">Masterpiece, tour-de-force direction, exceptional depth</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Conceptual connection to the app workflow
    st.markdown("### 🔄 Application Workflow & Architecture")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("📝 **Screen 2: Postings**\n\nSubmit movie metadata, director, cast, and your 3–4 line review. The backend assigns a 5-class rating and persists it to the database.")
    with c2:
        st.success("🔍 **Screen 3: Search & Justify**\n\nSearch any film to view aggregated star ratings, classified user postings, and a 4–5 sentence NLP justification explaining why.")
    with c3:
        st.warning("⚡ **Screen 4: Live Analyzer**\n\nTest any review snippet directly through the inference engine to inspect probability distributions across all 5 sentiment classes.")

    st.markdown(render_footer(), unsafe_allow_html=True)
