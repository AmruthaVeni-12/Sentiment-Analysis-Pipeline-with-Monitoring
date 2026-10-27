import pytest
from fastapi import BackgroundTasks
from src.database.session import SessionLocal, init_db
from src.api.main import root, health
from src.api.routes import analyze_sentiment, post_movie_review, search_movie_reviews
from src.api.schemas import SentimentRequest, ReviewPostRequest

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    init_db()

def test_health():
    res = health()
    assert res == {"status": "healthy"}

def test_root():
    res = root()
    assert res["status"] == "online"
    assert "endpoints" in res

def test_analyze_sentiment():
    db = SessionLocal()
    bg = BackgroundTasks()
    try:
        req = SentimentRequest(
            text="An extraordinary film with breathtaking cinematography and powerful acting!",
            model_type="svm_baseline"
        )
        res = analyze_sentiment(req, bg, db)
        assert 0 <= res.sentiment_class <= 4
        assert res.sentiment_label in ["Very Negative", "Negative", "Neutral", "Positive", "Very Positive"]
        assert res.star_rating in [1, 2, 3, 4, 5]
        assert len(res.probabilities) == 5
    finally:
        db.close()

def test_post_and_search_reviews():
    db = SessionLocal()
    bg = BackgroundTasks()
    try:
        post_req = ReviewPostRequest(
            movie_name="Inception Unit Test",
            released_year=2010,
            cast="Leonardo DiCaprio, Joseph Gordon-Levitt",
            direction_and_info="Directed by Christopher Nolan",
            about_movie="A stunning masterpiece of storytelling, mind-bending concepts and phenomenal direction."
        )
        post_res = post_movie_review(post_req, bg, db)
        assert post_res.movie_title == "Inception Unit Test"
        assert post_res.star_rating >= 1

        search_res = search_movie_reviews(title="Inception Unit Test", db=db)
        assert search_res.movie_title == "Inception Unit Test"
        assert search_res.total_reviews >= 1
        assert len(search_res.justification) > 50
        assert len(search_res.classified_postings) >= 1
    finally:
        db.close()
