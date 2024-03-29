import numpy as np
import matplotlib.pyplot as plt


def draw_bar(
    data,
    xlabel,
    ylabel,
    title,
    log=False,
    labelRotation=0,
    xtick_fontsize=10,
    annotation_text=None,
):
    keys = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    bars = plt.bar(keys, values, color="maroon", width=0.4, log=log)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.xticks(fontsize=xtick_fontsize)
    plt.xticks(rotation=labelRotation)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x(), yval + 5, yval)

    if annotation_text:
        plt.text(
            0.95,
            0.95,
            annotation_text,
            ha="right",
            va="top",
            transform=plt.gca().transAxes,
        )

    plt.show()
