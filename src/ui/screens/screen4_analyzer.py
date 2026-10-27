import streamlit as st
import requests
import plotly.express as px
import pandas as pd
from src.ui.styles import render_footer

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

# Standard 5 sentiment classes in strict consistent order
ORDERED_CLASSES = [
    "Very Negative",
    "Negative",
    "Neutral",
    "Positive",
    "Very Positive"
]

def render():
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <h1 class="page-title">⚡ Live Sentiment Studio</h1>
        <p class="page-subtitle">
            Direct text-analysis workspace. Paste any film review excerpt, snippet, or critical reaction to generate instant 5-class predictions and probability distributions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sample Quick Prompts
    st.markdown("""
<div style="margin-bottom:10px;">
  <span style='font-size:0.85rem; font-weight:600; color:#94A3B8; text-transform:uppercase; letter-spacing:0.5px;'>Quick-load sample critiques:</span>
</div>
""", unsafe_allow_html=True)
    c_p1, c_p2, c_p3 = st.columns(3)
    sample_text = ""
    with c_p1:
        st.markdown("<div class='secondary-btn-wrap'>", unsafe_allow_html=True)
        if st.button("🌟 Astonishing masterpiece...", use_container_width=True):
            sample_text = "An astonishing masterpiece with flawless direction, extraordinary acting, and an unforgettable story."
        st.markdown("</div>", unsafe_allow_html=True)
    with c_p2:
        st.markdown("<div class='secondary-btn-wrap'>", unsafe_allow_html=True)
        if st.button("🍿 Average popcorn flick...", use_container_width=True):
            sample_text = "An average popcorn movie with standard tropes. The plot offers few surprises but is mildly entertaining."
        st.markdown("</div>", unsafe_allow_html=True)
    with c_p3:
        st.markdown("<div class='secondary-btn-wrap'>", unsafe_allow_html=True)
        if st.button("⚠️ Painfully dull & atrocious...", use_container_width=True):
            sample_text = "Painfully dull, atrocious dialogue, and completely lifeless performances throughout. A total waste of time."
        st.markdown("</div>", unsafe_allow_html=True)

    user_input_text = st.text_area(
        "User Input Text",
        value=sample_text,
        height=125,
        placeholder="Type or paste any movie review snippet here...",
        label_visibility="collapsed"
    )

    # Word & Character Count
    char_count = len(user_input_text)
    word_count = len(user_input_text.split()) if user_input_text.strip() else 0
    st.markdown(
        f"<div style='text-align:right; font-size:0.82rem; color:#94A3B8; margin-top:-6px; margin-bottom:12px;'>"
        f"{word_count} words · {char_count} characters"
        f"</div>",
        unsafe_allow_html=True
    )

    analyze_btn = st.button("⚡ Analyze Sentiment", use_container_width=True)

    if analyze_btn or (user_input_text and len(user_input_text.strip()) > 3):
        if not user_input_text.strip():
            st.warning("Please enter review text to analyze.")
            return

        with st.spinner("Classifying sentiment across all 5 classes..."):
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
                st.error(f"Failed to communicate with API server: {e}")
                return

            st.markdown("<h3 style='margin-top: 24px;'>🎯 Model Prediction Result</h3>", unsafe_allow_html=True)

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
                <div class="saas-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center; border-left: 4px solid #8B5CF6;">
                    <div style="color: #94A3B8; font-size: 0.82rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;">Predicted Rating</div>
                    <div style="font-size: 2.3rem; font-weight: 800; color: #F59E0B; margin: 4px 0;">
                        {'★' * pred_data['star_rating']}
                    </div>
                    <div style="margin-bottom: 14px;">
                        <span class="sentiment-badge {badge_class}" style="font-size: 0.95rem !important;">{pred_data['sentiment_label']} ({pred_data['star_rating']}/5)</span>
                    </div>
                    <div style="display: flex; gap: 30px; border-top: 1px solid #1E293B; padding-top: 14px;">
                        <div>
                            <span style="color:#94A3B8; font-size:0.8rem; display:block; font-weight:600;">Confidence</span>
                            <span style="font-weight:800; color:#22D3EE; font-size:1.25rem;">{pred_data['confidence_score'] * 100:.1f}%</span>
                        </div>
                        <div>
                            <span style="color:#94A3B8; font-size:0.8rem; display:block; font-weight:600;">Inference Latency</span>
                            <span style="font-weight:800; color:#8B5CF6; font-size:1.25rem;">{pred_data['inference_time_ms']} ms</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            with col_res2:
                prob_dict = pred_data.get("probabilities", {})
                if prob_dict:
                    # Maintain strict consistent 5-class ordering
                    ordered_data = []
                    for cls_name in ORDERED_CLASSES:
                        ordered_data.append({
                            "Class": cls_name,
                            "Probability": prob_dict.get(cls_name, 0.0) * 100
                        })
                    df_probs = pd.DataFrame(ordered_data)
                    
                    colors = ["#EF4444", "#F97316", "#F59E0B", "#22D3EE", "#10B981"]
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
                        title=dict(text="5-Class Probability Distribution", font=dict(size=14, color="#F8FAFC")),
                        showlegend=False,
                        height=240,
                        margin=dict(l=10, r=20, t=30, b=10),
                        paper_bgcolor="#151F32",
                        plot_bgcolor="#151F32",
                        font=dict(color="#F8FAFC", family="Inter", size=13)
                    )
                    fig.update_xaxes(title="", range=[0, 100], gridcolor="#1E293B", tickfont=dict(color="#94A3B8"))
                    fig.update_yaxes(title="", gridcolor="#1E293B", tickfont=dict(color="#F8FAFC"))
                    st.plotly_chart(fig, use_container_width=True)

    st.markdown(render_footer(), unsafe_allow_html=True)
