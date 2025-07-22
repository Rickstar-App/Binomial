
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from binomial_model import binomial_option_pricing

# Page Configuration
st.set_page_config(page_title="Binomial Option Pricer", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>📈 Binomial Option Pricer</h1>", unsafe_allow_html=True)

# Inputs Section
st.markdown("### 🧮 Model Inputs")
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    S = st.number_input("Spot Price (S)", min_value=1.0, value=100.0, step=1.0)
    sigma = st.number_input("Volatility (σ)", min_value=0.01, value=0.2, step=0.01)
with col2:
    K = st.number_input("Strike Price (K)", min_value=1.0, value=100.0, step=1.0)
    r = st.number_input("Risk-free Rate (r)", min_value=0.0, value=0.05, step=0.01)
with col3:
    T = st.number_input("Time to Maturity (T in years)", min_value=0.01, value=1.0, step=0.1)
    N = st.number_input("Number of Steps (N)", min_value=1, value=100, step=1)

# Real-Time Option Price Outputs
st.markdown("### 💰 Option Price Output")
col_call, col_put = st.columns(2)
with col_call:
    call_price = binomial_option_pricing(S, K, T, r, sigma, int(N), option_type='call')
    st.markdown(
        f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 15px; border: 1px solid #ccc;'>"
        f"<h4>Call Option Price</h4><p style='font-size:20px'>💰 <span style='color:green; font-weight:bold;'>${call_price:.2f}</span></p>"
        f"</div>", unsafe_allow_html=True)
with col_put:
    put_price = binomial_option_pricing(S, K, T, r, sigma, int(N), option_type='put')
    st.markdown(
        f"<div style='background-color: #f9f9f9; border-radius: 10px; padding: 15px; border: 1px solid #ccc;'>"
        f"<h4>Put Option Price</h4><p style='font-size:20px'>💰 <span style='color:green; font-weight:bold;'>${put_price:.2f}</span></p>"
        f"</div>", unsafe_allow_html=True)

# Heatmap Controls Title
st.markdown("### 🔧 Heatmap Parameters")
col1, col2 = st.columns(2)
with col1:
    spot_min = st.number_input("Min Spot Price", value=80.0, step=1.0)
    spot_max = st.number_input("Max Spot Price", value=120.0, step=1.0)
with col2:
    vol_min = st.slider("Min Volatility for Heatmap", min_value=0.01, max_value=1.0, value=0.15, step=0.01)
    vol_max = st.slider("Max Volatility for Heatmap", min_value=0.01, max_value=1.0, value=0.38, step=0.01)

# Compute Grid Data
spot_range = np.linspace(spot_min, spot_max, 10)
vol_range = np.linspace(vol_min, vol_max, 10)

call_matrix = np.zeros((len(vol_range), len(spot_range)))
put_matrix = np.zeros((len(vol_range), len(spot_range)))

for i, vol in enumerate(vol_range):
    for j, spot in enumerate(spot_range):
        call_matrix[i, j] = binomial_option_pricing(spot, K, T, r, vol, int(N), option_type='call')
        put_matrix[i, j] = binomial_option_pricing(spot, K, T, r, vol, int(N), option_type='put')

# Convert to DataFrames
call_df = np.round(call_matrix, 2)
put_df = np.round(put_matrix, 2)
spot_labels = np.round(spot_range, 1)
vol_labels = np.round(vol_range, 2)

# Heatmaps
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

sns.heatmap(call_df, xticklabels=spot_labels, yticklabels=vol_labels,
            cmap="RdYlGn", annot=True, fmt=".2f", linewidths=0.3, ax=axes[0],
            cbar_kws={'label': 'Call Price'}, annot_kws={"size": 8})
axes[0].set_title("Call Price Heatmap", fontsize=14)
axes[0].set_xlabel("Spot Price")
axes[0].set_ylabel("Volatility")

sns.heatmap(put_df, xticklabels=spot_labels, yticklabels=vol_labels,
            cmap="RdYlGn", annot=True, fmt=".2f", linewidths=0.3, ax=axes[1],
            cbar_kws={'label': 'Put Price'}, annot_kws={"size": 8})
axes[1].set_title("Put Price Heatmap", fontsize=14)
axes[1].set_xlabel("Spot Price")
axes[1].set_ylabel("Volatility")

st.pyplot(fig)
