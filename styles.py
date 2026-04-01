import streamlit as st

def get_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,700;1,700&family=Syne:wght@800&family=Orbitron:wght@900&display=swap');

    :root {
        --bg-main: #000000;
        --bg-sidebar: #000000;
        --accent: #d32f2f;
        --accent-glow: rgba(211, 47, 47, 0.2);
        --text-main: #f5f5f5;
        --text-muted: #888888;
        --card-bg: #0a0a0a;
        --border: #3d1a1a;
    }

    /* PFND Brand Style (Nagasaki alternative via Orbitron) */
    /* Global Sticky Header (Noir Crimson Edition) */
    .global-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 75px;
        background: linear-gradient(180deg, #8b0000 0%, #1a0f0f 100%);
        border-bottom: 2px solid #b71c1c;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999;
        box-shadow: 0 4px 30px rgba(0,0,0,0.9);
        pointer-events: none;
    }
    .pfnd-brand {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        color: #fce4e4;
        font-size: 2.8rem;
        letter-spacing: 12px;
        margin-right: -12px;
        text-shadow: 0 0 15px rgba(255,255,255,0.4), 0 0 30px rgba(211,47,47,0.6);
        pointer-events: auto;
    }

    /* Streamlit UI Fixes for Global Header */
    .stApp {
        padding-top: 75px !important;
        background-color: var(--bg-main) !important;
    }
    
    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 75px !important;
        z-index: 1001 !important;
        pointer-events: none !important;
    }
    
    header[data-testid="stHeader"] * {
        pointer-events: auto !important;
    }

    [data-testid="stSidebarCollapseButton"] {
        color: #fce4e4 !important;
        background-color: rgba(255,255,255,0.2) !important;
        border-radius: 50% !important;
        position: fixed !important;
        top: 15px !important;
        left: 10px !important;
        z-index: 10000 !important;
    }
    
    /* Hide Deploy button, Streamlit toolbar and Main Menu */
    .stAppDeployButton, [data-testid="stToolbar"], #MainMenu {
        display: none !important;
    }

    [data-testid="stSidebar"] {
        top: 75px !important;
        height: calc(100vh - 75px) !important;
        background-color: var(--bg-sidebar) !important;
        z-index: 1000 !important;
    }

    section[data-testid="stSidebar"][aria-expanded="true"] {
        width: 200px !important;
        border-right: 1px solid var(--border) !important;
    }
    
    /* Top Bar Branding Fix (The request about useless space) */
    .block-container { padding-top: 2rem !important; }

    /* Custom Navbar/Header Simulation */
    .nav-label { color: var(--accent); font-weight: 800; letter-spacing: 1px; font-size: 0.9rem; }

    /* Card UI */
    .st-card {
        background-color: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 24px;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .st-card:hover { border-color: var(--accent); transform: translateY(-2px); }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #b71c1c 0%, #d32f2f 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: 600 !important;
        padding: 10px 24px !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Dynamic Main Content Centering */
    .block-container { 
        padding-top: 2rem !important; 
        max-width: 1200px !important;
        margin: 0 auto !important;
        width: 100% !important;
    }

    /* Hide default "Navigation" header in sidebar */
    [data-testid="stSidebarNav"] > div:first-child {
        display: none !important;
    }

    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: #161616 !important;
        border: 1px solid var(--border) !important;
        color: white !important;
    }
    .stTextInput>div>div>input:focus { border-color: var(--accent) !important; }

    /* Result Boxes */
    .result-box {
        padding: 30px;
        border-radius: 8px;
        text-align: center;
        border: 1px solid var(--border);
        background: #121212;
    }
    .status-real { color: #4CAF50; border-color: rgba(76, 175, 80, 0.3); background: rgba(76, 175, 80, 0.05); }
    .status-fake { color: #ff5252; border-color: rgba(211, 47, 47, 0.3); background: rgba(211, 47, 47, 0.05); }
    </style>
    """

def init_page(title):
    st.markdown(get_css(), unsafe_allow_html=True)

def draw_global_header():
    st.markdown('<div class="global-header"><div class="pfnd-brand">PFND</div></div>', unsafe_allow_html=True)

def draw_sidebar_footer():
    st.sidebar.markdown("<br><br>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p class='nav-label'>NOIR CRIMSON V1.2</p>", unsafe_allow_html=True)
    st.sidebar.caption("© 2026 Peanow Intelligence")
