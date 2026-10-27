import streamlit as st
import requests
from src.ui.styles import render_footer

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def render():
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0;">✍️ Post Movie Review</h2>
        <p style="color: #cbd5e1; font-size: 1rem; margin: 4px 0 0 0;">
            Submit film details and an audience review. The NLP engine will automatically classify the sentiment into 1 to 5 stars.
        </p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("posting_form"):
        col1, col2 = st.columns([3, 1])
        with col1:
            movie_name = st.text_input("Movie Name *", placeholder="e.g. Oppenheimer, Dune, The Godfather")
        with col2:
            released_year = st.number_input("Release Year", min_value=1900, max_value=2035, value=2023, step=1)

        col3, col4 = st.columns(2)
        with col3:
            cast = st.text_input("Lead Cast", placeholder="e.g. Cillian Murphy, Emily Blunt, Robert Downey Jr.")
        with col4:
            direction_info = st.text_input("Director & Technical Info", placeholder="e.g. Christopher Nolan (IMAX 70mm)")

        about_movie = st.text_area(
            "About Movie (in 3 to 4 lines) *",
            height=125,
            placeholder="Share your thoughts on the story, directing, and acting (e.g. 'A breathtaking cinematic achievement with intense performances and a masterclass in musical scoring.')"
        )

        submit_btn = st.form_submit_button("🚀 Submit & Analyze Review", use_container_width=True)

    if submit_btn:
        if not movie_name.strip():
            st.error("Please enter a valid Movie Name.")
            return
        if not about_movie.strip() or len(about_movie.strip()) < 8:
            st.error("Please provide a review of at least a few words (minimum 8 characters).")
            return

        payload = {
            "movie_name": movie_name.strip(),
            "released_year": int(released_year),
            "cast": cast.strip() if cast else None,
            "direction_and_info": direction_info.strip() if direction_info else None,
            "about_movie": about_movie.strip()
        }

        with st.spinner("Analyzing review and storing to database..."):
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

                    st.markdown(f"""
                    <div class="app-card" style="margin-top: 15px; border-left: 5px solid #f59e0b;">
                        <h4 style="margin: 0 0 14px 0; font-size: 1.15rem; color: #ffffff;">🎯 Sentiment Classification Summary</h4>
                        <div style="display: flex; gap: 35px; align-items: center; flex-wrap: wrap;">
                            <div>
                                <span style="color:#cbd5e1; font-size:0.85rem; display:block; font-weight:600;">Assigned Rating</span>
                                <span style="font-size:1.35rem; font-weight:800; color:#fbbf24;">{'★' * data['star_rating']} ({data['star_rating']}/5)</span>
                            </div>
                            <div>
                                <span style="color:#cbd5e1; font-size:0.85rem; display:block; font-weight:600;">Sentiment Tier</span>
                                <span class="badge-pill {badge_class}">{data['sentiment_label']}</span>
                            </div>
                            <div>
                                <span style="color:#cbd5e1; font-size:0.85rem; display:block; font-weight:600;">Model Confidence</span>
                                <span style="font-size:1.25rem; font-weight:800; color:#38bdf8;">{data['confidence_score'] * 100:.1f}%</span>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    st.info("💡 You can now search for this movie in **Screen 3** to see the aggregated star rating and full NLP justification!")
                else:
                    st.error(f"Backend error: {response.text}")
            except Exception as e:
                st.error(f"Failed to communicate with API server: {e}")

    st.markdown(render_footer(), unsafe_allow_html=True)
