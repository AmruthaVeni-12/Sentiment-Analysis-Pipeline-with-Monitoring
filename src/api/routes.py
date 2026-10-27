import time
import joblib
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.database.models import Movie, Review, DriftLog
from src.data.preprocessing import clean_text, LABEL_MAP, LABEL_STARS
from src.api.schemas import (
    SentimentRequest,
    SentimentResponse,
    ReviewPostRequest,
    ReviewPostResponse,
    MovieSearchResponse,
    ClassifiedPostingItem,
    BatchPredictRequest,
    BatchPredictResponse
)
from src.api.justification import generate_rating_justification

router = APIRouter(prefix="/api/v1", tags=["Sentiment & Reviews"])

SVM_MODEL_PATH = Path("models/svm_pipeline.joblib")
_cached_svm_pipeline = None

def get_svm_pipeline():
    global _cached_svm_pipeline
    if _cached_svm_pipeline is None:
        if SVM_MODEL_PATH.exists():
            _cached_svm_pipeline = joblib.load(SVM_MODEL_PATH)
        else:
            return None
    return _cached_svm_pipeline

def predict_with_svm(cleaned_text: str) -> Dict[str, Any]:
    pipeline = get_svm_pipeline()
    if pipeline is None:
        # Fallback heuristic if training has not completed yet
        return {
            "class": 2,
            "label": "Neutral",
            "stars": 3,
            "confidence": 0.50,
            "probabilities": {LABEL_MAP[i]: 0.20 for i in range(5)}
        }
    
    probs = pipeline.predict_proba([cleaned_text])[0]
    pred_class = int(pipeline.predict([cleaned_text])[0])
    confidence = float(probs[pred_class])
    probabilities = {LABEL_MAP[i]: float(probs[i]) for i in range(5)}
    
    return {
        "class": pred_class,
        "label": LABEL_MAP[pred_class],
        "stars": LABEL_STARS[pred_class],
        "confidence": confidence,
        "probabilities": probabilities
    }

def log_drift_data(text: str, pred_class: int):
    from src.database.session import SessionLocal
    db = SessionLocal()
    try:
        drift_entry = DriftLog(
            review_text=text[:1000],
            predicted_class=pred_class,
            char_length=len(text),
            word_count=len(text.split())
        )
        db.add(drift_entry)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Drift logging warning: {e}")
    finally:
        db.close()

