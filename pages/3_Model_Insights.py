import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from styles import init_page, draw_sidebar_footer


# ── Page Setup ─────────────────────────────────────────────────────────────
init_page("Model Insights")

# ── Data & Metrics Mockup (In production these would load from evaluation logs) ──
metrics = {
    "Accuracy": 0.956,
    "Precision": 0.948,
    "Recall": 0.962,
    "F1 Score": 0.955
}

st.markdown("<h1>Model Insights</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:var(--text-muted); margin-bottom:30px;'>Technical breakdown of the BiLSTM performance and neural architecture.</p>", unsafe_allow_html=True)

# ── Performance Cards ──
cols = st.columns(4)
for i, (name, val) in enumerate(metrics.items()):
    with cols[i]:
        st.markdown(f"""
        <div style='background:#121212; padding:20px; border:1px solid var(--border); border-radius:4px; text-align:center;'>
            <p style='color:var(--text-muted); margin:0; font-size:0.85rem;'>{name}</p>
            <h2 style='color:var(--accent); margin:5px 0;'>{val*100:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Architecture Table ──
st.markdown("### Neural Architecture (v2.0)")
st.markdown("""
<div style='background:rgba(211,47,47,0.02); padding:20px; border-radius:4px; border:1px solid var(--border);'>
<table style="width:100%; color:var(--text-main); border-collapse:collapse;">
  <tr style='border-bottom:1px solid var(--border);'>
    <th style='text-align:left;padding:12px;color:var(--text-muted);'>Layer</th>
    <th style='text-align:left;padding:12px;color:var(--text-muted);'>Spec</th>
  </tr>
  <tr style='border-bottom:1px solid var(--border);'><td style='padding:12px;'>Embedding</td><td style='padding:12px;'>64-dim Vector (3k Vocab)</td></tr>
  <tr style='border-bottom:1px solid var(--border);'><td style='padding:12px;'>Bi-LSTM</td><td style='padding:12px;'>32 Units · Dropout 0.7</td></tr>
  <tr style='border-bottom:1px solid var(--border);'><td style='padding:12px;'>Hidden</td><td style='padding:12px;'>32 Dense · ReLU</td></tr>
  <tr><td style='padding:12px;'>Output</td><td style='padding:12px;'>Sigmoid · Binary Crossentropy</td></tr>
</table>
</div>
""", unsafe_allow_html=True)

# ── Performance Chart (Mockup) ──
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("### Training Convergence")
epochs = list(range(1, 11))
acc = [0.85, 0.89, 0.92, 0.93, 0.94, 0.945, 0.95, 0.952, 0.954, 0.956]
val_acc = [0.82, 0.86, 0.88, 0.90, 0.91, 0.92, 0.925, 0.93, 0.935, 0.94]

fig = go.Figure()
fig.add_trace(go.Scatter(x=epochs, y=acc, name="Training Acc", line=dict(color='#D32F2F', width=3)))
fig.add_trace(go.Scatter(x=epochs, y=val_acc, name="Validation Acc", line=dict(color='#888888', dash='dot')))
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font_color='#888888',
    margin=dict(l=0, r=0, t=30, b=0),
    height=300,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(fig, use_container_width=True)

draw_sidebar_footer()


