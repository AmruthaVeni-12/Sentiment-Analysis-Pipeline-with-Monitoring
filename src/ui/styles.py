CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #0b0f19 !important;
        color: #f1f5f9 !important;
    }

    /* Reduce default Streamlit top blank padding */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
        max-width: 1200px !important;
    }

    /* Hide Streamlit footer & default menu clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #0f172a !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    }
    
    section[data-testid="stSidebar"] .stRadio label {
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        padding: 6px 12px !important;
        border-radius: 8px !important;
        transition: all 0.2s ease !important;
    }

    /* Headings */
    h1 {
        font-size: 2.1rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        color: #ffffff !important;
        margin-bottom: 0.5rem !important;
    }

    h2 {
        font-size: 1.6rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        color: #f8fafc !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.75rem !important;
    }

    h3 {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        color: #e2e8f0 !important;
    }

    p, span, label {
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }

    /* Cards */
    .glass-card {
        background: rgba(17, 24, 39, 0.75) !important;
        backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 14px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4) !important;
    }

    .hero-banner {
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        border: 1px solid rgba(99, 102, 241, 0.25) !important;
        border-radius: 16px !important;
        padding: 30px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 12px 30px -10px rgba(99, 102, 241, 0.15) !important;
    }

    .gradient-text {
        background: linear-gradient(135deg, #60a5fa 0%, #a855f7 50%, #ec4899 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        display: inline-block;
    }

    /* Sentiment Tier Badges */
    .tier-card {
        border-radius: 12px;
        padding: 16px 12px;
        text-align: center;
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .tier-card:hover {
        transform: translateY(-2px);
    }
    
    .tier-title {
        font-weight: 700;
        font-size: 0.95rem;
        margin-bottom: 4px;
    }

    .tier-desc {
        font-size: 0.78rem !important;
        color: #94a3b8;
        line-height: 1.4 !important;
        margin-top: 6px;
    }

    .pill-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.82rem !important;
        letter-spacing: 0.3px;
    }

    .pill-vneg { background: rgba(239, 68, 68, 0.15); color: #fca5a5; border: 1px solid rgba(239, 68, 68, 0.3); }
    .pill-neg  { background: rgba(249, 115, 22, 0.15); color: #fdba74; border: 1px solid rgba(249, 115, 22, 0.3); }
    .pill-neu  { background: rgba(234, 179, 8, 0.15);  color: #fde047; border: 1px solid rgba(234, 179, 8, 0.3); }
    .pill-pos  { background: rgba(59, 130, 246, 0.15); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.3); }
    .pill-vpos { background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.3); }

    /* Justification Box */
    .justification-card {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.8) 100%);
        border-left: 4px solid #38bdf8;
        border-radius: 12px;
        padding: 22px 26px;
        font-size: 1rem !important;
        line-height: 1.8 !important;
        color: #f1f5f9;
        margin: 18px 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }

    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border-radius: 10px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
    }

    .stButton > button:hover {
        opacity: 0.92 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
    }

    /* Inputs */
    .stTextInput > div > div > input, 
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 10px !important;
        color: #f8fafc !important;
        font-size: 0.95rem !important;
        padding: 10px 14px !important;
    }

    .stTextInput > div > div > input:focus, 
    .stTextArea > div > div > textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2) !important;
    }

    /* Clean Footer */
    .app-footer {
        margin-top: 45px;
        padding-top: 18px;
        border-top: 1px solid rgba(255, 255, 255, 0.08);
        text-align: center;
        color: #64748b;
        font-size: 0.82rem;
    }
</style>
"""

def render_footer():
    return """
    <div class="app-footer">
        🎬 <b>CinePulse</b> · 5-Class Movie Sentiment Platform · Powered by FastAPI & Scikit-Learn
    </div>
    """
