CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Global App Canvas */
    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
        background-color: #0b111e !important;
        color: #ffffff !important;
    }

    /* Streamlit Container Width & Padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1140px !important;
    }

    /* Clean Header/Footer Removals */
    #MainMenu, footer, header { visibility: hidden !important; }

    /* Sidebar - Deep Matte Navy */
    section[data-testid="stSidebar"] {
        background-color: #080d17 !important;
        border-right: 1px solid #1e293b !important;
    }

    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: #e2e8f0 !important;
        font-size: 0.95rem !important;
    }

    /* Typography Hierarchy - High Contrast White & Off-White */
    h1 {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #ffffff !important;
        letter-spacing: -0.02em !important;
        margin-bottom: 0.6rem !important;
    }

    h2 {
        font-size: 1.65rem !important;
        font-weight: 700 !important;
        color: #ffffff !important;
        letter-spacing: -0.01em !important;
        margin-top: 0.2rem !important;
        margin-bottom: 0.5rem !important;
    }

    h3 {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #f8fafc !important;
        margin-top: 1rem !important;
        margin-bottom: 0.5rem !important;
    }

    p, span, div, label {
        color: #e2e8f0 !important;
        font-size: 1rem !important;
        line-height: 1.65 !important;
    }

    /* Form Labels: Crisp, Bright White */
    .stTextInput label, 
    .stTextArea label, 
    .stNumberInput label,
    .stSelectbox label {
        color: #ffffff !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        margin-bottom: 6px !important;
    }

    /* Inputs: Dark Slate with High Contrast White Text */
    .stTextInput input, 
    .stTextArea textarea, 
    .stNumberInput input {
        background-color: #131c2e !important;
        border: 1.5px solid #2d3d57 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-size: 1rem !important;
        padding: 12px 14px !important;
    }

    .stTextInput input:focus, 
    .stTextArea textarea:focus {
        border-color: #f59e0b !important;
        box-shadow: 0 0 0 2px rgba(245, 158, 11, 0.25) !important;
    }

    /* Solid Unified Cards */
    .app-card {
        background-color: #131c2e !important;
        border: 1px solid #24344d !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.35) !important;
    }

    /* Hero Banner: Gold Accent */
    .hero-box {
        background: linear-gradient(145deg, #162035 0%, #101726 100%) !important;
        border: 1px solid #2e4060 !important;
        border-left: 5px solid #f59e0b !important;
        border-radius: 12px !important;
        padding: 28px !important;
        margin-bottom: 24px !important;
    }

    .gold-accent {
        color: #f59e0b !important;
        font-weight: 800 !important;
    }

    /* Buttons: Bold Cinema Gold that Suited with Deep Navy Canvas */
    .stButton > button {
        background-color: #f59e0b !important;
        color: #0b111e !important;
        border: 1px solid #d97706 !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.2px !important;
        transition: all 0.2s ease-in-out !important;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.25) !important;
    }

    .stButton > button:hover {
        background-color: #fbbf24 !important;
        color: #000000 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 18px rgba(245, 158, 11, 0.4) !important;
    }

    .stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* Sentiment Tier Badges (High Contrast Pills) */
    .tier-box {
        background-color: #131c2e;
        border: 1px solid #24344d;
        border-radius: 10px;
        padding: 16px 10px;
        text-align: center;
    }

    .badge-pill {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.85rem !important;
        margin: 6px 0;
        letter-spacing: 0.3px;
    }

    .badge-vneg { background-color: #7f1d1d; color: #fecaca !important; border: 1px solid #dc2626; }
    .badge-neg  { background-color: #7c2d12; color: #fed7aa !important; border: 1px solid #ea580c; }
    .badge-neu  { background-color: #713f12; color: #fef08a !important; border: 1px solid #ca8a04; }
    .badge-pos  { background-color: #1e3a8a; color: #bfdbfe !important; border: 1px solid #2563eb; }
    .badge-vpos { background-color: #14532d; color: #bbf7d0 !important; border: 1px solid #16a34a; }

    /* Rating Justification Box */
    .justification-panel {
        background-color: #162238;
        border-left: 4px solid #f59e0b;
        border-radius: 8px;
        padding: 22px 24px;
        font-size: 1.05rem !important;
        line-height: 1.8 !important;
        color: #ffffff !important;
        margin: 18px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    /* Clean Footer */
    .clean-footer {
        margin-top: 45px;
        padding-top: 18px;
        border-top: 1px solid #1e293b;
        text-align: center;
        color: #94a3b8 !important;
        font-size: 0.88rem !important;
    }
</style>
"""

def render_footer():
    return """
    <div class="clean-footer">
        🎬 <b>CinePulse</b> · 5-Class Movie Sentiment Platform · Powered by FastAPI & Scikit-Learn
    </div>
    """
