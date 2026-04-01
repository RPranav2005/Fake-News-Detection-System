import streamlit as st
from styles import init_page, draw_sidebar_footer


# ── Page Setup ─────────────────────────────────────────────────────────────
init_page("Dataset Context")

st.markdown("<h1>Dataset Context</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:var(--text-muted); margin-bottom:30px;'>Background information on the data sources and analysis methodology.</p>", unsafe_allow_html=True)

with st.container():
    st.markdown(f"""
    <div style='max-width:900px; margin-left:0;'>
    <h2 style='color:var(--accent); font-weight:800;'>Project Overview</h2>
    <p style='color:var(--text-muted); line-height:1.7;'>
    Peanow's Fake News Detector is an AI-powered misinformation analysis platform built on a 
    <b>Bidirectional LSTM (BiLSTM)</b> deep learning model.
    </p>
    
    <h3 style='color:var(--accent); margin-top:30px;'>Source Material</h3>
    <p style='color:var(--text-muted); line-height:1.7;'>
    The model was trained on the <b>Fake and Real News Dataset</b> (Kaggle), which consists of over 44,000 labelled news articles.
    Articles were sourced from major publications (True) and known misinformation repositories (Fake) between 2015-2018.
    </p>

    <h3 style='color:var(--accent); margin-top:30px;'>Analysis Methodology</h3>
    <ul style='color:var(--text-muted); line-height:2;'>
        <li><b>Fake / Real Classification</b> — BiLSTM probability output.</li>
        <li><b>Bias Detection</b> — Mapping emotional vs factual language density.</li>
        <li><b>Sentiment Analysis</b> — Polarity check to identify inflammatory tones.</li>
        <li><b>headline Integrity</b> — Checking for clickbait patterns and sensationalism.</li>
    </ul>

    <h3 style='color:var(--accent); margin-top:30px;'>Generalization & Ethics</h3>
    <p style='color:var(--text-muted); line-height:1.7;'>
    Version 2.0 of the model explicitly removes publisher names (e.g., Reuters, AP) during training 
    to ensure it learns linguistic patterns rather than just memorizing news agencies. 
    Users should always cross-reference AI results with multiple primary sources.
    </p>
    </div>
    """, unsafe_allow_html=True)

draw_sidebar_footer()


