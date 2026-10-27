import streamlit as st
import requests
import pandas as pd
from src.ui.styles import render_footer

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def render():
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0;">🔍 Search Film & Rating Justification</h2>
        <p style="color: #cbd5e1; font-size: 1rem; margin: 4px 0 0 0;">
            Query stored movie reviews to view aggregate star ratings, individual critiques, and an AI-generated justification.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch available titles
    movie_suggestions = []
    try:
        r = requests.get(f"{API_BASE_URL}/movies", timeout=3)
        if r.status_code == 200:
            movie_suggestions = [m["title"] for m in r.json()]
    except Exception:
        pass

    col_s1, col_s2 = st.columns([4, 1])
    with col_s1:
        search_query = st.text_input(
            "Search movie to get reviews",
            placeholder="Type a movie title (e.g. Inception, Oppenheimer, The Godfather)...",
            label_visibility="collapsed"
        )
    with col_s2:
        search_btn = st.button("🔎 Search", use_container_width=True)

    if movie_suggestions:
        st.markdown(
            f"<div style='font-size:0.88rem; color:#cbd5e1; margin-top:-6px; margin-bottom:16px;'>"
            f"<b style='color:#ffffff;'>Available Movies:</b> {', '.join(movie_suggestions[:6])}"
            f"</div>",
            unsafe_allow_html=True
        )

    if search_btn or (search_query and len(search_query.strip()) > 1):
        if not search_query.strip():
            st.warning("Please enter a movie title to search.")
            return

        with st.spinner(f"Retrieving critiques and synthesizing justification for '{search_query}'..."):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/reviews/search",
                    params={"title": search_query.strip()},
                    timeout=8
                )
                if response.status_code == 404:
                    st.warning(f"No movie found matching '{search_query}'. Try adding a review in Screen 2 first!")
                    return
                elif response.status_code != 200:
                    st.error(f"Error: {response.text}")
                    return

                data = response.json()
            except Exception as e:
                st.error(f"Failed to connect to API server: {e}")
                return

            year_tag = f"<span class='badge-pill badge-neu' style='margin-left:8px;'>{data['released_year']}</span>" if data.get("released_year") else ""
            
            meta_items = []
            if data.get("director"):
                meta_items.append(f"<b style='color:#ffffff;'>Director:</b> {data['director']}")
            if data.get("cast"):
                meta_items.append(f"<b style='color:#ffffff;'>Cast:</b> {data['cast']}")
            meta_html = f"<div style='color:#cbd5e1; font-size:0.95rem; margin-top:6px;'>{' · '.join(meta_items)}</div>" if meta_items else ""

            badge_class = {
                "Very Negative": "badge-vneg",
                "Negative": "badge-neg",
                "Neutral": "badge-neu",
                "Positive": "badge-pos",
                "Very Positive": "badge-vpos"
            }.get(data["sentiment_label"], "badge-neu")

            st.markdown(f"""
            <div class="app-card" style="margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap;">
                    <div>
                        <h2 style="margin: 0; font-size: 1.7rem; color: #ffffff;">🎬 {data['movie_title']} {year_tag}</h2>
                        {meta_html}
                    </div>
                    <div style="text-align: right;">
                        <span class="badge-pill {badge_class}" style="font-size: 0.95rem !important;">{data['sentiment_label']}</span>
                    </div>
                </div>
                <hr style="border: 0; border-top: 1px solid #24344d; margin: 18px 0;">
                <div style="display: flex; gap: 45px; flex-wrap: wrap;">
                    <div>
                        <span style="color:#cbd5e1; font-size:0.85rem; display:block; font-weight:600;">Overall Star Rating</span>
                        <span style="font-size:1.8rem; font-weight:800; color:#fbbf24;">{'★' * int(round(data['average_star_rating']))}</span>
                        <span style="font-size:1.2rem; color:#ffffff; font-weight:700; margin-left:8px;">{data['average_star_rating']} / 5.0</span>
                    </div>
                    <div>
                        <span style="color:#cbd5e1; font-size:0.85rem; display:block; font-weight:600;">Total Postings Analyzed</span>
                        <span style="font-size:1.8rem; font-weight:800; color:#38bdf8;">{data['total_reviews']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # NLP Justification
            st.markdown("<h3>📜 Rating Justification (4 to 5 Sentences)</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="justification-panel">
                {data['justification']}
            </div>
            """, unsafe_allow_html=True)

            # Classified Postings
            st.markdown("<h3>📊 Classified Results of Postings</h3>", unsafe_allow_html=True)
            if data["classified_postings"]:
                df = pd.DataFrame(data["classified_postings"])
                df_clean = pd.DataFrame({
                    "Date": df["created_at"],
                    "Rating": df["star_rating"].apply(lambda s: "★" * s),
                    "Sentiment": df["sentiment_label"],
                    "Confidence": df["confidence_score"].apply(lambda c: f"{c * 100:.1f}%"),
                    "Review Excerpt": df["review_text"]
                })
                st.dataframe(df_clean, use_container_width=True, hide_index=True)
            else:
                st.info("No individual reviews found for this title.")

    st.markdown(render_footer(), unsafe_allow_html=True)
