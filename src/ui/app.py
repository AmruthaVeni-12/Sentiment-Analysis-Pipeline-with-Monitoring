import streamlit as st
from src.ui.styles import CUSTOM_CSS
from src.ui.screens import screen1_overview, screen2_postings, screen3_search, screen4_analyzer

st.set_page_config(
    page_title="CinePulse · Movie Sentiment Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified high-contrast design
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Minimalist, high-contrast sidebar
st.sidebar.markdown("""
<div style="padding: 12px 0 24px 0; border-bottom: 1px solid #1e293b; margin-bottom: 16px;">
    <h2 style="margin: 0; font-size: 1.5rem; font-weight: 800; color: #ffffff;">
        🎬 <span style="color: #f59e0b;">CinePulse</span>
    </h2>
    <p style="margin: 4px 0 0 0; color: #cbd5e1; font-size: 0.85rem; font-weight: 500;">
        Movie Sentiment Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

nav_choice = st.sidebar.radio(
    "Navigation",
    [
        "🎬 Screen 1: Overview",
        "✍️ Screen 2: Post Review",
        "🔍 Screen 3: Search Film",
        "⚡ Screen 4: Live Analyzer",
        "📈 Evidently Drift Monitoring"
    ],
    index=0,
    label_visibility="collapsed"
)

# Render screens
if nav_choice == "🎬 Screen 1: Overview":
    screen1_overview.render()

elif nav_choice == "✍️ Screen 2: Post Review":
    screen2_postings.render()

elif nav_choice == "🔍 Screen 3: Search Film":
    screen3_search.render()

elif nav_choice == "⚡ Screen 4: Live Analyzer":
    screen4_analyzer.render()

elif nav_choice == "📈 Evidently Drift Monitoring":
    st.markdown("<h2>📈 Evidently AI Drift & Model Quality</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#cbd5e1; font-size:1rem;'>Detect distribution shift in incoming user critiques against reference IMDb baselines.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    col_d1, col_d2 = st.columns([1, 4])
    with col_d1:
        run_drift = st.button("🔄 Check Data Drift", use_container_width=True)
        
    from src.monitoring.drift import generate_drift_report
    if run_drift or st.checkbox("Show cached drift report", value=True):
        with st.spinner("Analyzing text length, vocabulary & rating shifts..."):
            summary = generate_drift_report()
            
            m1, m2, m3 = st.columns(3)
            with m1:
                status_txt = "⚠️ Drift Detected" if summary.get("drift_detected") else "✅ Baseline Stable"
                st.metric("Drift Status", status_txt)
            with m2:
                st.metric("Drift Share", f"{summary.get('drift_share', 0.0) * 100:.1f}%")
            with m3:
                st.metric("Samples Logged", summary.get("total_production_samples", 0))

            html_report_path = summary.get("report_html_path")
            if html_report_path and open(html_report_path, "r", encoding="utf-8"):
                st.markdown("<h3 style='margin-top:24px;'>📊 Interactive Evidently Report</h3>", unsafe_allow_html=True)
                with open(html_report_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                st.components.v1.html(html_content, height=750, scrolling=True)
