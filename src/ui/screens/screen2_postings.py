import streamlit as st
import requests
from src.ui.styles import render_footer

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def render():
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <h1 class="page-title">Post a Movie Review</h1>
        <p class="page-subtitle">
            Explore audience sentiment with AI-powered movie review analysis. Submit a film review to trigger real-time 5-class sentiment classification and persist the entry to the database.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("posting_form"):
        st.markdown("<div style='font-size:0.85rem; font-weight:600; color:#8B5CF6; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:12px;'>Film Metadata & Audience Critique</div>", unsafe_allow_html=True)

        # Row 1: Movie Name (required) & Release Year
        col1, col2 = st.columns([3, 1.2])
        with col1:
            movie_name = st.text_input("Movie Name *", placeholder="e.g. Oppenheimer, Dune, The Godfather")
        with col2:
            released_year = st.number_input("Release Year", min_value=1900, max_value=2035, value=2023, step=1)

        # Row 2: Lead Cast & Director / Tech Info
        col3, col4 = st.columns(2)
        with col3:
            cast = st.text_input("Lead Cast", placeholder="e.g. Cillian Murphy, Emily Blunt, Robert Downey Jr.")
        with col4:
            direction_info = st.text_input("Director & Technical Information", placeholder="e.g. Christopher Nolan (IMAX 70mm cinematography)")

        # Full Width: About Movie / Audience Review (required)
        about_movie = st.text_area(
            "About Movie / Audience Review *",
            height=125,
            placeholder="Write your movie critique here (e.g. 'A breathtaking cinematic achievement with intense performances and a masterclass in musical scoring.')"
        )

        submit_btn = st.form_submit_button("⚡ Analyze Review", use_container_width=True)

    if submit_btn:
        if not movie_name.strip():
            st.error("Please provide a valid Movie Name.")
            return
        if not about_movie.strip() or len(about_movie.strip()) < 8:
            st.error("Please enter a review critique of at least 8 characters.")
            return

        payload = {
            "movie_name": movie_name.strip(),
            "released_year": int(released_year),
            "cast": cast.strip() if cast else None,
            "direction_and_info": direction_info.strip() if direction_info else None,
            "about_movie": about_movie.strip()
        }

        with st.spinner("Classifying sentiment and recording telemetry..."):
            try:
                response = requests.post(f"{API_BASE_URL}/reviews/post", json=payload, timeout=8)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ {data['message']}")

                    badge_class = {
                        0: "badge-vneg",
                        1: "badge-neg",
                        2: "badge-neu",
                        3: "badge-pos",
                        4: "badge-vpos"
                    }.get(data["sentiment_class"], "badge-neu")

                    # Structured Result Card
                    st.markdown(f"""
                    <div class="saas-card" style="margin-top: 20px; border-left: 4px solid #8B5CF6;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 16px;">
                            <div>
                                <div style="font-size: 0.8rem; font-weight: 600; text-transform: uppercase; color: #94A3B8; letter-spacing: 0.5px;">
                                    Automated Inference Result
                                </div>
                                <h3 style="margin: 4px 0 0 0; color: #F8FAFC;">{data['movie_title']}</h3>
                            </div>
                            <span class="sentiment-badge {badge_class}">{data['sentiment_label']}</span>
                        </div>
                        <div style="display: flex; gap: 40px; align-items: center; flex-wrap: wrap;">
                            <div>
                                <span style="color:#94A3B8; font-size:0.82rem; display:block; font-weight:600;">Predicted Rating</span>
                                <span style="font-size:1.45rem; font-weight:800; color:#F59E0B;">{'★' * data['star_rating']}</span>
                                <span style="font-size:0.95rem; color:#F8FAFC; margin-left:4px;">({data['star_rating']}/5 Stars)</span>
                            </div>
                            <div>
                                <span style="color:#94A3B8; font-size:0.82rem; display:block; font-weight:600;">Prediction Confidence</span>
                                <span style="font-size:1.35rem; font-weight:800; color:#22D3EE;">{data['confidence_score'] * 100:.1f}%</span>
                            </div>
                            <div>
                                <span style="color:#94A3B8; font-size:0.82rem; display:block; font-weight:600;">Database Record</span>
                                <span style="font-size:0.95rem; font-weight:600; color:#CBD5E1;">Review #{data['review_id']} registered</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("💡 You can now search for this title in **Search Film** to inspect the aggregate score and AI justification!")
                else:
                    st.error(f"Backend error: {response.text}")
            except Exception as e:
                st.error(f"Failed to communicate with API server: {e}")

    st.markdown(render_footer(), unsafe_allow_html=True)
