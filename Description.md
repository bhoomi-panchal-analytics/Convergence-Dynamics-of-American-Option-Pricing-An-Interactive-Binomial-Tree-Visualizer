# Convergence-Dynamics-of-American-Option-Pricing-An-Interactive-Binomial-Tree-Visualizer
Build a Python-based interactive visualization that shows how the American option price converges as the number of binomial steps increases. Also compare it to the European price and optionally Black–Scholes.


1. Objective

**To build an interactive Streamlit web application that:**
Visualizes the binomial tree structure for underlying asset price evolution.
Prices American call and put options using the Cox-Ross-Rubinstein (CRR) binomial model.
Demonstrates how the option price converges numerically as the number of time steps increases.

**Provides intuition behind:**
Early exercise premium (American vs European)
Backward induction
Discrete-time approximation of continuous-time pricing

The aim is educational and analytical: to bridge theoretical pricing models with computational implementation.

2. Problem Statement

**Closed-form solutions such as the Fischer Black–Myron Scholes–Robert C. Merton framework (Black-Scholes-Merton) assume European-style exercise and continuous time. However**:
American options allow early exercise.
No closed-form solution exists for American puts under Black-Scholes.
Numerical methods are required.

**The binomial tree provides:**
A discrete-time approximation of geometric Brownian motion.
A practical framework for American option pricing via backward induction.
A converging sequence toward theoretical continuous-time prices as steps increase.

**Core Research Question:**
How does the American option price converge as the number of binomial steps increases, and how does early exercise affect convergence behavior?

3. Key Financial Concepts Used

Risk-neutral valuation
No-arbitrage principle
Backward induction
Early exercise condition
Convergence to continuous-time models
Stability vs computational complexity trade-off


4. Data Needed

This is a model-based simulation. No external dataset is required.

**Inputs (user-controlled via Streamlit sliders):**
Initial stock price (S₀)
Strike price (K)
Risk-free rate (r)
Volatility (σ)
Time to maturity (T)
Number of steps (N)
Option type (Call / Put)

**Optional:**  
Dividend yield (q)

5. Mathematical Framework (CRR Model)

**For each time step:**
u = exp(σ√Δt)
d = 1/u
p = (e^(rΔt) − d) / (u − d)

**Terminal payoff:**
Call: max(S − K, 0)
Put: max(K − S, 0)

**Backward induction for American option:**
Value = max(Immediate exercise, Discounted expected value)

### repo
binomial-tree-visualizer/
│
├── app.py
├── pricing.py
├── visualization.py
├── utils.py
├── requirements.txt
├── README.md
├── LICENSE
└── assets/
