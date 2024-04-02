import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def draw_scatter_plots(df, xlabel, ylabel, title, xlog=None, ylog=None):

    fig, ax = plt.subplots(figsize=(20, 10))

    x = df[xlabel]
    y = df[ylabel]
    plt.scatter(x, y)

    if xlog:
        plt.xscale("log")
    if ylog:
        plt.yscale("log")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if isinstance(x, pd.Series):
        x = x.tolist()
    if isinstance(y, pd.Series):
        y = y.tolist()

    min_x_idx = x.index(min(x))
    max_x_idx = x.index(max(x))
    min_y_idx = y.index(min(y))
    max_y_idx = y.index(max(y))
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    median_x = np.median(x)
    median_y = np.median(y)

    print(mean_x)
    print(mean_y)
    for idx in {min_x_idx, max_x_idx, min_y_idx, max_y_idx}:
        plt.text(x[idx], y[idx], f"({x[idx]}, {y[idx]})", fontsize=9, ha="left")

    plt.text(
        mean_x,
        mean_y, f"Mean\n({mean_x:.2f}, {mean_y:.2f})", fontsize=9, ha="left"
    )
    plt.text(
        median_x,
        median_y,
        f"Median\n({median_x:.2f}, {median_y:.2f})",
        fontsize=9,
        ha="left",
    )

    plt.show()
