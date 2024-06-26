# Import libraries
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd

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
    # plt.show()


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
            i + 0.1,
            whisker_low + 2,
            f"Whisker bas: {whisker_low:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
        )
        plt.text(
            i + 0.1,
            whisker_high,
            f"Whisker haut: {whisker_high:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
        )

    if log:
        plt.yscale("log")
        generateFileChart(file, title, "boxplot_with_log")
    else:
        generateFileChart(file, title, "boxplot")
    # show plot
    # plt.show()


def draw_box_plot_multiple_dense(
    data, xlabel, ylabel, title, file, log=False, dropNaN=True
):
    if dropNaN:
        data = data.dropna(subset=[xlabel, ylabel])

    data[ylabel] = data[ylabel].astype(float)

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
        # Moyenne
        # if y_max - y_min > 20:
        plt.text(
            i + 0.1,
            stats["50%"],
            f"Med: {stats['50%']:.2f}",
            va="center",
            ha="left",
        )
        plt.text(
            i + 0.4,
            stats["50%"],
            f"Moy: {stats['mean']:.2f}",
            va="center",
            ha="left",
        )
        # Min
        plt.text(
            i + 0.1,
            y_min / 1.2,
            f"{y_min:.2f}",
            va="center",
            ha="left",
            # backgroundcolor="w",
            color="blue",
        )
        # Max
        plt.text(
            i + 0.1,
            y_max * 1.2,
            f"{y_max:.2f}",
            va="center",
            ha="left",
            # backgroundcolor="w",
            color="red",
        )

    if log:
        plt.yscale("log")
        generateFileChart(file, title, "boxplot_with_log")
    else:
        generateFileChart(file, title, "boxplot")
    # show plot
    # plt.show()


def draw_box_plot_multiple_dense_show_moy_med_up_and_down(
    data, xlabel, ylabel, title, file, log=False, dropNaN=True
):
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
        # Moyenne
        # if y_max - y_min > 20:
        plt.text(
            i + 0.1,
            stats["75%"],
            f"Med: {stats['50%']:.2f}",
            va="center",
            ha="left",
        )
        plt.text(
            i + 0.1,
            stats["50%"],
            f"Moy: {stats['mean']:.2f}",
            va="center",
            ha="left",
        )
        # Min
        plt.text(
            i + 0.1,
            y_min / 1.2,
            f"{y_min:.2f}",
            va="center",
            ha="left",
            # backgroundcolor="w",
            color="blue",
        )
        # Max
        plt.text(
            i + 0.1,
            y_max * 1.2,
            f"{y_max:.2f}",
            va="center",
            ha="left",
            # backgroundcolor="w",
            color="red",
        )

    if log:
        plt.yscale("log")
        generateFileChart(file, title, "boxplot_with_log")
    else:
        generateFileChart(file, title, "boxplot")
    # show plot
    # plt.show()


def draw_multiple_box_plot(data, title, xlabel=None, ylabel=None):
    plt.boxplot(data.values(), labels=data.keys())
    plt.title(title)
    plt.xlabel(xlabel)
    plt.xticks(rotation=45)
    plt.ylabel(ylabel)
    plt.yscale("log")
    # plt.show()


def draw_box_plot_special(data, xlabel, ylabel, title, file, log=False, dropNaN=True):

    data[xlabel] = data[xlabel].astype(float)
    if dropNaN:
        data = data.dropna(subset=[xlabel, ylabel])

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
    # plt.show()


def draw_box_plot_multiple_numberTenders_NumberTendersSme(
    data, xlabel, ylabel, title, file, log=False, dropNaN=True, bin_width=5
):
    if dropNaN:
        data = data.dropna(subset=[xlabel, ylabel])

    # Determine the range for binning based on min and max of x values
    min_x, max_x = 5, data[xlabel].max()
    bins = np.arange(min_x - bin_width, max_x + bin_width, bin_width)

    # Create a new column 'x_bin' for the binned x values
    data["x_bin"] = pd.cut(data[xlabel], bins=bins, include_lowest=True, right=False)

    # Group the data by 'x_bin' and collect the y values in lists
    grouped_data = (
        data.groupby("x_bin")[ylabel].apply(list).reset_index(name="y_values")
    )

    fig, ax = plt.subplots(figsize=(20, 10))

    # Creating plot with binned x labels
    boxplot_elements = ax.boxplot(
        grouped_data["y_values"],
        patch_artist=True,
        labels=[str(interval) for interval in grouped_data["x_bin"]],
    )

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if log:
        plt.yscale("log")

    # Rotate the x-axis labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    # Annotate statistics for each bin
    for i, (interval, y_values) in enumerate(
        zip(grouped_data["x_bin"], grouped_data["y_values"]), start=1
    ):
        if y_values:  # Check if y_values list is not empty
            stats = pd.Series(y_values).describe()
            if "min" in stats.index and "max" in stats.index:
                y_min, y_max = stats["min"], stats["max"]
                median = stats["50%"]
                mean = stats["mean"]

                # Display the mean value
                plt.text(
                    i + 0.3,
                    median,
                    f"{median:.2f}",
                    va="center",
                    ha="left",
                    color="black",
                )
                # Display the min value
                plt.text(
                    i + 0.3,
                    y_min,
                    f"{y_min:.2f}",
                    va="center",
                    ha="left",
                    color="blue",
                )
                # Display the max value
                plt.text(
                    i + 0.3,
                    y_max + 10,
                    f"{y_max:.2f}",
                    va="center",
                    ha="left",
                    color="red",
                )
            else:
                print(f"No statistical data for {interval}")
        else:
            print(f"No data to plot for {interval}")

    # Save the plot
    plt.tight_layout()  # Adjust layout to fit everything nicely
    generateFileChart(file, title, "boxplot_with_log" if log else "boxplot")

    # plt.show()


