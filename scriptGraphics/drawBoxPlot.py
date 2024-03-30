# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from scriptGraphics.generateFileChart import generateFileChart


def draw_box_plot(data, xlabel, ylabel, title, file, log=False, dropNaN=True):
    data[xlabel] = data[xlabel].astype(float)

    if dropNaN:
        data = data.dropna(subset=[xlabel])

    fig, ax = plt.subplots(figsize=(20, 10))

    # Creating plot
    # warning : awardEstimatedPrice, awardPrice
    boxplot_elements = plt.boxplot(data[ylabel], patch_artist=True)

    plt.xticks([1], [xlabel])
    plt.ylabel(ylabel)
    plt.title(title)

    # Calcul et affichage des valeurs statistiques
    stats = data[ylabel].describe()
    y_min, y_max = stats["min"], stats["max"]

    whiskers = [item.get_ydata() for item in boxplot_elements["whiskers"]]
    whisker_low, whisker_high = whiskers[0][1], whiskers[1][1]

    # Place les annotations des statistiques clés
    plt.text(
        1.1,
        stats["25%"],
        f"Q1: {stats['25%']:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    plt.text(
        1.1,
        stats["50%"],
        f"Médiane: {stats['50%']:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    plt.text(
        1.3,
        stats["50%"],
        f"Moyenne: {stats['mean']:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    plt.text(
        1.1,
        stats["75%"],
        f"Q3: {stats['75%']:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    plt.text(
        1.1,
        y_min,
        f"Min: {y_min:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
        color="blue",
    )
    plt.text(
        1.1,
        y_max,
        f"Max: {y_max:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
        color="red",
    )
    plt.text(
        1.2,
        whisker_low,
        f"Whisker bas: {whisker_low:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    plt.text(
        1.2,
        whisker_high,
        f"Whisker haut: {whisker_high:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )

    if log:
        plt.yscale("log")
        generateFileChart(file, xlabel, "boxplot_with_log")
    else:
        generateFileChart(file, xlabel, "boxplot")
    # show plot
    plt.show()


def draw_box_plot_multiple(data, xlabel, ylabel, title, file, log=False, dropNaN=True):
    if dropNaN:
        data = data.dropna(subset=[xlabel, ylabel])

    unique_values = data[xlabel].unique()
    data_to_plot = [data[data[xlabel] == val][ylabel] for val in unique_values]

    fig, ax = plt.subplots(figsize=(20, 10))

    # Creating plot
    boxplot_elements = ax.boxplot(
        data_to_plot, patch_artist=True, labels=[str(val) for val in unique_values]
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    for i, val in enumerate(unique_values, start=1):
        stats = data[data[xlabel] == val][ylabel].describe()
        y_min, y_max = stats["min"], stats["max"]
        whiskers = [
            item.get_ydata()
            for item in boxplot_elements["whiskers"][2 * (i - 1) : 2 * i]
        ]
        whisker_low, whisker_high = whiskers[0][1], whiskers[1][1]

        plt.text(
            i + 0.1,
            stats["25%"],
            f"Q1: {stats['25%']:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
        )
        plt.text(
            i + 0.1,
            stats["50%"],
            f"Médiane: {stats['50%']:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
        )
        plt.text(
            i + 0.4,
            stats["50%"],
            f"Moyenne: {stats['mean']:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
        )
        plt.text(
            i + 0.1,
            stats["75%"],
            f"Q3: {stats['75%']:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
        )
        plt.text(
            i + 0.1,
            y_min,
            f"Min: {y_min:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
            color="blue",
        )
        plt.text(
            i + 0.1,
            y_max,
            f"Max: {y_max:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
            color="red",
        )
        plt.text(
            i + 0.2,
            whisker_low,
            f"Whisker bas: {whisker_low:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
        )
        plt.text(
            i + 0.2,
            whisker_high,
            f"Whisker haut: {whisker_high:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
        )

    if log:
        plt.yscale("log")
        generateFileChart(file, xlabel + "_" + ylabel, "boxplot_with_log")
    else:
        generateFileChart(file, xlabel + "_" + ylabel, "boxplot")
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


def draw_box_plot_special(data, xlabel, ylabel, title, file, log=False, dropNaN=True):

    data[xlabel] = data[xlabel].astype(float)

    if dropNaN:
        data = data.dropna(subset=[xlabel])

    # print(data.head())
    fig, ax = plt.subplots(figsize=(20, 10))

    boxplot_elements = plt.boxplot(data[ylabel], patch_artist=True)

    plt.xticks([1], [xlabel])
    plt.ylabel(ylabel)
    plt.title(title)

    # Calcul et affichage des valeurs statistiques
    stats = data[ylabel].describe()
    y_min, y_max = stats["min"], stats["max"]

    whiskers = [item.get_ydata() for item in boxplot_elements["whiskers"]]
    whisker_low, whisker_high = whiskers[0][1], whiskers[1][1]

    # Place les annotations des statistiques clés
    plt.text(
        1.1,
        stats["25%"],
        f"Q1: {stats['25%']:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    plt.text(
        1.1,
        stats["50%"],
        f"Médiane: {stats['50%']:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    plt.text(
        1.3,
        stats["50%"],
        f"Moyenne: {stats['mean']:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    # plt.text(
    #     1.1,
    #     y_max / 2,
    #     f"Moyenne: {stats['mean']:.2f}",
    #     va="center",
    #     ha="left",
    #     backgroundcolor="w",
    # )
    plt.text(
        1.1,
        stats["75%"],
        f"Q3: {stats['75%']:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    plt.text(
        1.1,
        y_min,
        f"Min: {y_min:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
        color="blue",
    )
    plt.text(
        1.1,
        y_max,
        f"Max: {y_max:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
        color="red",
    )
    plt.text(
        1.2,
        whisker_low,
        f"Whisker bas: {whisker_low:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    # plt.text(
    #     1.2,
    #     y_max / 4,
    #     f"Whisker bas: {whisker_low:.2f}",
    #     va="center",
    #     ha="left",
    #     backgroundcolor="w",
    # )
    plt.text(
        1.2,
        whisker_high,
        f"Whisker haut: {whisker_high:.2f}",
        va="center",
        ha="left",
        backgroundcolor="w",
    )
    # plt.text(
    #     1.2,
    #     y_max / 3,
    #     f"Whisker haut: {whisker_high:.2f}",
    #     va="center",
    #     ha="left",
    #     backgroundcolor="w",
    # )

    # awardPrice vs awardEstimatedPrice faut mettre
    # plt.text(1.1, y_max/2, f"Moyenne: {stats['mean']:.2f}", va='center', ha='left', backgroundcolor='w')
    # plt.text(1.2, y_max/4, f"Whisker bas: {whisker_low:.2f}", va='center', ha='left', backgroundcolor='w')
    # plt.text(1.2, y_max/3, f"Whisker haut: {whisker_high:.2f}", va='center', ha='left', backgroundcolor='w')

    if log:
        plt.yscale("log")
        generateFileChart(file, xlabel, "boxplot_with_log")
    else:
        generateFileChart(file, xlabel, "boxplot")
    # show plot
    plt.show()
