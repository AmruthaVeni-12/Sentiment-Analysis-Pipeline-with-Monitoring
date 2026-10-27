import streamlit as st
from src.ui.styles import CUSTOM_CSS
from src.ui.screens import screen1_overview, screen2_postings, screen3_search, screen4_analyzer

st.set_page_config(
    page_title="Movie Sentiment MLOps Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Sidebar Navigation matching user's architecture
st.sidebar.title("🎬 Movie Sentiment MLOps")
st.sidebar.caption("5-Class Sentiment Intelligence System")

nav_choice = st.sidebar.radio(
    "Navigation :",
    [
        "Screen 1: Context & Overview",
        "Screen 2: Postings (Review Form)",
        "Screen 3: Search Movie & Justification",
        "Screen 4: Sentiment Analysis (Live)",
        "⚙️ MLOps Drift & Model Monitoring"
    ],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Pipeline Info")
st.sidebar.info(
    "**Dataset**: IMDb (5 Classes)\n\n"
    "**Baseline**: Calibrated LinearSVC\n\n"
    "**Deep Learning**: DistilBERT\n\n"
    "**MLOps**: DVC • MLflow • Evidently AI"
)

if nav_choice == "Screen 1: Context & Overview":
    screen1_overview.render()

elif nav_choice == "Screen 2: Postings (Review Form)":
    screen2_postings.render()

elif nav_choice == "Screen 3: Search Movie & Justification":
    screen3_search.render()

elif nav_choice == "Screen 4: Sentiment Analysis (Live)":
    screen4_analyzer.render()

elif nav_choice == "⚙️ MLOps Drift & Model Monitoring":
    st.markdown("## ⚙️ Evidently AI Drift & Model Monitoring")
    st.markdown("*Real-time detection of data drift, vocabulary shifts, and sentiment prediction distribution changes.*")
    st.markdown("---")
    
    col_d1, col_d2 = st.columns([1, 4])
    with col_d1:
        run_drift = st.button("🔄 Run Drift Analysis", use_container_width=True)
        
    from src.monitoring.drift import generate_drift_report
    if run_drift or st.checkbox("Show latest drift summary", value=True):
        with st.spinner("Computing Evidently AI drift metrics..."):
            summary = generate_drift_report()
            
            m1, m2, m3 = st.columns(3)
            with m1:
                status_color = "red" if summary.get("drift_detected") else "green"
                status_txt = "⚠️ DRIFT DETECTED" if summary.get("drift_detected") else "✅ STABLE (No Drift)"
                st.metric("Drift Status", status_txt)
            with m2:
                st.metric("Drift Share", f"{summary.get('drift_share', 0.0) * 100:.1f}%")
            with m3:
                st.metric("Production Samples", summary.get("total_production_samples", 0))

            html_report_path = summary.get("report_html_path")
            if html_report_path and open(html_report_path, "r", encoding="utf-8"):
                st.markdown("### 📈 Evidently AI Interactive Dashboard")
                with open(html_report_path, "r", encoding="utf-8") as f:
                    html_content = f.read()
                st.components.v1.html(html_content, height=800, scrolling=True)
