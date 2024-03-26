# Import libraries
import matplotlib.pyplot as plt
import numpy as np


def draw_box_plot_without_log(data, xlabel, title):

    fig = plt.figure(figsize=(10, 7))

    # Creating plot
    plt.boxplot(data)

    plt.xticks([1], [""])
    plt.xlabel(xlabel)
    plt.title(title)

    # show plot
    plt.show()
