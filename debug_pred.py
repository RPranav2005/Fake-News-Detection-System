import os
import pickle
import numpy as np
import tensorflow as tf
from preprocess import preprocess_single

# Load
model = tf.keras.models.load_model("saved_model.h5")
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

fake_text = """BREAKING: UNBELIEVABLE Discovery They Don't Want You to Know! "Exclusive documents leaked from a top-secret agency reveal a SHOCKING scandal that will change everything. Insiders claim the entire system is completely rigged and a massive cover-up is happening right now. You won't believe what happens next as officials scramble to hide the truth from the public. This is a total disaster and a bombshell for the upcoming election! Share this everywhere before it gets taken down by the mainstream media!\""""

real_text = """Economic Growth Trends Show Moderate Recovery in Q3. According to the latest report from the Bureau of Labor Statistics, the national economy expanded at an annual rate of 2.1% in the third quarter. The data suggests that increased consumer spending and a stable labor market contributed to the growth. Federal officials stated that while inflation remains a concern, the current trajectory indicates a steady recovery. Private sector analysts confirmed that manufacturing output rose by 0.5%, following a period of stagnation earlier this year."""

def test(text, name):
    padded = preprocess_single(text, tokenizer)
    proba  = float(model.predict(padded, verbose=0)[0][0])
    print(f"[{name}] Raw Proba: {proba:.6f} -> {'REAL' if proba >= 0.5 else 'FAKE'}")

test(fake_text, "FAKE SAMPLE")
test(real_text, "REAL SAMPLE")
