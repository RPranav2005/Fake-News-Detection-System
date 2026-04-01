import streamlit as st
import os
import pickle
import tensorflow as tf
from styles import init_page, draw_sidebar_footer
from preprocess import clean_text, preprocess_single
import utils

# ── Page Setup ─────────────────────────────────────────────────────────────
init_page("Fake News Detection")

# ── Load Model (Cached) ────────────────────────────────────────────────────
@st.cache_resource
def load_model_and_tokenizer():
    model_path = "saved_model.h5"
    vocab_path = "tokenizer.pkl"
    if os.path.exists(model_path) and os.path.exists(vocab_path):
        try:
            model = tf.keras.models.load_model(model_path)
            with open(vocab_path, "rb") as f:
                tokenizer = pickle.load(f)
            return model, tokenizer, None
        except Exception as e:
            return None, None, str(e)
    return None, None, "Model files missing. Please run model_lstm.py first."

model, tokenizer, load_error = load_model_and_tokenizer()

# ── UI Layout ──────────────────────────────────────────────────────────────
st.markdown("<h1>Fake News Detection</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:var(--text-muted); margin-bottom:30px;'>Analyze articles for misinformation using our BiLSTM Neural Network.</p>", unsafe_allow_html=True)

if load_error:
    st.error(load_error)
    st.stop()

# Input Content
user_input = ""
article_title = "User Input"

with st.container():
    user_input = st.text_area("Article Content", placeholder="Paste article text here...", height=250)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Start Analysis"):
        if not user_input or len(user_input.strip()) < 20:
            st.warning("Please provide a valid article (minimum 20 characters).")
        else:
            with st.spinner("Analyzing linguistic patterns..."):
                # Preprocess & Predict
                seq = preprocess_single(user_input, tokenizer)
                prediction = model.predict(seq)[0][0]
                label = "FAKE" if prediction < 0.5 else "REAL"
                confidence = (1 - prediction) if label == "FAKE" else prediction
                
                # Secondary Analysis
                sentiment = utils.analyze_sentiment(user_input)
                bias = utils.detect_bias(user_input)
                clickbait = {"is_clickbait": False, "score": 0.0, "reasons": []} # URL disabled
                credibility = utils.compute_credibility_score(confidence, sentiment["score"], bias["score"], label == "REAL")
                explanation = utils.generate_explanation(label, confidence, sentiment, bias, clickbait)

                # ── Display Results ──
                st.markdown("---")
                col1, col2 = st.columns([1, 1.5])

                with col1:
                    status_class = "status-real" if label == "REAL" else "status-fake"
                    st.markdown(f"""
                    <div class="result-box {status_class}">
                        <h4 style='margin:0; opacity:0.8; font-size:0.9rem; text-transform:uppercase;'>Verdict</h4>
                        <h1 style='margin:5px 0; font-size:3rem;'>{label}</h1>
                        <p style='margin:0; font-weight:600;'>{round(confidence*100, 1)}% Confidence</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown(f"""
                    <div class="result-box">
                        <h4 style='margin:0; opacity:0.8; font-size:0.9rem;'>Credibility Score</h4>
                        <h1 style='margin:5px 0; font-size:2.8rem; color:var(--accent);'>{credibility['score']}</h1>
                        <p style='margin:0; font-weight:600;'>{credibility['level']}</p>
                    </div>
                    """, unsafe_allow_html=True)

                with col2:
                    st.markdown("<h4 style='margin-bottom:15px;'>Analysis Report</h4>", unsafe_allow_html=True)
                    st.markdown(f"""<div class="explanation-card">{explanation}</div>""", unsafe_allow_html=True)
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.metric("Bias Level", bias["label"])
                    with c2:
                        st.metric("Sentiment", sentiment["label"])
                    with c3:
                        cb_text = "Clickbait" if clickbait["is_clickbait"] else "Normal"
                        st.metric("Headline", cb_text)

draw_sidebar_footer()


