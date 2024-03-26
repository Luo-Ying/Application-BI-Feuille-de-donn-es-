import numpy as np
import matplotlib.pyplot as plt


def draw_hist_without_log(data, xlabel, ylabel, title):
    keys = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(keys, values, color="maroon", width=0.4)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def draw_hist_with_log(data, xlabel, ylabel, title):
    keys = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(keys, values, color="maroon", width=0.4, log=True)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()
