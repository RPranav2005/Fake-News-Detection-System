import streamlit as st
from styles import init_page, draw_sidebar_footer, draw_global_header

# ── Page Configuration (Master) ───────────────────────────────────────────
# We define pages explicitly to ensure they appear in the sidebar
pages = {
    "Navigation": [
        st.Page("pages/0_Home.py", title="Home", default=True),
        st.Page("pages/2_Detection.py", title="Detector"),
        st.Page("pages/3_Model_Insights.py", title="Insights"),
        st.Page("pages/4_Dataset_Context.py", title="Dataset"),
    ]
}

# Set global config
st.set_page_config(
    page_title="Peanow's Detector",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Run Navigation
draw_global_header()
pg = st.navigation(pages, position="sidebar")
pg.run()
