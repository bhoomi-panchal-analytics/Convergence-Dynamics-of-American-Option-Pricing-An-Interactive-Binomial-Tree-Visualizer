import streamlit as st
import numpy as np

from pricing import (
    american_option_price,
    european_option_price,
    convergence_study,
    build_stock_tree,
    crr_parameters
)

from visualization import (
    plot_stock_tree,
    plot_convergence,
    plot_runtime
)

st.set_page_config(layout="wide")

st.title("Binomial Tree Visualizer – American Option Convergence")

st.sidebar.header("Model Parameters")

S0 = st.sidebar.number_input("Initial Stock Price (S0)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05)
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2)
T = st.sidebar.number_input("Time to Maturity (T in years)", value=1.0)
q = st.sidebar.number_input("Dividend Yield (q)", value=0.0)

N = st.sidebar.slider("Number of Steps (Tree Visualization)", 1, 50, 10)
max_steps = st.sidebar.slider("Max Steps for Convergence Study", 50, 1000, 300)

option_type = st.sidebar.selectbox("Option Type", ["call", "put"])

st.subheader("Single-Step Pricing Result")

amer_price = american_option_price(S0, K, r, sigma, T, N, option_type, q)
euro_price = european_option_price(S0, K, r, sigma, T, N, option_type, q)

col1, col2 = st.columns(2)

col1.metric("American Option Price", round(amer_price, 4))
col2.metric("European Option Price", round(euro_price, 4))

st.write("Early Exercise Premium:",
         round(amer_price - euro_price, 6))

# -------------------------------------------------
# Tree Visualization (Small N Only)
# -------------------------------------------------

if N <= 15:
    dt, u, d, p = crr_parameters(S0, K, r, sigma, T, N, q)
    stock_tree = build_stock_tree(S0, u, d, N)
    fig_tree = plot_stock_tree(stock_tree, N)
    st.pyplot(fig_tree)
else:
    st.warning("Tree visualization limited to N ≤ 15 for clarity.")

# -------------------------------------------------
# Convergence Study
# -------------------------------------------------

st.subheader("Convergence Study")

data = convergence_study(
    S0, K, r, sigma, T,
    max_steps=max_steps,
    option_type=option_type,
    q=q,
    step_size=10
)

fig_conv = plot_convergence(data)
st.pyplot(fig_conv)

st.subheader("Runtime Analysis")

fig_runtime = plot_runtime(data)
st.pyplot(fig_runtime)

st.write("Time complexity grows approximately O(N²).")
