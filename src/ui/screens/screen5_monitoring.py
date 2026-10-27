import os
import streamlit as st
import pandas as pd
from src.ui.styles import render_footer
from src.monitoring.drift import generate_drift_report

def render():
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <h1 class="page-title">📈 Evidently Drift Monitoring</h1>
        <p class="page-subtitle">
            Continuous ML quality assurance — detect data drift, vocabulary shifts, and prediction distribution shifts in incoming critiques against baseline training distributions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Action Toolbar
    col_t1, col_t2 = st.columns([1, 3])
    with col_t1:
        run_analysis = st.button("🔄 Run Drift Analysis", use_container_width=True)
    with col_t2:
        auto_load = st.checkbox("Display active drift inspection report", value=True)

    if run_analysis or auto_load:
        with st.spinner("Evaluating statistical Kolmogorov-Smirnov & Wasserstein drift tests..."):
            summary = generate_drift_report()

        # Metrics KPI Grid
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            is_drifted = summary.get("drift_detected", False)
            status_label = "⚠️ Drift Detected" if is_drifted else "✅ Baseline Stable"
            status_sub = "Threshold breached" if is_drifted else "Within 95% CI"
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Drift Status</div>
                <div class="kpi-value" style="font-size:1.35rem; color:{'#F87171' if is_drifted else '#34D399'};">
                    {status_label}
                </div>
                <div class="kpi-sub" style="color:#94A3B8;">{status_sub}</div>
            </div>
            """, unsafe_allow_html=True)

        with m2:
            drift_share = summary.get("drift_share", 0.0) * 100
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Drift Share</div>
                <div class="kpi-value" style="color:#8B5CF6;">{drift_share:.1f}%</div>
                <div class="kpi-sub">Tolerance ceiling: 50%</div>
            </div>
            """, unsafe_allow_html=True)

        with m3:
            drifted_cols = summary.get("drifted_columns_count", 0)
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Drifted Features</div>
                <div class="kpi-value">{drifted_cols}</div>
                <div class="kpi-sub">Length, words, class</div>
            </div>
            """, unsafe_allow_html=True)

        with m4:
            prod_samples = summary.get("total_production_samples", 0)
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">Production Samples</div>
                <div class="kpi-value" style="color:#22D3EE;">{prod_samples}</div>
                <div class="kpi-sub">Captured in SQLite buffer</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

        # Baseline & Reference Dataset Specs
        col_ref1, col_ref2 = st.columns(2)
        with col_ref1:
            st.markdown("""
            <div class="saas-card" style="margin-bottom: 15px;">
                <h4 style="margin: 0 0 10px 0; color: #F8FAFC; font-size: 1rem;">📦 Reference Distribution (Baseline)</h4>
                <div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.7;">
                    • <b>Dataset:</b> IMDb 5-Class Stratified Test Split (<code>data/processed/test.csv</code>)<br>
                    • <b>Sample Size:</b> 156 balanced movie critiques<br>
                    • <b>Monitored Signals:</b> Character length, token count, predicted sentiment class
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_ref2:
            st.markdown(f"""
            <div class="saas-card" style="margin-bottom: 15px;">
                <h4 style="margin: 0 0 10px 0; color: #F8FAFC; font-size: 1rem;">⚡ Live Production Window</h4>
                <div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.7;">
                    • <b>Telemetry Source:</b> <code>drift_logs</code> table in SQLite<br>
                    • <b>Active Invocations:</b> {prod_samples} reviews processed<br>
                    • <b>Drift Test Protocol:</b> Two-sample Kolmogorov-Smirnov test (p=0.05)
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Embedded Report Container
        html_report_path = summary.get("report_html_path")
        if html_report_path and os.path.exists(html_report_path):
            st.markdown("""
            <div style="margin: 20px 0 12px 0;">
                <h3 style="margin: 0;">📊 Evidently AI Telemetry Report</h3>
                <p style="color: #94A3B8; font-size: 0.88rem; margin: 4px 0 0 0;">
                    Interactive statistical comparison of input distributions and model predictions.
                </p>
            </div>
            """, unsafe_allow_html=True)
            with open(html_report_path, "r", encoding="utf-8") as f:
                html_content = f.read()
            st.components.v1.html(html_content, height=800, scrolling=True)
        else:
            st.info("Report file not generated yet. Click 'Run Drift Analysis' above.")

    st.markdown(render_footer(), unsafe_allow_html=True)
