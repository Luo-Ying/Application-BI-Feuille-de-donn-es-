# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def draw_box_plot(data, xlabel, ylabel, title, log=None):

    fig = plt.figure(figsize=(10, 7))

    # Creating plot
    bp = plt.boxplot(data)

    plt.xticks([1], [""])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if log:
        plt.yscale("log")

    for i, box in enumerate(bp["boxes"]):
        # Minimum value
        plt.text(
            i + 1,
            np.min(data[i]),
            f"{np.min(data[i]):.2f}",
            verticalalignment="bottom",
            horizontalalignment="center",
            fontsize=10,
        )
        # Median value
        plt.text(
            i + 1,
            np.median(data[i]),
            f"{np.median(data[i]):.2f}",
            verticalalignment="bottom",
            horizontalalignment="center",
            fontsize=10,
        )
        # Mean value
        plt.text(
            i + 1,
            np.mean(data[i]),
            f"{np.mean(data[i]):.2f}",
            verticalalignment="bottom",
            horizontalalignment="center",
            fontsize=10,
        )
        # Maximum value
        plt.text(
            i + 1,
            np.max(data[i]),
            f"{np.max(data[i]):.2f}",
            verticalalignment="top",
            horizontalalignment="center",
            fontsize=10,
        )

    for i, flier in enumerate(bp["fliers"]):
        for value in flier.get_ydata():
            plt.text(
                i + 1,
                value,
                f"{value:.2f}",
                verticalalignment="bottom",
                horizontalalignment="center",
                fontsize=10,
            )

    # show plot
    plt.show()


def draw_multiple_box_plot(data, title, xlabel=None, ylabel=None):
    plt.boxplot(data.values(), labels=data.keys())
    plt.title(title)
    plt.xlabel(xlabel)
    plt.xticks(rotation=45)
    plt.ylabel(ylabel)
    plt.yscale("log")
    plt.show()
