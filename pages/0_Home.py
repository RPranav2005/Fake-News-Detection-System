import streamlit as st
from styles import init_page, draw_sidebar_footer, draw_global_header

# ── Page Configuration ─────────────────────────────────────────────────────
# This page is now managed by st.navigation in app.py, but we keep styling
from styles import get_css
st.markdown(get_css(), unsafe_allow_html=True)

# ── Hero Section ───────────────────────────────────────────────────────────
# ── Hero Section (Cinematic Merge) ─────────────────────────────────────────
st.markdown("""
<div style="text-align: center; padding: 100px 0 60px 0; width: 100%;">
    <p class="sub-branding">PEANOW'S FAKE NEWS DETECTOR</p>
    <div style="margin: 30px 0;">
        <h1 class="akira" style="font-size: 4rem;">COMING SOON</h1>
    </div>
    <p class="coming-soon-sub">NEWS ARTICLES COMING SOON</p>
</div>
""", unsafe_allow_html=True)

# ── Call to Action ─────────────────────────────────────────────────────────
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("START AI ANALYSIS →", use_container_width=True):
        st.switch_page("pages/2_Detection.py")

st.markdown("<br><br>", unsafe_allow_html=True)

# ── Feature Grid ───────────────────────────────────────────────────────────
f1, f2, f3 = st.columns(3)

with f1:
    st.markdown("""
    <div class="st-card">
        <h3 style="color: var(--accent); margin-top:0;">Real-time Analysis</h3>
        <p style="color: var(--text-muted);">Instant classification using advanced BiLSTM deep learning models trained on verified news datasets.</p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="st-card">
        <h3 style="color: var(--accent); margin-top:0;">Bias Detection</h3>
        <p style="color: var(--text-muted);">Identify hidden political leanings and sensationalism patterns in text content automatically.</p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="st-card">
        <h3 style="color: var(--accent); margin-top:0;">Clickbait Check</h3>
        <p style="color: var(--text-muted);">Analyze headlines to detect manipulative click-driven language designed to mislead readers.</p>
    </div>
    """, unsafe_allow_html=True)

# ── Sidebar Footer ────────────────────────────────────────────────────────
draw_sidebar_footer()
