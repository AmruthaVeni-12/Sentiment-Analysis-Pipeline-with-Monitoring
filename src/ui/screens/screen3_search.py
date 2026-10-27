import streamlit as st
import requests
import pandas as pd
from src.ui.styles import render_footer

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def render():
    st.markdown("""
    <div style="margin-bottom: 22px;">
        <h1 class="page-title">Explore Movie Sentiment</h1>
        <p class="page-subtitle">
            Search stored audience critiques, aggregated star ratings, and natural language sentiment justifications powered by the CinePulse inference engine.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Fetch available titles from database
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
        search_btn = st.button("🔎 Search Film", use_container_width=True)

    if movie_suggestions:
        st.markdown(
            f"<div style='font-size:0.86rem; color:#94A3B8; margin-top:-6px; margin-bottom:18px;'>"
            f"<span style='color:#CBD5E1; font-weight:600;'>Cataloged Titles:</span> {', '.join(movie_suggestions[:7])}"
            f"</div>",
            unsafe_allow_html=True
        )

    if search_btn or (search_query and len(search_query.strip()) > 1):
        if not search_query.strip():
            st.warning("Please enter a film title to search.")
            return

        with st.spinner(f"Querying reviews and synthesizing justification for '{search_query}'..."):
            try:
                response = requests.get(
                    f"{API_BASE_URL}/reviews/search",
                    params={"title": search_query.strip()},
                    timeout=8
                )
                if response.status_code == 404:
                    st.warning(f"No movie found matching '{search_query}'. Submit a review in 'Post Movie Review' to create this film's record!")
                    return
                elif response.status_code != 200:
                    st.error(f"Error: {response.text}")
                    return

                data = response.json()
            except Exception as e:
                st.error(f"Failed to connect to backend server: {e}")
                return

            year_tag = f"<span class='sentiment-badge badge-neu' style='font-size:0.8rem; margin-left:8px;'>{data['released_year']}</span>" if data.get("released_year") else ""
            
            meta_items = []
            if data.get("director"):
                meta_items.append(f"<span style='color:#F8FAFC;'>Director:</span> {data['director']}")
            if data.get("cast"):
                meta_items.append(f"<span style='color:#F8FAFC;'>Cast:</span> {data['cast']}")
            meta_html = f"<div style='color:#94A3B8; font-size:0.92rem; margin-top:6px;'>{' · '.join(meta_items)}</div>" if meta_items else ""

            badge_class = {
                "Very Negative": "badge-vneg",
                "Negative": "badge-neg",
                "Neutral": "badge-neu",
                "Positive": "badge-pos",
                "Very Positive": "badge-vpos"
            }.get(data["sentiment_label"], "badge-neu")

            # Structured Film Card
            st.markdown(f"""
            <div class="saas-card" style="margin-top: 15px;">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 10px;">
                    <div>
                        <h2 style="margin: 0; font-size: 1.65rem; color: #F8FAFC;">🎬 {data['movie_title']} {year_tag}</h2>
                        {meta_html}
                    </div>
                    <div style="text-align: right;">
                        <span class="sentiment-badge {badge_class}" style="font-size: 0.95rem !important;">{data['sentiment_label']}</span>
                    </div>
                </div>
                <hr style="border: 0; border-top: 1px solid #1E293B; margin: 18px 0;">
                <div style="display: flex; gap: 48px; flex-wrap: wrap;">
                    <div>
                        <span style="color:#94A3B8; font-size:0.82rem; display:block; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">Aggregate Star Rating</span>
                        <span style="font-size:1.75rem; font-weight:800; color:#F59E0B;">{'★' * int(round(data['average_star_rating']))}</span>
                        <span style="font-size:1.15rem; color:#F8FAFC; font-weight:700; margin-left:6px;">{data['average_star_rating']} / 5.0</span>
                    </div>
                    <div>
                        <span style="color:#94A3B8; font-size:0.82rem; display:block; font-weight:600; text-transform:uppercase; letter-spacing:0.5px;">Audience Critiques</span>
                        <span style="font-size:1.75rem; font-weight:800; color:#22D3EE;">{data['total_reviews']}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # AI Rating Justification Panel
            st.markdown("<h3>📜 AI-Generated Rating Justification</h3>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="justification-card">
                {data['justification']}
            </div>
            """, unsafe_allow_html=True)

            # Classified Postings
            st.markdown("<h3>📊 Classified Audience Critiques</h3>", unsafe_allow_html=True)
            if data["classified_postings"]:
                df = pd.DataFrame(data["classified_postings"])
                df_clean = pd.DataFrame({
                    "Timestamp": df["created_at"],
                    "Rating": df["star_rating"].apply(lambda s: "★" * s),
                    "Sentiment": df["sentiment_label"],
                    "Confidence": df["confidence_score"].apply(lambda c: f"{c * 100:.1f}%"),
                    "Critique Excerpt": df["review_text"]
                })
                st.dataframe(df_clean, use_container_width=True, hide_index=True)
            else:
                st.info("No individual reviews found for this title.")

    st.markdown(render_footer(), unsafe_allow_html=True)
