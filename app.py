import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from blackscholes import call_price, put_price, delta, gamma, vega, theta, rho, implied_vol, monte_carlo

st.set_page_config(page_title="Black-Scholes Pricer", layout="wide")
st.markdown("Made by [Anshul Sharma](https://www.linkedin.com/in/anshul-sharma-520489387/)")
st.title("Black-Scholes Options Pricing Model")

# -------------------------
# Sidebar inputs
# -------------------------
st.sidebar.header("Parameters")
S = st.sidebar.number_input("Stock Price (S)", value=100.0, min_value=1.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0, min_value=1.0)
T = st.sidebar.number_input("Time to Expiry (T, years)", value=1.0, min_value=0.01)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05, min_value=0.0, max_value=1.0)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2, min_value=0.01, max_value=5.0)

st.sidebar.markdown("---")
st.sidebar.header("Heatmap Parameters")
S_min = st.sidebar.number_input("Min Stock Price", value=50.0, min_value=1.0)
S_max = st.sidebar.number_input("Max Stock Price", value=150.0, min_value=1.0)
sigma_min = st.sidebar.number_input("Min Volatility", value=0.05, min_value=0.01)
sigma_max = st.sidebar.number_input("Max Volatility", value=0.5, min_value=0.01)

# -------------------------
# Call and Put Prices
# -------------------------
call = call_price(S, K, T, r, sigma)
put = put_price(S, K, T, r, sigma)
mc_call = monte_carlo(S, K, T, r, sigma, option_type='call', simulations=10000)
mc_put = monte_carlo(S, K, T, r, sigma, option_type='put', simulations=10000)

st.header("Option Prices")
col1, col2 = st.columns(2)
col1.markdown(f"""
<div style='background-color:#1a472a; padding:20px; border-radius:10px; text-align:center'>
<h3 style='color:#00ff00'>CALL Value</h3>
<h2 style='color:#00ff00'>${call:.2f}</h2>
<p style='color:#aaaaaa'>Monte Carlo: ${mc_call:.2f}</p>
</div>
""", unsafe_allow_html=True)

col2.markdown(f"""
<div style='background-color:#4a1a1a; padding:20px; border-radius:10px; text-align:center'>
<h3 style='color:#ff4444'>PUT Value</h3>
<h2 style='color:#ff4444'>${put:.2f}</h2>
<p style='color:#aaaaaa'>Monte Carlo: ${mc_put:.2f}</p>
</div>
""", unsafe_allow_html=True)

# -------------------------
# Greeks
# -------------------------
st.header("Greeks")
g1, g2, g3, g4, g5 = st.columns(5)
g1.metric("Delta", f"{delta(S, K, T, r, sigma):.4f}")
g2.metric("Gamma", f"{gamma(S, K, T, r, sigma):.4f}")
g3.metric("Vega", f"{vega(S, K, T, r, sigma):.4f}")
g4.metric("Theta", f"{theta(S, K, T, r, sigma):.4f}")
g5.metric("Rho", f"{rho(S, K, T, r, sigma):.4f}")


# -------------------------
# P&L at Expiry
# -------------------------
st.header("P&L at Expiry")

S_expiry = np.linspace(S * 0.5, S * 1.5, 100)
call_pnl = [max(s - K, 0) - call for s in S_expiry]
put_pnl = [max(K - s, 0) - put for s in S_expiry]

fig_pnl, ax_pnl = plt.subplots(figsize=(10, 4))
fig_pnl.patch.set_facecolor('#0E1117')
ax_pnl.set_facecolor('#0E1117')
ax_pnl.plot(S_expiry, call_pnl, color='#00ff00', label='Call P&L')
ax_pnl.plot(S_expiry, put_pnl, color='#ff4444', label='Put P&L')
ax_pnl.axhline(y=0, color='white', linestyle='--', linewidth=0.8)
ax_pnl.axvline(x=K, color='yellow', linestyle='--', linewidth=0.8, label='Strike Price')
ax_pnl.set_xlabel('Stock Price at Expiry', color='white')
ax_pnl.set_ylabel('Profit / Loss', color='white')
ax_pnl.set_title('P&L at Expiry', color='white')
ax_pnl.tick_params(colors='white')
ax_pnl.legend()
ax_pnl.spines['bottom'].set_color('white')
ax_pnl.spines['left'].set_color('white')
ax_pnl.spines['top'].set_visible(False)
ax_pnl.spines['right'].set_visible(False)
st.pyplot(fig_pnl)

