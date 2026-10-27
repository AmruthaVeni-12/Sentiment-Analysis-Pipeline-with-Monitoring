from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    release_year = Column(Integer, nullable=True)
    cast_info = Column(String(500), nullable=True)
    director_info = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    reviews = relationship("Review", back_populates="movie", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False, index=True)
    review_text = Column(Text, nullable=False)
    predicted_class = Column(Integer, nullable=False)   # 0 to 4
    predicted_label = Column(String(50), nullable=False) # e.g. "Positive"
    confidence_score = Column(Float, nullable=False)
    model_name = Column(String(100), default="svm_baseline")
    created_at = Column(DateTime, default=datetime.utcnow)

    movie = relationship("Movie", back_populates="reviews")


class DriftLog(Base):
    __tablename__ = "drift_logs"

    id = Column(Integer, primary_key=True, index=True)
    review_text = Column(Text, nullable=False)
    predicted_class = Column(Integer, nullable=False)
    char_length = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
