import numpy as np
from scipy.stats import norm


# ---------------------------------------------------
# Parameter Validation
# ---------------------------------------------------

def validate_inputs(S0, K, r, sigma, T, N):
    """
    Basic sanity checks for model inputs.
    """
    if S0 <= 0:
        raise ValueError("Initial stock price must be positive.")
    if K <= 0:
        raise ValueError("Strike price must be positive.")
    if sigma <= 0:
        raise ValueError("Volatility must be positive.")
    if T <= 0:
        raise ValueError("Time to maturity must be positive.")
    if N <= 0:
        raise ValueError("Number of steps must be positive.")


def check_no_arbitrage(r, sigma, T, N):
    """
    Check risk-neutral probability bounds indirectly.
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    if not (0 < p < 1):
        raise ValueError("Arbitrage condition violated: adjust N or parameters.")


# ---------------------------------------------------
# Black–Scholes European Benchmark
# ---------------------------------------------------

def black_scholes_price(S0, K, r, sigma, T, option_type="call", q=0.0):
    """
    Closed-form European option price.
    Useful for convergence comparison.
    """

    d1 = (
        np.log(S0 / K)
        + (r - q + 0.5 * sigma**2) * T
    ) / (sigma * np.sqrt(T))

    d2 = d1 - sigma * np.sqrt(T)

    if option_type.lower() == "call":
        price = (
            S0 * np.exp(-q * T) * norm.cdf(d1)
            - K * np.exp(-r * T) * norm.cdf(d2)
        )
    else:
        price = (
            K * np.exp(-r * T) * norm.cdf(-d2)
            - S0 * np.exp(-q * T) * norm.cdf(-d1)
        )

    return price


# ---------------------------------------------------
# Formatting Helpers
# ---------------------------------------------------

def format_price(value):
    return round(float(value), 6)


def percentage_error(model_price, benchmark_price):
    return abs(model_price - benchmark_price) / benchmark_price * 100
