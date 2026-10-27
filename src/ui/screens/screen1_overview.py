import streamlit as st
import pandas as pd
from src.ui.styles import render_footer
from src.database.session import SessionLocal
from src.database.models import Movie, Review, DriftLog
from src.data.preprocessing import LABEL_MAP, LABEL_STARS

def get_platform_metrics():
    """Queries real live platform data from the persistent SQLite database."""
    db = SessionLocal()
    try:
        total_movies = db.query(Movie).count()
        total_reviews = db.query(Review).count()
        drift_count = db.query(DriftLog).count()

        reviews = db.query(Review).all()
        if reviews:
            avg_stars = sum([LABEL_STARS.get(r.predicted_class, 3) for r in reviews]) / len(reviews)
            recent_reviews = [
                {
                    "Movie": r.movie.title if r.movie else "Unknown",
                    "Rating": "★" * LABEL_STARS.get(r.predicted_class, 3),
                    "Sentiment": r.predicted_label,
                    "Confidence": f"{r.confidence_score * 100:.1f}%",
                    "Review": r.review_text[:110] + ("..." if len(r.review_text) > 110 else "")
                } for r in reviews[-5:]
            ]
        else:
            avg_stars = 0.0
            recent_reviews = []

        return {
            "total_movies": total_movies,
            "total_reviews": total_reviews,
            "avg_stars": avg_stars,
            "drift_count": drift_count,
            "recent_reviews": recent_reviews
        }
    except Exception:
        return {
            "total_movies": 0,
            "total_reviews": 0,
            "avg_stars": 0.0,
            "drift_count": 0,
            "recent_reviews": []
        }
    finally:
        db.close()

def render():
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h1 class="page-title">🎬 CinePulse Intelligence Dashboard</h1>
        <p class="page-subtitle">
            Enterprise sentiment classification & MLOps platform for film critique analysis. Transforming raw subjective natural language into structured 5-star evaluation metrics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Real Live KPI Grid
    metrics = get_platform_metrics()

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Reviews Analyzed</div>
            <div class="kpi-value">{metrics['total_reviews']}</div>
            <div class="kpi-sub" style="color:#8B5CF6;">Stored in SQLite</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Films Cataloged</div>
            <div class="kpi-value">{metrics['total_movies']}</div>
            <div class="kpi-sub" style="color:#22D3EE;">Active titles</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        star_display = f"{metrics['avg_stars']:.1f} / 5.0" if metrics['total_reviews'] > 0 else "N/A"
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Average Sentiment Score</div>
            <div class="kpi-value" style="color:#F59E0B;">{star_display}</div>
            <div class="kpi-sub" style="color:#94A3B8;">Across database</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-label">Active Inference Engine</div>
            <div class="kpi-value" style="font-size:1.35rem; color:#10B981;">Online</div>
            <div class="kpi-sub" style="color:#94A3B8;">Calibrated LinearSVC (~2ms)</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # 5-Tier Sentiment Spectrum Guide
    st.markdown("<h3>⭐ Calibrated 5-Class Sentiment Hierarchy</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color:#94A3B8; font-size:0.92rem; margin-bottom: 16px;'>CinePulse maps natural language movie reviews into 5 calibrated ordinal classes derived from IMDb star ratings:</p>", unsafe_allow_html=True)

    t1, t2, t3, t4, t5 = st.columns(5)
    with t1:
        st.markdown("""
        <div class="saas-card" style="padding:16px 12px; text-align:center; border-top:3px solid #EF4444; height:100%;">
            <div style="font-weight:700; color:#EF4444; font-size:0.95rem;">★ 1 Star</div>
            <span class="sentiment-badge badge-vneg">Very Negative</span>
            <div style="font-size:0.8rem; color:#94A3B8; margin-top:8px; line-height:1.4;">Unwatchable, critical failure, atrocious script.</div>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div class="saas-card" style="padding:16px 12px; text-align:center; border-top:3px solid #F97316; height:100%;">
            <div style="font-weight:700; color:#F97316; font-size:0.95rem;">★★ 2 Stars</div>
            <span class="sentiment-badge badge-neg">Negative</span>
            <div style="font-size:0.8rem; color:#94A3B8; margin-top:8px; line-height:1.4;">Weak pacing, formulaic, misses expectations.</div>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div class="saas-card" style="padding:16px 12px; text-align:center; border-top:3px solid #F59E0B; height:100%;">
            <div style="font-weight:700; color:#F59E0B; font-size:0.95rem;">★★★ 3 Stars</div>
            <span class="sentiment-badge badge-neu">Neutral</span>
            <div style="font-size:0.8rem; color:#94A3B8; margin-top:8px; line-height:1.4;">Standard popcorn flick, mixed audience reception.</div>
        </div>
        """, unsafe_allow_html=True)
    with t4:
        st.markdown("""
        <div class="saas-card" style="padding:16px 12px; text-align:center; border-top:3px solid #22D3EE; height:100%;">
            <div style="font-weight:700; color:#22D3EE; font-size:0.95rem;">★★★★ 4 Stars</div>
            <span class="sentiment-badge badge-pos">Positive</span>
            <div style="font-size:0.8rem; color:#94A3B8; margin-top:8px; line-height:1.4;">Strong performance, thoughtful storytelling.</div>
        </div>
        """, unsafe_allow_html=True)
    with t5:
        st.markdown("""
        <div class="saas-card" style="padding:16px 12px; text-align:center; border-top:3px solid #10B981; height:100%;">
            <div style="font-weight:700; color:#10B981; font-size:0.95rem;">★★★★★ 5 Stars</div>
            <span class="sentiment-badge badge-vpos">Very Positive</span>
            <div style="font-size:0.8rem; color:#94A3B8; margin-top:8px; line-height:1.4;">Cinematic masterpiece, profound emotional depth.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 25px;'></div>", unsafe_allow_html=True)

    # Recent Activity Table
    st.markdown("<h3>📋 Recent Analysis Activity</h3>", unsafe_allow_html=True)
    if metrics["recent_reviews"]:
        df_recent = pd.DataFrame(metrics["recent_reviews"])
        st.dataframe(df_recent, use_container_width=True, hide_index=True)
    else:
        st.markdown("""
        <div class="saas-card" style="text-align:center; padding:30px;">
            <div style="font-size:1.5rem; margin-bottom:6px;">📭</div>
            <div style="font-weight:600; color:#F8FAFC;">No reviews registered in the database yet</div>
            <div style="font-size:0.88rem; color:#94A3B8; margin-top:4px;">Navigate to <b>Post Movie Review</b> in the sidebar to analyze and catalog your first film.</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(render_footer(), unsafe_allow_html=True)
