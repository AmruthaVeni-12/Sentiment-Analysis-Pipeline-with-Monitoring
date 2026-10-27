from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.database.session import init_db
from src.api.routes import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initializes SQLite database schemas on startup."""
    init_db()
    yield

app = FastAPI(
    title="Movie Sentiment MLOps API",
    description="REST API serving 5-class IMDb sentiment analysis, movie postings, ratings, and NLP justification",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for Streamlit and external access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API router
app.include_router(router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "online",
        "service": "Movie Sentiment Analysis API",
        "endpoints": {
            "sentiments": "/api/v1/sentiments",
            "post_reviews": "/api/v1/reviews/post",
            "search_reviews": "/api/v1/reviews/search",
            "docs": "/docs"
        }
    }

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}
