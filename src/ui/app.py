import streamlit as st
from src.ui.styles import CUSTOM_CSS
from src.ui.screens import screen1_overview, screen2_postings, screen3_search, screen4_analyzer

st.set_page_config(
    page_title="CinePulse · Movie Sentiment Intelligence",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply unified design system
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Minimalist, elegant sidebar
st.sidebar.markdown("""
<div style="padding: 10px 0 20px 0;">
    <h2 style="margin: 0; font-size: 1.45rem; font-weight: 800; letter-spacing: -0.5px;">
        🎬 <span style="background: linear-gradient(135deg, #60a5fa, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">CinePulse</span>
    </h2>
    <p style="margin: 4px 0 0 0; color: #64748b; font-size: 0.8rem; font-weight: 500;">
        Movie Sentiment Intelligence
    </p>
</div>
""", unsafe_allow_html=True)

nav_choice = st.sidebar.radio(
    "Navigation",
    [
        "🎬 Overview",
        "✍️ Post Review",
        "🔍 Search Film",
        "⚡ Live Analyzer",
        "📈 Drift & Monitoring"
    ],
    index=0,
    label_visibility="collapsed"
)

# Render chosen screen
if nav_choice == "🎬 Overview":
    screen1_overview.render()

elif nav_choice == "✍️ Post Review":
    screen2_postings.render()

elif nav_choice == "🔍 Search Film":
    screen3_search.render()

elif nav_choice == "⚡ Live Analyzer":
    screen4_analyzer.render()

elif nav_choice == "📈 Drift & Monitoring":
    st.markdown("## 📈 Evidently AI Drift & Model Quality")
    st.markdown("<p style='color:#94a3b8; font-size:0.95rem;'>Detect distribution shift in incoming user critiques against reference IMDb baselines.</p>", unsafe_allow_html=True)
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
                st.markdown("<h3 style='margin-top:20px;'>📊 Interactive Evidently Report</h3>", unsafe_allow_html=True)
                with open(html_report_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                st.components.v1.html(html_content, height=750, scrolling=True)
