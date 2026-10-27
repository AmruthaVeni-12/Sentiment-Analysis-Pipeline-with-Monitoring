from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field

class SentimentRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Movie review text to analyze")
    model_type: Optional[str] = Field("svm_baseline", description="Model identifier: 'svm_baseline' or 'distilbert'")

class SentimentResponse(BaseModel):
    sentiment_class: int = Field(..., description="Predicted class index (0 to 4)")
    sentiment_label: str = Field(..., description="Label ('Very Negative' to 'Very Positive')")
    star_rating: int = Field(..., description="Corresponding star rating (1 to 5 stars)")
    confidence_score: float = Field(..., description="Predicted probability of the chosen class")
    probabilities: Dict[str, float] = Field(..., description="Class probability distribution")
    inference_time_ms: float = Field(..., description="Latency in milliseconds")

class ReviewPostRequest(BaseModel):
    movie_name: str = Field(..., min_length=1, description="Title of the movie")
    released_year: Optional[int] = Field(None, ge=1880, le=2100, description="Release year")
    cast: Optional[str] = Field(None, description="Key cast members")
    direction_and_info: Optional[str] = Field(None, description="Director and additional film info")
    about_movie: str = Field(..., min_length=5, description="User's review text (3 to 4 lines)")

class ReviewPostResponse(BaseModel):
    movie_id: int
    review_id: int
    movie_title: str
    sentiment_class: int
    sentiment_label: str
    star_rating: int
    confidence_score: float
    message: str

class ClassifiedPostingItem(BaseModel):
    review_id: int
    review_text: str
    sentiment_class: int
    sentiment_label: str
    star_rating: int
    confidence_score: float
    created_at: str

class MovieSearchResponse(BaseModel):
    movie_title: str
    released_year: Optional[int]
    cast: Optional[str]
    director: Optional[str]
    average_star_rating: float
    sentiment_label: str
    total_reviews: int
    justification: str
    classified_postings: List[ClassifiedPostingItem]

class BatchPredictRequest(BaseModel):
    texts: List[str]

class BatchPredictResponse(BaseModel):
    total: int
    predictions: List[SentimentResponse]
