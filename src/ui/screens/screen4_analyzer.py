import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from src.ui.styles import render_footer

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def render():
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0;">⚡ Real-Time Sentiment Studio</h2>
        <p style="color: #cbd5e1; font-size: 1rem; margin: 4px 0 0 0;">
            Test arbitrary movie snippets or audience critiques to inspect instant classification and 5-class probability distributions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sample prompt buttons
    st.markdown("<span style='font-size:0.9rem; font-weight:600; color:#cbd5e1;'>Sample review excerpts:</span>", unsafe_allow_html=True)
    c_p1, c_p2, c_p3 = st.columns(3)
    sample_text = ""
    with c_p1:
        if st.button("🌟 'Astonishing masterpiece...'", use_container_width=True):
            sample_text = "An astonishing masterpiece with flawless direction, extraordinary acting, and an unforgettable story."
    with c_p2:
        if st.button("🍿 'Average popcorn flick...'", use_container_width=True):
            sample_text = "An average popcorn movie with standard tropes. The plot offers few surprises but is mildly entertaining."
    with c_p3:
        if st.button("⚠️ 'Painfully dull and atrocious...'", use_container_width=True):
            sample_text = "Painfully dull, atrocious dialogue, and completely lifeless performances throughout. A total waste of time."

    user_input_text = st.text_area(
        "User Input Text",
        value=sample_text,
        height=115,
        placeholder="Type or paste any movie review snippet here...",
        label_visibility="collapsed"
    )

    analyze_btn = st.button("⚡ Run Sentiment Analysis", use_container_width=True)

    if analyze_btn or (user_input_text and len(user_input_text.strip()) > 3):
        if not user_input_text.strip():
            st.warning("Please enter some review text to analyze.")
            return

        with st.spinner("Analyzing sentiment across 5 classes..."):
            try:
                r = requests.post(
                    f"{API_BASE_URL}/sentiments",
                    json={"text": user_input_text.strip(), "model_type": "svm_baseline"},
                    timeout=5
                )
                if r.status_code != 200:
                    st.error(f"Inference error: {r.text}")
                    return
                pred_data = r.json()
            except Exception as e:
                st.error(f"Failed to connect to API server: {e}")
                return

            st.markdown("<h3 style='margin-top: 24px;'>🎯 Output Sentiment Analyzer</h3>", unsafe_allow_html=True)

            badge_class = {
                0: "badge-vneg",
                1: "badge-neg",
                2: "badge-neu",
                3: "badge-pos",
                4: "badge-vpos"
            }.get(pred_data["sentiment_class"], "badge-neu")

            col_res1, col_res2 = st.columns([1, 1])

            with col_res1:
                st.markdown(f"""
                <div class="app-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center;">
                    <div style="color: #cbd5e1; font-size: 0.9rem; font-weight: 600;">Predicted Rating</div>
                    <div style="font-size: 2.3rem; font-weight: 800; color: #fbbf24; margin: 4px 0;">
                        {'★' * pred_data['star_rating']}
                    </div>
                    <div style="margin-bottom: 14px;">
                        <span class="badge-pill {badge_class}" style="font-size: 1rem !important;">{pred_data['sentiment_label']}</span>
                    </div>
                    <div style="display: flex; gap: 24px; border-top: 1px solid #24344d; padding-top: 14px;">
                        <div>
                            <span style="color:#cbd5e1; font-size:0.8rem; display:block; font-weight:600;">Confidence</span>
                            <span style="font-weight:800; color:#38bdf8; font-size:1.25rem;">{pred_data['confidence_score'] * 100:.1f}%</span>
                        </div>
                        <div>
                            <span style="color:#cbd5e1; font-size:0.8rem; display:block; font-weight:600;">Inference Latency</span>
                            <span style="font-weight:800; color:#fbbf24; font-size:1.25rem;">{pred_data['inference_time_ms']} ms</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_res2:
                prob_dict = pred_data.get("probabilities", {})
                if prob_dict:
                    df_probs = pd.DataFrame({
                        "Class": list(prob_dict.keys()),
                        "Probability": [v * 100 for v in prob_dict.values()]
                    })
                    
                    colors = ["#ef4444", "#f97316", "#eab308", "#3b82f6", "#22c55e"]
                    fig = px.bar(
                        df_probs,
                        x="Probability",
                        y="Class",
                        orientation="h",
                        text=df_probs["Probability"].apply(lambda p: f"{p:.1f}%"),
                        color="Class",
                        color_discrete_sequence=colors
                    )
                    fig.update_layout(
                        title=dict(text="Class Probability Distribution", font=dict(size=15, color="#ffffff")),
                        showlegend=False,
                        height=240,
                        margin=dict(l=10, r=20, t=30, b=10),
                        paper_bgcolor="#131c2e",
                        plot_bgcolor="#131c2e",
                        font=dict(color="#ffffff", family="Plus Jakarta Sans", size=13)
                    )
                    fig.update_xaxes(title="", range=[0, 100], gridcolor="#24344d", tickfont=dict(color="#ffffff"))
                    fig.update_yaxes(title="", gridcolor="#24344d", tickfont=dict(color="#ffffff"))
                    st.plotly_chart(fig, use_container_width=True)

    st.markdown(render_footer(), unsafe_allow_html=True)