# -------------------------
# Implied Vol Calculator
# -------------------------
st.header("Implied Volatility Calculator")
st.write("Enter a market option price to calculate implied volatility.")
col1, col2 = st.columns(2)
market_price = col1.number_input("Market Option Price", value=10.45, min_value=0.01)
option_type_iv = col2.selectbox("Option Type", ["call", "put"])
if st.button("Calculate Implied Volatility"):
    iv = implied_vol(market_price, S, K, T, r, option_type=option_type_iv)
    st.success(f"Implied Volatility: {iv*100:.2f}%")

# -------------------------
# Heatmaps
# -------------------------
st.header("Options Price - Interactive Heatmap")
st.write("Explore how option prices fluctuate with varying stock prices and volatility levels.")

S_range = np.linspace(S_min, S_max, 10)
sigma_range = np.linspace(sigma_min, sigma_max, 10)

call_matrix = np.zeros((len(sigma_range), len(S_range)))
put_matrix = np.zeros((len(sigma_range), len(S_range)))

for i, s in enumerate(sigma_range):
    for j, stock in enumerate(S_range):
        call_matrix[i, j] = round(call_price(stock, K, T, r, s), 2)
        put_matrix[i, j] = round(put_price(stock, K, T, r, s), 2)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Call Price Heatmap")
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    fig1.patch.set_facecolor('#0E1117')
    ax1.set_facecolor('#0E1117')
    sns.heatmap(call_matrix, annot=True, fmt=".2f",
                xticklabels=[f"{s:.0f}" for s in S_range],
                yticklabels=[f"{s:.2f}" for s in sigma_range],
                cmap="RdYlGn", ax=ax1, cbar_kws={'label': 'Call Price'})
    ax1.set_xlabel('Stock Price', color='white')
    ax1.set_ylabel('Volatility', color='white')
    ax1.tick_params(colors='white')
    st.pyplot(fig1)

with col2:
    st.subheader("Put Price Heatmap")
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    fig2.patch.set_facecolor('#0E1117')
    ax2.set_facecolor('#0E1117')
    sns.heatmap(put_matrix, annot=True, fmt=".2f",
                xticklabels=[f"{s:.0f}" for s in S_range],
                yticklabels=[f"{s:.2f}" for s in sigma_range],
                cmap="RdYlGn_r", ax=ax2, cbar_kws={'label': 'Put Price'})
    ax2.set_xlabel('Stock Price', color='white')
    ax2.set_ylabel('Volatility', color='white')
    ax2.tick_params(colors='white')
    st.pyplot(fig2)


# -------------------------
# Greeks Heatmaps
# -------------------------
st.header("Greeks Heatmaps")

delta_matrix = np.zeros((len(sigma_range), len(S_range)))
gamma_matrix = np.zeros((len(sigma_range), len(S_range)))

for i, s in enumerate(sigma_range):
    for j, stock in enumerate(S_range):
        delta_matrix[i, j] = round(delta(stock, K, T, r, s), 4)
        gamma_matrix[i, j] = round(gamma(stock, K, T, r, s), 4)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Delta Heatmap")
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    fig3.patch.set_facecolor('#0E1117')
    ax3.set_facecolor('#0E1117')
    sns.heatmap(delta_matrix, annot=True, fmt=".2f",
                xticklabels=[f"{s:.0f}" for s in S_range],
                yticklabels=[f"{s:.2f}" for s in sigma_range],
                cmap="RdYlGn", ax=ax3, cbar_kws={'label': 'Delta'})
    ax3.set_xlabel('Stock Price', color='white')
    ax3.set_ylabel('Volatility', color='white')
    ax3.tick_params(colors='white')
    st.pyplot(fig3)

with col2:
    st.subheader("Gamma Heatmap")
    fig4, ax4 = plt.subplots(figsize=(8, 6))
    fig4.patch.set_facecolor('#0E1117')
    ax4.set_facecolor('#0E1117')
    sns.heatmap(gamma_matrix, annot=True, fmt=".3f",
                xticklabels=[f"{s:.0f}" for s in S_range],
                yticklabels=[f"{s:.2f}" for s in sigma_range],
                cmap="RdYlGn", ax=ax4, cbar_kws={'label': 'Gamma'})
    ax4.set_xlabel('Stock Price', color='white')
    ax4.set_ylabel('Volatility', color='white')
    ax4.tick_params(colors='white')
    st.pyplot(fig4)

