import os
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf
from preprocess import preprocess_single

# Load
model = tf.keras.models.load_model("saved_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Load original data
fake_df = pd.read_csv("dataset/Fake.csv")
true_df = pd.read_csv("dataset/True.csv")

def test(text, name):
    padded = preprocess_single(text, tokenizer)
    proba  = float(model.predict(padded, verbose=0)[0][0])
    print(f"[{name}] Raw Proba: {proba:.6f} -> {'REAL' if proba >= 0.5 else 'FAKE'}")

print("--- Testing Dataset Samples ---")
test(fake_df['text'].iloc[0], "Original Fake.csv sample")
test(true_df['text'].iloc[0], "Original True.csv sample")

print("\n--- Testing Custom Samples ---")
real_custom = "WASHINGTON (Reuters) - The U.S. economy showed signs of strength as markets rallied today following the latest employment report."
test(real_custom, "Custom Real (with Reuters)")

real_no_reuters = "The national economy expanded by 2.1% this quarter as consumer spending increased according to government reports."
test(real_no_reuters, "Custom Real (no Reuters)")
