CUSTOM_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    /* -------------------------------------------------------------
       1. GLOBAL RESET & BASE CANVAS
       Main Background: #0B1120 | Text: #F8FAFC | Font: Inter
       ------------------------------------------------------------- */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        background-color: #0B1120 !important;
        color: #F8FAFC !important;
    }

    /* Container constraints & comfortable vertical rhythm */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 3.5rem !important;
        max-width: 1160px !important;
    }

    /* Clean Streamlit default decoration removal */
    #MainMenu, footer, header { visibility: hidden !important; }

    /* -------------------------------------------------------------
       2. SIDEBAR NAVIGATION (#101A2C)
       ------------------------------------------------------------- */
    section[data-testid="stSidebar"] {
        background-color: #101A2C !important;
        border-right: 1px solid #1E293B !important;
    }

    /* Sidebar brand container */
    .sidebar-brand {
        padding: 14px 12px 20px 12px;
        border-bottom: 1px solid #1E293B;
        margin-bottom: 20px;
    }

    .brand-title {
        font-size: 1.35rem;
        font-weight: 800;
        color: #F8FAFC;
        letter-spacing: -0.02em;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .brand-badge {
        font-size: 0.68rem;
        background: rgba(139, 92, 246, 0.2);
        color: #A78BFA;
        border: 1px solid rgba(139, 92, 246, 0.4);
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-left: 6px;
    }

    .brand-sub {
        font-size: 0.82rem;
        color: #94A3B8;
        margin-top: 4px;
        font-weight: 400;
    }

    /* Sidebar Radio Navigation items - SaaS Polish */
    section[data-testid="stSidebar"] .stRadio > div {
        gap: 6px !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        background-color: transparent !important;
        border-radius: 8px !important;
        padding: 10px 14px !important;
        margin-bottom: 2px !important;
        color: #CBD5E1 !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        transition: all 0.15s ease-in-out !important;
        display: flex !important;
        align-items: center !important;
        border: 1px solid transparent !important;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.04) !important;
        color: #F8FAFC !important;
        border-color: rgba(255, 255, 255, 0.08) !important;
    }

    /* Active Radio button item state */
    section[data-testid="stSidebar"] .stRadio label[data-checked="true"],
    section[data-testid="stSidebar"] .stRadio div[aria-checked="true"] {
        background-color: rgba(139, 92, 246, 0.15) !important;
        color: #F8FAFC !important;
        font-weight: 600 !important;
        border: 1px solid rgba(139, 92, 246, 0.4) !important;
    }

    /* -------------------------------------------------------------
       3. TYPOGRAPHY HIERARCHY
       Titles: 26-32px | Subheadings: 18-22px | Body: 14-16px
       ------------------------------------------------------------- */
    h1, .page-title {
        font-size: 1.85rem !important;
        font-weight: 800 !important;
        color: #F8FAFC !important;
        letter-spacing: -0.025em !important;
        margin-bottom: 0.35rem !important;
        line-height: 1.25 !important;
    }

    h2, .section-heading {
        font-size: 1.35rem !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        letter-spacing: -0.015em !important;
        margin-top: 0.6rem !important;
        margin-bottom: 0.5rem !important;
    }

    h3 {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #F8FAFC !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.4rem !important;
    }

    p, span, div {
        color: #CBD5E1 !important;
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }

    .page-subtitle {
        color: #94A3B8 !important;
        font-size: 0.98rem !important;
        margin-bottom: 1.5rem !important;
        line-height: 1.5 !important;
    }

    /* -------------------------------------------------------------
       4. CARDS & SURFACES (#151F32 & #1C2940)
       ------------------------------------------------------------- */
    .saas-card {
        background-color: #151F32 !important;
        border: 1px solid #1E293B !important;
        border-radius: 12px !important;
        padding: 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4) !important;
    }

    .saas-card-elevated {
        background-color: #1C2940 !important;
        border: 1px solid #293952 !important;
        border-radius: 12px !important;
        padding: 22px !important;
        margin-bottom: 20px !important;
    }

    /* Metric & KPI Cards */
    .kpi-card {
        background-color: #151F32;
        border: 1px solid #1E293B;
        border-radius: 10px;
        padding: 18px 20px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        transition: transform 0.15s ease, border-color 0.15s ease;
    }
    
    .kpi-card:hover {
        border-color: #334155;
        transform: translateY(-2px);
    }

    .kpi-label {
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
        color: #94A3B8 !important;
        margin-bottom: 6px !important;
    }

    .kpi-value {
        font-size: 1.75rem !important;
        font-weight: 800 !important;
        color: #F8FAFC !important;
        line-height: 1.2 !important;
    }

    .kpi-sub {
        font-size: 0.8rem !important;
        color: #22D3EE !important;
        margin-top: 6px !important;
        font-weight: 500 !important;
    }

    /* -------------------------------------------------------------
       5. FORM INPUTS & LABELS (#1C2940 surface)
       ------------------------------------------------------------- */
    /* Hide Streamlit default input instructions ("Press Enter to submit form" / "Press Ctrl+Enter") */
    [data-testid="InputInstructions"],
    div[data-testid="InputInstructions"],
    span[data-testid="InputInstructions"],
    .stInputInstructions,
    small:has(span) {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0px !important;
        width: 0px !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: none !important;
    }

    .stTextInput label, 
    .stTextArea label, 
    .stNumberInput label,
    .stSelectbox label {
        color: #F8FAFC !important;
        font-size: 0.92rem !important;
        font-weight: 600 !important;
        margin-bottom: 6px !important;
    }

    /* Container wrappers for input elements */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    div[data-testid="stNumberInputContainer"] {
        background-color: #1C2940 !important;
        border: 1px solid #293952 !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    .stTextInput input, 
    .stTextArea textarea, 
    .stNumberInput input {
        background-color: #1C2940 !important;
        border: 1px solid #293952 !important;
        border-radius: 8px !important;
        color: #F8FAFC !important;
        font-size: 0.95rem !important;
        padding: 12px 14px !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }

    /* Seamless number input step buttons */
    .stNumberInput div[data-baseweb="input"] input {
        border: none !important;
    }

    .stNumberInput button,
    div[data-testid="stNumberInputContainer"] button {
        background-color: #24354D !important;
        color: #CBD5E1 !important;
        border: none !important;
        border-left: 1px solid #293952 !important;
        transition: background 0.15s ease, color 0.15s ease !important;
    }

    .stNumberInput button:hover,
    div[data-testid="stNumberInputContainer"] button:hover {
        background-color: #334B6C !important;
        color: #F8FAFC !important;
    }

    .stNumberInput button svg,
    div[data-testid="stNumberInputContainer"] button svg {
        fill: #CBD5E1 !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #64748B !important;
        font-size: 0.92rem !important;
    }

    .stTextInput input:focus, 
    .stTextArea textarea:focus,
    .stNumberInput input:focus,
    div[data-baseweb="input"]:focus-within,
    div[data-testid="stNumberInputContainer"]:focus-within {
        border-color: #8B5CF6 !important;
        box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.25) !important;
        outline: none !important;
    }

    /* -------------------------------------------------------------
       6. PRIMARY ACTION BUTTONS (Cinematic Violet #8B5CF6)
       ------------------------------------------------------------- */
    .stButton > button {
        background: linear-gradient(135deg, #8B5CF6 0%, #7C3AED 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #6D28D9 !important;
        border-radius: 8px !important;
        padding: 11px 24px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.2px !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(139, 92, 246, 0.3) !important;
        cursor: pointer !important;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #9333EA 0%, #6D28D9 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(139, 92, 246, 0.45) !important;
    }

    .stButton > button:active {
        transform: translateY(1px) !important;
    }

    /* -------------------------------------------------------------
       7. RESTRAINED SENTIMENT BADGES (Accessible & Crisp)
       Positive: Green | Neutral: Amber | Negative: Coral
       ------------------------------------------------------------- */
    .sentiment-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 6px;
        font-weight: 600;
        font-size: 0.85rem !important;
        letter-spacing: 0.2px;
    }

    .badge-vneg {
        background: rgba(239, 68, 68, 0.15);
        color: #F87171 !important;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }

    .badge-neg {
        background: rgba(249, 115, 22, 0.15);
        color: #FB923C !important;
        border: 1px solid rgba(249, 115, 22, 0.35);
    }

    .badge-neu {
        background: rgba(245, 158, 11, 0.15);
        color: #FBBF24 !important;
        border: 1px solid rgba(245, 158, 11, 0.35);
    }

    .badge-pos {
        background: rgba(34, 211, 238, 0.15);
        color: #38BDF8 !important;
        border: 1px solid rgba(34, 211, 238, 0.35);
    }

    .badge-vpos {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399 !important;
        border: 1px solid rgba(16, 185, 129, 0.35);
    }

    /* -------------------------------------------------------------
       8. JUSTIFICATION PANEL & EDITORIAL CALLOUTS
       ------------------------------------------------------------- */
    .justification-card {
        background-color: #151F32;
        border: 1px solid #1E293B;
        border-left: 4px solid #8B5CF6;
        border-radius: 8px;
        padding: 20px 24px;
        font-size: 0.98rem !important;
        line-height: 1.75 !important;
        color: #F1F5F9 !important;
        margin: 16px 0;
    }

    /* -------------------------------------------------------------
       9. CLEAN DATA TABLE STYLING
       ------------------------------------------------------------- */
    div[data-testid="stDataFrame"] {
        border: 1px solid #1E293B !important;
        border-radius: 10px !important;
        background-color: #151F32 !important;
    }

    /* -------------------------------------------------------------
       10. FOOTER
       ------------------------------------------------------------- */
    .app-footer {
        margin-top: 50px;
        padding-top: 20px;
        border-top: 1px solid #1E293B;
        text-align: center;
        color: #64748B !important;
        font-size: 0.82rem !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }
</style>
"""

def render_footer():
    return """
    <div class="app-footer">
        <div>
            🎬 <b>CinePulse</b> · 5-Class Movie Sentiment Intelligence
        </div>
        <div>
            Engine: <b>FastAPI</b> · Model: <b>Calibrated LinearSVC</b> · Monitoring: <b>Evidently AI</b>
        </div>
    </div>
    """
