import numpy as np
import matplotlib.pyplot as plt


def plot_stock_tree(stock_tree, N):
    """
    Plot binomial stock price tree (small N recommended: <= 15)
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(N + 1):
        for j in range(i + 1):
            ax.scatter(i, stock_tree[j, i])
            ax.text(i, stock_tree[j, i],
                    f"{stock_tree[j, i]:.2f}",
                    fontsize=8)

            if i > 0:
                # connect to previous nodes
                if j < i:
                    ax.plot([i - 1, i],
                            [stock_tree[j, i - 1],
                             stock_tree[j, i]],
                            linewidth=0.5)
                if j > 0:
                    ax.plot([i - 1, i],
                            [stock_tree[j - 1, i - 1],
                             stock_tree[j, i]],
                            linewidth=0.5)

    ax.set_title("Binomial Stock Price Tree")
    ax.set_xlabel("Time Step")
    ax.set_ylabel("Stock Price")
    ax.grid(True)

    return fig


def plot_convergence(data):
    """
    Plot American and European convergence
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(data["steps"], data["american"], label="American")
    ax.plot(data["steps"], data["european"], label="European")

    ax.set_title("Option Price Convergence")
    ax.set_xlabel("Number of Steps (N)")
    ax.set_ylabel("Option Price")
    ax.legend()
    ax.grid(True)

    return fig


def plot_runtime(data):
    """
    Plot runtime vs steps
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(data["steps"], data["runtime"])

    ax.set_title("Runtime Complexity")
    ax.set_xlabel("Number of Steps (N)")
    ax.set_ylabel("Computation Time (seconds)")
    ax.grid(True)

    return fig
