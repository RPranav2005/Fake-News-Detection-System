"""
model_lstm.py
=============
Hyper-regularized model for realistic metrics.
"""

import os
import pickle
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    classification_report, confusion_matrix,
)

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Embedding, Bidirectional, LSTM, Dense, Dropout, SpatialDropout1D,
)
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
from tensorflow.keras.preprocessing.text import Tokenizer

# Local imports
from preprocess import run_preprocessing, texts_to_padded

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH  = os.path.join(BASE_DIR, "saved_model.h5")
TOK_PATH    = os.path.join(BASE_DIR, "tokenizer.pkl")
STATIC_DIR  = os.path.join(BASE_DIR, "static")

MAX_WORDS   = 3000
MAX_LEN     = 400
EMBED_DIM   = 64

def build_model():
    model = Sequential([
        Embedding(MAX_WORDS, EMBED_DIM),
        SpatialDropout1D(0.4), # Increased
        Bidirectional(LSTM(32, return_sequences=False)), # Reduced
        Dropout(0.7), # Increased
        Dense(32, activation="relu", kernel_regularizer=l2(0.01)), # Increased regularization
        Dropout(0.5), # Increased
        Dense(1, activation="sigmoid", name="output")
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    return model

def train():
    print("\n" + "="*50)
    print("  REALISTIC FAKE NEWS DETECTOR TRAINING")
    print("="*50)

    # Split
    X_train_text, X_test_text, y_train, y_test = run_preprocessing()

    # Tokenizer
    tokenizer = Tokenizer(num_words=MAX_WORDS, oov_token="<OOV>")
    tokenizer.fit_on_texts(X_train_text)

    # Vectorize
    X_train = texts_to_padded(X_train_text, tokenizer)
    X_test  = texts_to_padded(X_test_text, tokenizer)

    # Train
    model = build_model()
    model.summary()

    callbacks = [
        EarlyStopping(monitor="val_loss", patience=2, restore_best_weights=True, verbose=1),
        ModelCheckpoint(MODEL_PATH, monitor="val_loss", save_best_only=True, verbose=1)
    ]

    print("[INFO] Starting training (expect realistic metrics) ...")
    history = model.fit(
        X_train, y_train,
        validation_data=(X_test, y_test),
        epochs=10,
        batch_size=64,
        callbacks=callbacks
    )

    # Eval
    y_pred = (model.predict(X_test) > 0.5).astype(int)
    print("\n" + classification_report(y_test, y_pred, target_names=["FAKE", "REAL"]))

    # Save
    with open(TOK_PATH, "wb") as f:
        pickle.dump(tokenizer, f)

    # Manual plots
    def save_plot(history, path):
        plt.figure(figsize=(12, 4))
        plt.subplot(1, 2, 1)
        plt.plot(history.history["accuracy"], label="Train")
        plt.plot(history.history["val_accuracy"], label="Val")
        plt.title("Accuracy")
        plt.legend()
        plt.subplot(1, 2, 2)
        plt.plot(history.history["loss"], label="Train")
        plt.plot(history.history["val_loss"], label="Val")
        plt.title("Loss")
        plt.legend()
        plt.savefig(path)
        plt.close()

    save_plot(history, os.path.join(STATIC_DIR, "training_curves.png"))
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["FAKE", "REAL"], yticklabels=["FAKE", "REAL"])
    plt.title("Confusion Matrix")
    plt.savefig(os.path.join(STATIC_DIR, "confusion_matrix.png"))
    plt.close()

    print(f"\n[✓] Done! Accuracy should be in the realistic range.")

if __name__ == "__main__":
    train()
