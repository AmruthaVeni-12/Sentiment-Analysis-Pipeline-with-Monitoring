import streamlit as st
import requests
import pandas as pd
from src.ui.styles import render_footer

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def render():
    st.markdown("## 🔍 Screen 3: Search Movie & Rating Justification")
    st.markdown("*Retrieve stored reviews, aggregated star ratings, and an AI-synthesized rating justification.*")
    st.markdown("---")

    # Fetch available movies for convenience
    movie_suggestions = []
    try:
        r = requests.get(f"{API_BASE_URL}/movies", timeout=3)
        if r.status_code == 200:
            movie_suggestions = [m["title"] for m in r.json()]
    except Exception:
        # Fallback to direct DB query if API is offline
        try:
            from src.database.session import SessionLocal
            from src.database.models import Movie
            db = SessionLocal()
            movie_suggestions = [m.title for m in db.query(Movie).all()]
            db.close()
        except Exception:
            pass

    search_query = st.text_input(
        "Search movie to get reviews :",
        placeholder="Type a movie title (e.g. Inception, The Dark Knight...)"
    )

    if movie_suggestions:
        st.caption(f"Registered movies in database: {', '.join(movie_suggestions[:8])}")

    if st.button("🔎 Fetch Reviews & Analysis", use_container_width=True) or search_query:
        if not search_query.strip():
            st.warning("Please enter a movie title to search.")
            return

        with st.spinner(f"Analyzing postings for '{search_query}'..."):
            data = None
            try:
                response = requests.get(f"{API_BASE_URL}/reviews/search", params={"title": search_query.strip()}, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                elif response.status_code == 404:
                    st.warning(f"No movie found matching '{search_query}'. Submit a review for this movie in Screen 2 first!")
                    return
            except Exception:
                # Direct DB fallback
                from src.database.session import SessionLocal
                from src.database.models import Movie, Review
                from src.api.justification import generate_rating_justification
                from src.data.preprocessing import LABEL_STARS
                db = SessionLocal()
                try:
                    movie = db.query(Movie).filter(Movie.title.ilike(f"%{search_query.strip()}%")).first()
                    if movie:
                        reviews = db.query(Review).filter(Review.movie_id == movie.id).all()
                        postings = []
                        total_stars = 0
                        review_dicts = []
                        for rev in reviews:
                            s = LABEL_STARS.get(rev.predicted_class, 3)
                            total_stars += s
                            postings.append({
                                "review_id": rev.id,
                                "review_text": rev.review_text,
                                "sentiment_class": rev.predicted_class,
                                "sentiment_label": rev.predicted_label,
                                "star_rating": s,
                                "confidence_score": rev.confidence_score,
                                "created_at": rev.created_at.strftime("%Y-%m-%d %H:%M") if rev.created_at else ""
                            })
                            review_dicts.append({"review_text": rev.review_text, "predicted_label": rev.predicted_label})
                        
                        avg_s = (total_stars / len(reviews)) if reviews else 3.0
                        lbl = "Positive" if avg_s >= 3.5 else ("Negative" if avg_s <= 2.5 else "Neutral")
                        just = generate_rating_justification(
                            movie.title, avg_s, lbl, review_dicts, movie.director_info or "", movie.cast_info or ""
                        )
                        data = {
                            "movie_title": movie.title,
                            "released_year": movie.release_year,
                            "cast": movie.cast_info,
                            "director": movie.director_info,
                            "average_star_rating": round(avg_s, 2),
                            "sentiment_label": lbl,
                            "total_reviews": len(postings),
                            "justification": just,
                            "classified_postings": postings
                        }
                    else:
                        st.warning(f"Movie '{search_query}' not found.")
                        return
                finally:
                    db.close()

            if data:
                # 1. Wireframe Element: Star Rating
                st.markdown(f"### 🎬 {data['movie_title']} {f'({data.get(\"released_year\")})' if data.get('released_year') else ''}")
                
                if data.get("director") or data.get("cast"):
                    meta_bits = []
                    if data.get("director"): meta_bits.append(f"**Director:** {data['director']}")
                    if data.get("cast"): meta_bits.append(f"**Cast:** {data['cast']}")
                    st.caption(" | ".join(meta_bits))

                m1, m2, m3 = st.columns(3)
                with m1:
                    st.metric("Overall Star Rating", f"{data['average_star_rating']} / 5.0", delta=f"{'⭐' * int(round(data['average_star_rating']))}")
                with m2:
                    st.metric("Consensus Sentiment", data["sentiment_label"])
                with m3:
                    st.metric("Total Postings", data["total_reviews"])

                # 2. Wireframe Element: Justification of rating in 4 to 5 sentences
                st.markdown("#### 📜 Justification of Rating (4 to 5 Sentences)")
                st.markdown(f"""
                <div class="justification-box">
                    {data['justification']}
                </div>
                """, unsafe_allow_html=True)

                # 3. Wireframe Element: Classified results of postings
                st.markdown("#### 📊 Classified Results of Postings")
                if data["classified_postings"]:
                    df_postings = pd.DataFrame(data["classified_postings"])
                    df_display = df_postings[["created_at", "star_rating", "sentiment_label", "confidence_score", "review_text"]].copy()
                    df_display.columns = ["Timestamp", "Stars", "Sentiment", "Confidence", "Review Text"]
                    df_display["Stars"] = df_display["Stars"].apply(lambda s: "⭐" * s)
                    df_display["Confidence"] = df_display["Confidence"].apply(lambda c: f"{c * 100:.1f}%")
                    st.dataframe(df_display, use_container_width=True, hide_index=True)
                else:
                    st.info("No individual reviews found for this movie yet.")

    st.markdown(render_footer(), unsafe_allow_html=True)