# ----------------- Screen 4: Sentiment Analysis Endpoint -----------------
@router.post("/sentiments", response_model=SentimentResponse)
def analyze_sentiment(
    req: SentimentRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    start_t = time.time()
    clean_txt = clean_text(req.text)
    
    prediction = predict_with_svm(clean_txt)
    latency_ms = round((time.time() - start_t) * 1000, 2)
    
    background_tasks.add_task(log_drift_data, clean_txt, prediction["class"])
    
    return SentimentResponse(
        sentiment_class=prediction["class"],
        sentiment_label=prediction["label"],
        star_rating=prediction["stars"],
        confidence_score=prediction["confidence"],
        probabilities=prediction["probabilities"],
        inference_time_ms=latency_ms
    )

# ----------------- Screen 2: Post Reviews Endpoint -----------------
@router.post("/reviews/post", response_model=ReviewPostResponse)
def post_movie_review(
    req: ReviewPostRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    cleaned_title = req.movie_name.strip()
    clean_review_txt = clean_text(req.about_movie)
    
    # Check or create movie
    movie = db.query(Movie).filter(Movie.title.ilike(cleaned_title)).first()
    if not movie:
        movie = Movie(
            title=cleaned_title,
            release_year=req.released_year,
            cast_info=req.cast,
            director_info=req.direction_and_info
        )
        db.add(movie)
        db.commit()
        db.refresh(movie)
    else:
        # Update metadata if provided and previously empty
        if req.released_year and not movie.release_year:
            movie.release_year = req.released_year
        if req.cast and not movie.cast_info:
            movie.cast_info = req.cast
        if req.direction_and_info and not movie.director_info:
            movie.director_info = req.direction_and_info
        db.commit()
    
    # Run sentiment analysis
    prediction = predict_with_svm(clean_review_txt)
    
    # Save review record
    review_record = Review(
        movie_id=movie.id,
        review_text=clean_review_txt,
        predicted_class=prediction["class"],
        predicted_label=prediction["label"],
        confidence_score=prediction["confidence"],
        model_name="svm_baseline"
    )
    db.add(review_record)
    db.commit()
    db.refresh(review_record)
    
    # Background drift log
    background_tasks.add_task(log_drift_data, clean_review_txt, prediction["class"])
    
    return ReviewPostResponse(
        movie_id=movie.id,
        review_id=review_record.id,
        movie_title=movie.title,
        sentiment_class=prediction["class"],
        sentiment_label=prediction["label"],
        star_rating=prediction["stars"],
        confidence_score=prediction["confidence"],
        message=f"Review successfully analyzed and registered for '{movie.title}'!"
    )

# ----------------- Screen 3: Search Movie & Reviews Endpoint -----------------
@router.get("/reviews/search", response_model=MovieSearchResponse)
def search_movie_reviews(
    title: str = Query(..., min_length=1, description="Movie title to search"),
    db: Session = Depends(get_db)
):
    cleaned_title = title.strip()
    movie = db.query(Movie).filter(Movie.title.ilike(f"%{cleaned_title}%")).first()
    
    if not movie:
        raise HTTPException(
            status_code=404,
            detail=f"No movie found matching title '{title}'. Please check spelling or submit reviews in Screen 2."
        )
    
    reviews = db.query(Review).filter(Review.movie_id == movie.id).order_by(Review.created_at.desc()).all()
    
    postings = []
    total_stars = 0
    review_dicts = []
    
    for r in reviews:
        star_val = LABEL_STARS.get(r.predicted_class, 3)
        total_stars += star_val
        item = ClassifiedPostingItem(
            review_id=r.id,
            review_text=r.review_text,
            sentiment_class=r.predicted_class,
            sentiment_label=r.predicted_label,
            star_rating=star_val,
            confidence_score=r.confidence_score,
            created_at=r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else ""
        )
        postings.append(item)
        review_dicts.append({"review_text": r.review_text, "predicted_label": r.predicted_label})
    
    avg_stars = (total_stars / len(reviews)) if reviews else 3.0
    
    # Map avg_stars to overall sentiment label
    if avg_stars <= 1.8:
        overall_label = "Very Negative"
    elif avg_stars <= 2.6:
        overall_label = "Negative"
    elif avg_stars <= 3.4:
        overall_label = "Neutral"
    elif avg_stars <= 4.2:
        overall_label = "Positive"
    else:
        overall_label = "Very Positive"
        
    justification = generate_rating_justification(
        movie_title=movie.title,
        star_rating=avg_stars,
        sentiment_label=overall_label,
        reviews=review_dicts,
        director=movie.director_info or "",
        cast=movie.cast_info or ""
    )
    
    return MovieSearchResponse(
        movie_title=movie.title,
        released_year=movie.release_year,
        cast=movie.cast_info,
        director=movie.director_info,
        average_star_rating=round(avg_stars, 2),
        sentiment_label=overall_label,
        total_reviews=len(postings),
        justification=justification,
        classified_postings=postings
    )

# ----------------- Helper: List All Movies -----------------
@router.get("/movies")
def list_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).order_by(Movie.title.asc()).all()
    return [{"id": m.id, "title": m.title, "year": m.release_year} for m in movies]

# ----------------- Drift & Monitoring Endpoint -----------------
@router.get("/monitoring/drift")
def trigger_drift_analysis():
    from src.monitoring.drift import generate_drift_report
    report_summary = generate_drift_report()
    return report_summary