def draw_box_plot_multiple_numberTenders_typeOfContract(
    data, xlabel, ylabel, title, file, log=False, dropNaN=True
):
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
        # Médiane
        plt.text(
            i + 0.1,
            20,
            f"Médiane: {stats['50%']:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
        )
        # Moyenne
        plt.text(
            i + 0.4,
            20,
            f"Moyenne: {stats['mean']:.2f}",
            va="center",
            ha="left",
            backgroundcolor="w",
        )
        # Min
        plt.text(
            i + 0.1,
            y_min / 1.2,
            f"{y_min:.2f}",
            va="center",
            ha="left",
            # backgroundcolor="w",
            color="blue",
        )
        # Max
        plt.text(
            i + 0.1,
            y_max * 1.1,
            f"{y_max:.2f}",
            va="center",
            ha="left",
            # backgroundcolor="w",
            color="red",
        )

    if log:
        plt.yscale("log")
        generateFileChart(file, title, "boxplot_with_log")
    else:
        generateFileChart(file, title, "boxplot")
    # show plot
    # plt.show()


def draw_box_plot_multiple_simple_stats(
    data, xlabel, ylabel, title, file, log=False, dropNaN=True
):
    if dropNaN:
        data = data.dropna(subset=[xlabel, ylabel])

    unique_values = data[xlabel].unique()
    data_to_plot = [data[data[xlabel] == val][ylabel] for val in unique_values]

    fig, ax = plt.subplots(figsize=(20, 10))

    # Creating plot
    boxplot_elements = ax.boxplot(
        data_to_plot, patch_artist=True, labels=[str(val) for val in unique_values]
    )
    selected_indices = [
        0,
        len(unique_values) // 2,
        len(unique_values) - 1,
    ]  # exemple: la première, la médiane et la dernière boîte
    stats = pd.DataFrame(
        index=unique_values[selected_indices], columns=["Median", "Mean"]
    )

    for i in selected_indices:
        val = unique_values[i]
        median_val = np.median(data[data[xlabel] == val][ylabel])
        mean_val = np.mean(data[data[xlabel] == val][ylabel])
        stats.loc[val, "Median"] = f"{median_val:.2f}"
        stats.loc[val, "Mean"] = f"{mean_val:.2f}"

    table = plt.table(
        cellText=stats.values,
        colLabels=stats.columns,
        rowLabels=stats.index,
        loc="bottom",
        bbox=[0.25, -0.2, 0.5, 0.1],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(6)
    table.scale(1, 1)

    plt.subplots_adjust(bottom=0.3)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if log:
        plt.yscale("log")
        generateFileChart(file, title, "boxplot_with_log")
    else:
        generateFileChart(file, title, "boxplot")
    # show plot
    # plt.show()


def draw_box_plot_multiple_simple_stats(
    data, xlabel, ylabel, title, file, log=False, dropNaN=True
):
    if dropNaN:
        data = data.dropna(subset=[xlabel, ylabel])

    unique_values = data[xlabel].unique()
    data_to_plot = [data[data[xlabel] == val][ylabel] for val in unique_values]

    fig, ax = plt.subplots(figsize=(20, 10))

    # Creating plot
    boxplot_elements = ax.boxplot(
        data_to_plot, patch_artist=True, labels=[str(val) for val in unique_values]
    )
    selected_indices = [
        0,
        len(unique_values) // 2,
        len(unique_values) - 1,
    ]  # exemple: la première, la médiane et la dernière boîte
    stats = pd.DataFrame(
        index=unique_values[selected_indices], columns=["Median", "Mean"]
    )

    for i in selected_indices:
        val = unique_values[i]
        median_val = np.median(data[data[xlabel] == val][ylabel])
        mean_val = np.mean(data[data[xlabel] == val][ylabel])
        stats.loc[val, "Median"] = f"{median_val:.2f}"
        stats.loc[val, "Mean"] = f"{mean_val:.2f}"

    table = plt.table(
        cellText=stats.values,
        colLabels=stats.columns,
        rowLabels=stats.index,
        loc="bottom",
        bbox=[0.25, -0.2, 0.5, 0.1],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(6)
    table.scale(1, 1)

    plt.subplots_adjust(bottom=0.3)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    if log:
        plt.yscale("log")
        generateFileChart(file, title, "boxplot_with_log")
    else:
        generateFileChart(file, title, "boxplot")
    # show plot
    # plt.show()


def draw_boxplot_special_replace_abnormal_value_awardDate_and_awardEstimatedDate(
    df, file, title
):
    df = df.dropna(subset=["awardPrice"])
    # Visualiser les moyennes en utilisant l'index comme label sur l'axe des x
    plt.figure(figsize=(14, 7))  # Ajustez la taille selon vos besoins
    sns.boxplot(x="group_id", y="awardPrice", data=df)

    # Ajuster les paramètres de l'axe des x pour améliorer la lisibilité
    plt.xticks(
        rotation=90,
        horizontalalignment="center",
        fontweight="light",
        fontsize="x-small",
    )

    # Ajouter des titres et des labels aux axes
    plt.title("Moyenne des awardPrice par groupe")
    plt.xlabel("Index du groupe")
    plt.ylabel("Moyenne des awardPrice")
    plt.yscale("log")
    # Afficher le graphique
    plt.tight_layout()  # Ajuste automatiquement les sous-tracés pour qu'ils tiennent dans la figure
    generateFileChart(file, title, "boxplot_with_log")
    # plt.show()
