import matplotlib.pyplot as plt
import numpy as np


def draw_line_chart(x, y, xlabel, ylabel, title, xlog=None, ylog=None):

    fig, ax = plt.subplots(figsize=(20, 10))

    # Plotting the line chart
    plt.plot(x, y, marker="o", markersize=8, linestyle="-", linewidth=2)

    if xlog:
        plt.xscale("log")
    if ylog:
        plt.yscale("log")

    # Adding title and labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    # Displaying the plot
    plt.grid(True)
    # plt.show()
