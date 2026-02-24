import numpy as np
import time


def crr_parameters(S0, K, r, sigma, T, N, q=0.0):
    """
    Compute CRR binomial model parameters.
    """
    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp((r - q) * dt) - d) / (u - d)

    if p <= 0 or p >= 1:
        raise ValueError("Risk-neutral probability out of bounds. Adjust parameters.")

    return dt, u, d, p


def build_stock_tree(S0, u, d, N):
    """
    Construct stock price tree.
    """
    stock_tree = np.zeros((N + 1, N + 1))

    for i in range(N + 1):
        for j in range(i + 1):
            stock_tree[j, i] = S0 * (u ** (i - j)) * (d ** j)

    return stock_tree


def european_option_price(S0, K, r, sigma, T, N, option_type="call", q=0.0):
    dt, u, d, p = crr_parameters(S0, K, r, sigma, T, N, q)

    stock_tree = build_stock_tree(S0, u, d, N)
    option_tree = np.zeros((N + 1, N + 1))

    # Terminal payoff
    if option_type.lower() == "call":
        option_tree[:, N] = np.maximum(stock_tree[:, N] - K, 0)
    else:
        option_tree[:, N] = np.maximum(K - stock_tree[:, N], 0)

    # Backward induction
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            option_tree[j, i] = np.exp(-r * dt) * (
                p * option_tree[j, i + 1] +
                (1 - p) * option_tree[j + 1, i + 1]
            )

    return option_tree[0, 0]


def american_option_price(S0, K, r, sigma, T, N, option_type="call", q=0.0):
    dt, u, d, p = crr_parameters(S0, K, r, sigma, T, N, q)

    stock_tree = build_stock_tree(S0, u, d, N)
    option_tree = np.zeros((N + 1, N + 1))

    # Terminal payoff
    if option_type.lower() == "call":
        option_tree[:, N] = np.maximum(stock_tree[:, N] - K, 0)
    else:
        option_tree[:, N] = np.maximum(K - stock_tree[:, N], 0)

    # Backward induction with early exercise
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):

            continuation = np.exp(-r * dt) * (
                p * option_tree[j, i + 1] +
                (1 - p) * option_tree[j + 1, i + 1]
            )

            if option_type.lower() == "call":
                exercise = max(stock_tree[j, i] - K, 0)
            else:
                exercise = max(K - stock_tree[j, i], 0)

            option_tree[j, i] = max(continuation, exercise)

    return option_tree[0, 0]


def convergence_study(S0, K, r, sigma, T, max_steps,
                      option_type="call", q=0.0, step_size=10):

    steps_list = []
    american_prices = []
    european_prices = []
    runtimes = []

    for N in range(step_size, max_steps + 1, step_size):
        start = time.time()

        amer = american_option_price(
            S0, K, r, sigma, T, N, option_type, q
        )
        euro = european_option_price(
            S0, K, r, sigma, T, N, option_type, q
        )

        end = time.time()

        steps_list.append(N)
        american_prices.append(amer)
        european_prices.append(euro)
        runtimes.append(end - start)

    return {
        "steps": steps_list,
        "american": american_prices,
        "european": european_prices,
        "runtime": runtimes
    }
