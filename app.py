import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from binomial_model import binomial_option_pricing
from greeks import calculate_greeks

# Page Configuration
st.set_page_config(page_title="Binomial Option Pricer", layout="wide")

# Title
st.markdown("<h1 style='text-align: center;'>📈 Binomial Option Pricer</h1>", unsafe_allow_html=True)

# Inputs Section
st.markdown("### 🔧 Inputs")
with st.container():
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

style = st.selectbox("Option Style", ["European", "American"], index=0).lower()

# Real-Time Option Price Outputs
col_call, col_put = st.columns(2)
with col_call:
    call_price = binomial_option_pricing(S, K, T, r, sigma, int(N), option_type='call', style=style)
    st.markdown(f"<div style='border:1px solid #ccc; padding:10px; border-radius:5px;'>📈 Call Option Price: <b>${call_price:.2f}</b></div>", unsafe_allow_html=True)

with col_put:
    put_price = binomial_option_pricing(S, K, T, r, sigma, int(N), option_type='put', style=style)
    st.markdown(f"<div style='border:1px solid #ccc; padding:10px; border-radius:5px;'>📉 Put Option Price: <b>${put_price:.2f}</b></div>", unsafe_allow_html=True)

# Purchase Price Inputs for PnL
st.markdown("### 💰 Purchase Prices")
col1, col2 = st.columns(2)
with col1:
    call_purchase_price = st.number_input("Call Purchase Price", min_value=0.0, value=10.0, step=0.1)
with col2:
    put_purchase_price = st.number_input("Put Purchase Price", min_value=0.0, value=10.0, step=0.1)

# Heatmap Parameters
st.markdown("### 🌡️ Heatmap Parameters")
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
        call_matrix[i, j] = binomial_option_pricing(spot, K, T, r, vol, int(N), option_type='call', style=style)
        put_matrix[i, j] = binomial_option_pricing(spot, K, T, r, vol, int(N), option_type='put', style=style)

# Convert to DataFrames
call_df = np.round(call_matrix, 2)
put_df = np.round(put_matrix, 2)
spot_labels = np.round(spot_range, 1)
vol_labels = np.round(vol_range, 2)

# Price Heatmaps
st.markdown("### 📊 Option Price Heatmaps")
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

# Calculate PnL Matrices
call_pnl_matrix = call_matrix - call_purchase_price
put_pnl_matrix = put_matrix - put_purchase_price

call_pnl_df = np.round(call_pnl_matrix, 2)
put_pnl_df = np.round(put_pnl_matrix, 2)

# PnL Heatmaps
st.markdown("### 💹 PnL Heatmaps")
fig_pnl, axes_pnl = plt.subplots(1, 2, figsize=(14, 6))

sns.heatmap(call_pnl_df, xticklabels=spot_labels, yticklabels=vol_labels,
            cmap="RdYlGn", center=0, annot=True, fmt=".2f", linewidths=0.3,
            ax=axes_pnl[0], cbar_kws={'label': 'Call PnL'}, annot_kws={"size": 8})
axes_pnl[0].set_title("Call PnL Heatmap", fontsize=14)
axes_pnl[0].set_xlabel("Spot Price")
axes_pnl[0].set_ylabel("Volatility")

sns.heatmap(put_pnl_df, xticklabels=spot_labels, yticklabels=vol_labels,
            cmap="RdYlGn", center=0, annot=True, fmt=".2f", linewidths=0.3,
            ax=axes_pnl[1], cbar_kws={'label': 'Put PnL'}, annot_kws={"size": 8})
axes_pnl[1].set_title("Put PnL Heatmap", fontsize=14)
axes_pnl[1].set_xlabel("Spot Price")
axes_pnl[1].set_ylabel("Volatility")

st.pyplot(fig_pnl)

# --- Option Greeks Section ---
st.markdown("### ⚠️ Option Greeks Calculations")

call_greeks = calculate_greeks(S, K, T, r, sigma, int(N), option_type='call')
put_greeks = calculate_greeks(S, K, T, r, sigma, int(N), option_type='put')

# --- Coloring and Utility Functions ---
def color_value(val, is_beneficial):
    color = 'green' if is_beneficial else 'red'
    return f"<span style='color:{color}; font-weight:bold'>{val:.4f}</span>"

def is_beneficial(greek, value, option_type):
    if greek == 'delta':
        return value > 0 if option_type == 'call' else value < 0
    elif greek == 'gamma':
        return value > 0.5
    elif greek == 'vega':
        return value > 0
    elif greek == 'theta':
        return value < 0
    elif greek == 'rho':
        return value > 0 if option_type == 'call' else value < 0
    return False

def render_greek_table(greeks_dict, option_type):
    rendered = ""
    for greek in ['delta', 'gamma', 'vega', 'theta', 'rho']:
        val = greeks_dict[greek]
        colored = color_value(val, is_beneficial(greek, val, option_type))
        rendered += f"**{greek.capitalize()}**: {colored}<br>"
    return rendered

# --- Render Columns ---
col1, col2 = st.columns(2)
with col1:
    st.markdown("#### 📈 Call Option Greeks")
    st.markdown(render_greek_table(call_greeks, 'call'), unsafe_allow_html=True)

with col2:
    st.markdown("#### 📉 Put Option Greeks")
    st.markdown(render_greek_table(put_greeks, 'put'), unsafe_allow_html=True)

# --- Definitions ---
st.markdown("""
#### ℹ️ What Do These Mean?

- **Delta**: Sensitivity to changes in the underlying asset price.
- **Gamma**: Sensitivity of Delta to changes in the underlying price.
- **Vega**: Sensitivity to changes in implied volatility.
- **Theta**: Sensitivity to the passage of time (time decay).
- **Rho**: Sensitivity to changes in the interest rate.
""")
