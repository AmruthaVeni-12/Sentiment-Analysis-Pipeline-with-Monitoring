import streamlit as st
import requests
from src.ui.styles import render_footer

API_BASE_URL = "http://127.0.0.1:8000/api/v1"

def render():
    st.markdown("## 📝 Screen 2: Movie Review Postings")
    st.markdown("*Register movie details and submit your review for automated NLP sentiment classification.*")
    st.markdown("---")

    with st.form("posting_form"):
        st.subheader("Film Metadata & Review Submission")
        
        movie_name = st.text_input("Movie Name :", placeholder="e.g. Inception, Oppenheimer, The Godfather")
        
        col_meta1, col_meta2 = st.columns(2)
        with col_meta1:
            released_year = st.number_input("Released Year :", min_value=1900, max_value=2030, value=2023, step=1)
        with col_meta2:
            cast = st.text_input("Cast :", placeholder="e.g. Cillian Murphy, Emily Blunt, Matt Damon")
            
        direction_info = st.text_input("Direction & Additional Info :", placeholder="e.g. Directed by Christopher Nolan, IMAX 70mm cinematography")
        
        about_movie = st.text_area(
            "About Movie (in 3 to 4 lines) :",
            height=120,
            placeholder="Write your movie review here (e.g. 'Phenomenal performances and a gripping musical score that kept me on the edge of my seat...')"
        )
        
        submit_btn = st.form_submit_button("🚀 Submit Posting & Classify Sentiment", use_container_width=True)

    if submit_btn:
        if not movie_name.strip():
            st.error("Please provide a valid Movie Name.")
            return
        if not about_movie.strip() or len(about_movie.strip()) < 5:
            st.error("Please enter a review description of at least 3 to 4 lines (minimum 10 characters).")
            return

        payload = {
            "movie_name": movie_name.strip(),
            "released_year": int(released_year),
            "cast": cast.strip() if cast else None,
            "direction_and_info": direction_info.strip() if direction_info else None,
            "about_movie": about_movie.strip()
        }

        with st.spinner("Classifying sentiment and registering to database..."):
            try:
                response = requests.post(f"{API_BASE_URL}/reviews/post", json=payload, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    st.success(f"✅ {data['message']}")
                    
                    # Result card
                    st.markdown("""
                    <div class="metric-card">
                        <h4>🎯 Automated Classification Result</h4>
                    """, unsafe_allow_html=True)
                    
                    res_col1, res_col2, res_col3 = st.columns(3)
                    with res_col1:
                        st.metric("Assigned Rating", "⭐" * data["star_rating"])
                    with res_col2:
                        st.metric("Sentiment Class", data["sentiment_label"])
                    with res_col3:
                        st.metric("Confidence Score", f"{data['confidence_score'] * 100:.1f}%")
                        
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.info("💡 You can now search for this movie in **Screen 3** to see the aggregated star rating and full NLP justification!")
                else:
                    st.error(f"Backend API error: {response.text}")
            except requests.exceptions.ConnectionError:
                # Local fallback if API server is not running separately
                from src.database.session import SessionLocal
                from src.database.models import Movie, Review, DriftLog
                from src.api.routes import predict_with_svm, clean_text
                
                db = SessionLocal()
                try:
                    movie = db.query(Movie).filter(Movie.title.ilike(movie_name.strip())).first()
                    if not movie:
                        movie = Movie(
                            title=movie_name.strip(),
                            release_year=int(released_year),
                            cast_info=cast.strip() if cast else None,
                            director_info=direction_info.strip() if direction_info else None
                        )
                        db.add(movie)
                        db.commit()
                        db.refresh(movie)
                    
                    cleaned_txt = clean_text(about_movie)
                    pred = predict_with_svm(cleaned_txt)
                    
                    rev = Review(
                        movie_id=movie.id,
                        review_text=cleaned_txt,
                        predicted_class=pred["class"],
                        predicted_label=pred["label"],
                        confidence_score=pred["confidence"],
                        model_name="svm_baseline"
                    )
                    db.add(rev)
                    db.commit()
                    
                    st.success(f"✅ Review successfully registered locally for '{movie.title}'!")
                    st.metric("Assigned Rating", f"{'⭐' * pred['stars']} ({pred['label']})")
                finally:
                    db.close()

    st.markdown(render_footer(), unsafe_allow_html=True)
