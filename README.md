# 🛡️ Fake News Detection System

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10+-FF6F00?logo=tensorflow&logoColor=white)](https://www.tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.25+-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

A state-of-the-art **Fake News Detection and Misinformation Analysis** platform. This system utilizes a **Bidirectional LSTM (BiLSTM)** neural network to classify news articles as "REAL" or "FAKE" while providing a comprehensive breakdown of linguistic patterns, sentiment, bias, and overall credibility.

---

## 🚀 Key Features

- **🔍 Intelligent Verdict**: Real-time classification of news articles with high-precision confidence scoring.
- **📊 Multi-Dimensional Analysis**:
    - **Sentiment Analysis**: Understand the emotional tone of the content.
    - **Bias Detection**: Identifies potential political or linguistic bias.
    - **Credibility Scoring**: An algorithmic score (1-10) evaluating the reliability of the source text.
- **📝 Automated Explanations**: Generates a detailed reasoning report for every analysis.
- **🖥️ Premium Dashboard**: A modern, multi-page Streamlit interface designed for a seamless user experience.
- **📈 Model Insights**: Interactive visualization of training metrics, confusion matrices, and model architecture.

---

## 🛠️ Tech Stack

- **Deep Learning**: TensorFlow, Keras (BiLSTM Architecture)
- **NLP**: NLTK, Scikit-learn
- **Frontend**: Streamlit (with custom CSS/Glassmorphism)
- **Data Handling**: Pandas, NumPy
- **Visualization**: Plotly, Wordcloud, Seaborn, Matplotlib

---

## 🏗️ Project Structure

```text
├── app.py                # Main Streamlit entrance
├── model_lstm.py         # BiLSTM training & model definition
├── preprocess.py         # Advanced text cleaning & tokenization
├── utils.py              # Logic for sentiment, bias, and credibility
├── styles.py             # Custom UI design system
├── pages/                # Multi-page application structure
│   ├── 0_Home.py         # Landing Page
│   ├── 2_Detection.py    # Main Detector
│   ├── 3_Model_Insights.py # Metrics & Graphs
│   └── 4_Dataset_Context.py # Data transparency
├── dataset/              # Training/Validation data
├── static/               # Generated plots & assets
├── tokenizer.pkl         # Pre-trained tokenizer
└── saved_model.h5        # Trained BiLSTM model
```

---

## 🏁 Getting Started

### 1. Clone the repository
```bash
git clone https://github.com/your-username/fake-news-detector.git
cd fake-news-detector
```

### 2. Set up virtual environment (Recommended)
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 🧠 Model Architecture

The core of the system is a **Bidirectional Long Short-Term Memory (BiLSTM)** network. Unlike traditional LSTMs, BiLSTMs process text in both directions (forward and backward), allowing the model to capture context from both the start and the end of a sentence—crucial for identifying subtle misinformation patterns.

**Hyperparameters:**
- **Max Words**: 3,000 (Vocabulary size)
- **Max Length**: 400 (Tokens per article)
- **Regularization**: SpatialDropout1D (0.4) and L2 weight decay to prevent overfitting.
- **Optimizer**: Adam (0.0001 learning rate)

---

## 📈 Performance

The model is trained on a hybridized dataset (ISOT, WELFake) to ensure generalizability. It focuses on **realistic metrics** rather than overfit 99% accuracy, ensuring it performs well on real-world news content.

> [!TIP]
> You can view live training curves and the confusion matrix directly in the **Model Insights** tab of the application.

---

## ⚖️ License

Distributed under the MIT License. See `LICENSE` for more information.

---

**Developed with ❤️ by [Your Name/Peanow]**
