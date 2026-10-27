import streamlit as st
from src.ui.styles import CUSTOM_CSS
from src.ui.screens import (
    screen1_overview,
    screen2_postings,
    screen3_search,
    screen4_analyzer,
    screen5_monitoring
)

st.set_page_config(
    page_title="CinePulse · Movie Sentiment Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply global SaaS design system
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Sidebar Header & Brand
st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="brand-title">
        <span>🎬 CinePulse</span>
        <span class="brand-badge">MLOps v1.0</span>
    </div>
    <div class="brand-sub">
        Movie Sentiment Intelligence Platform
    </div>
</div>
""", unsafe_allow_html=True)

nav_choice = st.sidebar.radio(
    "Navigation",
    [
        "🎬 Overview",
        "✍️ Post Movie Review",
        "🔍 Search Film",
        "⚡ Live Analyzer",
        "📈 Evidently Drift Monitoring"
    ],
    index=0,
    label_visibility="collapsed"
)

# Dispatch to Screen Modules
if nav_choice == "🎬 Overview":
    screen1_overview.render()

elif nav_choice == "✍️ Post Movie Review":
    screen2_postings.render()

elif nav_choice == "🔍 Search Film":
    screen3_search.render()

elif nav_choice == "⚡ Live Analyzer":
    screen4_analyzer.render()

elif nav_choice == "📈 Evidently Drift Monitoring":
    screen5_monitoring.render()
