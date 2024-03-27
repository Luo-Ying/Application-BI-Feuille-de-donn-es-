# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


def draw_box_plot_without_log(data, xlabel, title):

    fig = plt.figure(figsize=(10, 7))

    # Creating plot
    plt.boxplot(data)

    plt.xticks([1], [""])
    plt.xlabel(xlabel)
    plt.title(title)

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
