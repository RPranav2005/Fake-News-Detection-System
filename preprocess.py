"""
preprocess.py
=============
Aggressive cleaning v3 for realistic metrics.
- Strips first 20 words.
- Strips publisher markers.
- Minimal vocabulary (3000 words).
"""

import os
import re
import pickle
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

# ── NLTK assets ──────────────────────────────────────────────────────────────
nltk.download("stopwords", quiet=True)
nltk.download("punkt", quiet=True)

# ── Constants ─────────────────────────────────────────────────────────────────
VOCAB_SIZE   = 3000     # Very limited for generality
MAX_LENGTH   = 400
EMBED_DIM    = 128
STOP_WORDS   = set(stopwords.words("english"))

def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""

    # 1. Stripping markers (Case Sensitive stage)
    text = re.sub(r"^[A-Z\s,]+\s+\([A-Za-z\s]+\)\s+-\s+", " ", text) 
    text = re.sub(r"^[A-Z\s,]+(?:,\s+[A-Z][a-z]+\s+\d+)?\s+-\s+", " ", text)

    # 2. Standardize
    text = text.lower()
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    
    # 3. Tokenize
    text = re.sub(r"\s+", " ", text).strip()
    tokens = text.split()
    tokens = [t for t in tokens if t not in STOP_WORDS and len(t) > 2]
    
    # 4. CRITICAL: Strip the first 20 words to eliminate any remaining intro/location/bio bias
    if len(tokens) > 30:
        tokens = tokens[20:]

    return " ".join(tokens)

def run_preprocessing(fake_path="dataset/Fake.csv", true_path="dataset/True.csv"):
    print("[INFO] Loading dataset ...")
    fake_df = pd.read_csv(fake_path)
    true_df = pd.read_csv(true_path)

    # Shuffled sampling to reduce size and potentially make it harder (optional, 20k random)
    fake_df = fake_df.sample(min(10000, len(fake_df)), random_state=42)
    true_df = true_df.sample(min(10000, len(true_df)), random_state=42)

    fake_df["label"] = 0  
    true_df["label"] = 1  

    df = pd.concat([fake_df, true_df]).reset_index(drop=True)
    print(f"[INFO] Balanced dataset: {len(df)} samples")

    print("[INFO] Cleaning text (AGGERSSIVE v3) ...")
    df["content"] = (df["title"].fillna("") + " " + df["text"].fillna("")).apply(clean_text)
    
    df = df[df["content"].str.len() > 50]

    X_train_text, X_test_text, y_train, y_test = train_test_split(
        df["content"], df["label"], test_size=0.2, random_state=42, shuffle=True, stratify=df["label"]
    )

    return X_train_text.tolist(), X_test_text.tolist(), y_train.values, y_test.values

def texts_to_padded(texts, tokenizer, max_len=MAX_LENGTH):
    sequences = tokenizer.texts_to_sequences(texts)
    padded = pad_sequences(sequences, maxlen=max_len, padding="post", truncating="post")
    return padded

def preprocess_single(text: str, tokenizer: Tokenizer) -> np.ndarray:
    cleaned = clean_text(text)
    padded  = texts_to_padded([cleaned], tokenizer)
    return padded
