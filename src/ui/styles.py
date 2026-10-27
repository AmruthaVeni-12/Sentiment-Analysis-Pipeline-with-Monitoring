CUSTOM_CSS = """
<style>
    /* Main container styling */
    .main {
        background-color: #0e1117;
        color: #fafafa;
    }
    
    /* Card design */
    .metric-card {
        background: linear-gradient(135deg, #1e222d 0%, #262c3a 100%);
        border: 1px solid #363c4e;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }
    
    .rating-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    .badge-very-pos { background-color: #1b5e20; color: #a5d6a7; border: 1px solid #2e7d32; }
    .badge-pos      { background-color: #1565c0; color: #90caf9; border: 1px solid #1976d2; }
    .badge-neutral  { background-color: #e65100; color: #ffcc80; border: 1px solid #f57c00; }
    .badge-neg      { background-color: #ad1457; color: #f48fb1; border: 1px solid #c2185b; }
    .badge-very-neg { background-color: #b71c1c; color: #ef9a9a; border: 1px solid #d32f2f; }

    .justification-box {
        background: #141b2d;
        border-left: 5px solid #00d2ff;
        border-radius: 8px;
        padding: 18px 24px;
        font-size: 1.05rem;
        line-height: 1.7;
        color: #e2e8f0;
        margin: 15px 0;
    }
    
    .footer-container {
        margin-top: 50px;
        padding: 20px 0;
        border-top: 1px solid #2d3748;
        text-align: center;
        color: #718096;
        font-size: 0.85rem;
    }
</style>
"""

def render_footer():
    return """
    <div class="footer-container">
        🎬 <b>Movie Sentiment Intelligence Platform</b> | MLOps Pipeline with DVC, MLflow, FastAPI & Evidently AI
    </div>
    """
