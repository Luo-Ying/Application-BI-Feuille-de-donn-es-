import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate
import seaborn as sns

from scriptGraphics.generateFileChart import generateFileChart


def draw_bar(
    data,
    xlabel,
    ylabel,
    title,
    file,
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

    if log:
        plt.yscale("log")
        generateFileChart(file, xlabel, "hist_with_log")
    else:
        generateFileChart(file, xlabel, "hist")
    plt.show()


def draw_hist(data, xlabel, ylabel, title, file, log=False, dropNaN=True, top=True):
    if dropNaN:
        data[ylabel] = data[ylabel].astype(float)
        data = data.dropna(subset=[ylabel])

    keys = list(data[xlabel].astype(str))
    values = list(data[ylabel].astype(int))

    top_5 = data.groupby(xlabel).sum().nlargest(5, ylabel)
    legend_text = "Top 5:\n" + "\n".join(
        [f"{i + 1}. {cat}: {val[ylabel]}" for i, (cat, val) in enumerate(top_5.iterrows())])

    fig, ax = plt.subplots(figsize=(20, 10))

    # Création de l'histogramme avec échelle logarithmique
    bars = ax.bar(keys, values, color="maroon", width=0.4, log=True)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    # ax.set_title(title)

    plt.text(
        0.5,
        1.08,
        title,
        horizontalalignment="center",
        fontsize=20,
        transform=ax.transAxes,
    )

    # Rotation des étiquettes de l'axe des x pour une meilleure lisibilité
    plt.xticks(rotation=45)

    # Ajout du nombre au-dessus des barres
    for bar in bars:
        height = bar.get_height()
        ax.annotate(
            "{}".format(height),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  # 3 points de décalage vertical
            textcoords="offset points",
            ha="center",
            va="bottom",
            rotation=0,
        )

    if top:
        plt.legend(title=legend_text, loc='upper right')
    if log:
        plt.yscale("log")
        generateFileChart(file, xlabel, "hist_with_log")
    else:
        generateFileChart(file, xlabel, "hist")
    plt.show()


def draw_hist_with_errors(data, xlabel, ylabel, title, file, log=False, dropNaN=True):
    data[f"Group_{xlabel}"] = data.apply(group_values, xlabel=xlabel, axis=1)
    grouped_data = data.groupby(f"Group_{xlabel}")[ylabel].sum().reset_index()
    # print(tabulate(grouped_data, headers="keys", tablefmt="psql"))
    draw_hist(
        grouped_data, f"Group_{xlabel}", ylabel, title, file, log=log, dropNaN=dropNaN
    )


def group_values(row, xlabel):
    if pd.isnull(row[xlabel]) or row[xlabel] in ["NaN", "None", " "]:
        return "Valeurs vides"
    # elif row[xlabel] in ['S', 'U', 'W']:  # Si lettre ['0', '1']
    #     return row[xlabel]
    elif (isinstance(row[xlabel], int) or isinstance(row[xlabel], float)) and row[
        xlabel
    ] > 0:  # Si lettre ['0', '1']
        return "Valeurs correctes"
    # elif row[xlabel] in ['K', 'A', 'C', 'KA', 'AC', 'KC', 'KAC']: # Si lettre ['0', '1']
    #     return row[xlabel]
    # elif row[xlabel] in ['0', '1']:  # Si lettre ['0', '1']
    #     return row[xlabel]
    else:
        return "Valeurs erronées"


def draw_custom_hist(data, xlabel, ylabel, title, file, value_min, value_max, bin_size):
    # Calcul des bornes des tranches
    bins = np.arange(value_min, value_max + bin_size, bin_size)

    fig, ax = plt.subplots(figsize=(20, 10))

    counts, _, bars = ax.hist(
        data[ylabel], bins=bins, color="maroon", edgecolor="black"
    )

    ax.set_xlabel(xlabel)
    ax.set_ylabel("Nombre d’occurrences")
    ax.set_title(title)

    # Définir les étiquettes de l'axe des x pour qu'elles correspondent au milieu de chaque tranche
    tick_labels = [f"{int(bins[i])}-{int(bins[i + 1])}" for i in range(len(bins) - 1)]
    plt.xticks(
        ticks=np.arange(value_min + bin_size / 2, value_max, bin_size),
        labels=tick_labels,
        rotation=45,
    )

    # Ajout du nombre au-dessus des barres
    for count, bar in zip(counts, bars):
        height = bar.get_height()
        ax.annotate(
            "{}".format(int(count)),
            xy=(bar.get_x() + bar.get_width() / 2, height),
            xytext=(0, 3),  # 3 points de décalage vertical
            textcoords="offset points",
            ha="center",
            va="bottom",
        )

    plt.yscale("log")
    generateFileChart(file, xlabel, "hist")

    plt.show()


def draw_multiple_hist(
    data,
    xlabel,
    ylabel,
    title,
    file,
    log=False,
    dropNaN=True,
    rotation_annotation=None,
    rotation_xlabel=None,
    top=False,
):
    if dropNaN:
        data = data.dropna(subset=[xlabel, ylabel])

    top_5 = data.groupby(xlabel).sum().nlargest(5, 'count')
    legend_text = "Top 5:\n" + "\n".join(
        [f"{i + 1}. {cat}: {val['count']}" for i, (cat, val) in enumerate(top_5.iterrows())])

    sns_plot = sns.catplot(
        x=xlabel, y="count", hue=ylabel, data=data, kind="bar", height=6, aspect=2
    )

    for p in sns_plot.ax.patches:
        sns_plot.ax.annotate(
            format(p.get_height(), ".2f"),
            (p.get_x() + p.get_width() / 2.0, p.get_height()),
            ha="center",
            va="center",
            xytext=(0, 9),
            textcoords="offset points",
            rotation=rotation_annotation,
        )

    plt.xticks(rotation=rotation_xlabel)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.subplots_adjust(top=0.9)
    text = xlabel + "_" + ylabel

    if top:
        plt.legend(title=legend_text, loc='upper right')
    if log:
        plt.yscale("log")
        generateFileChart(file, text, "hist_with_log")
    else:
        generateFileChart(file, text, "hist")
    plt.show()


def hist_pivot(
    data,
    xlabel,
    ylabel,
    title,
    file,
    log=False,
    dropNaN=True,
    rotation_annotation=None,
    rotation_xlabel=None,):

    if dropNaN:
        data = data.dropna(subset=[xlabel, ylabel])

    df_pivot = data.pivot(index=xlabel, columns=ylabel, values=f'Nb{ylabel}').fillna(0)

    ax = df_pivot.plot(kind='bar', stacked=True, figsize=(20, 10))

    plt.xlabel(xlabel)
    plt.ylabel(f'Nombre de {ylabel}')
    plt.title(f'Histogramme cumulée des {ylabel} en fonction des {xlabel}')

    text = xlabel + "_" + ylabel

    totals = df_pivot.sum(axis=1)
    for rect in ax.patches:
        width, height = rect.get_width(), rect.get_height()
        x, y = rect.get_x(), rect.get_y()
        if height > 0:
            label_index = int(x + width / 2)
            total = totals.iloc[label_index]
            percentage = f'{height / total:.1%}'
            label = f'{int(height)} ({percentage})'
            ax.text(x + width / 2, y + height / 2, label, ha='center', va='center', fontsize=10, color='black')

    for i, total in enumerate(totals):
        ax.annotate(f"{total}", (i, total), ha='center', va='bottom', fontsize=10, color='black')

    plt.tight_layout()
    if log:
        plt.yscale("log")
        generateFileChart(file, text, "hist_pivot_with_log")
    else:
        generateFileChart(file, text, "hist_pivot")

    plt.show()


def hist_pivot_multplie(
    data,
    xlabel,
    ylabel,
    ylabel2,
    title,
    file,
    log=False,
    dropNaN=True,
    rotation_annotation=None,
    rotation_xlabel=None,):

    if dropNaN:
        data = data.dropna(subset=[xlabel, ylabel, ylabel2])

    # Calculer le nombre d'offres non-PME
    data['NbNonPme'] = data[ylabel] - data[ylabel2]

    # Création de l'histogramme
    ax = data.plot(x=xlabel,
                   y=[ylabel2, 'NbNonPme'],
                   kind='bar',
                   stacked=True,
                   figsize=(20, 10))

    plt.xlabel(xlabel)
    plt.ylabel('Nombre d’offres')
    plt.title(title)

    if rotation_xlabel is not None:
        plt.xticks(rotation=rotation_xlabel)

    for rect in ax.patches:
        width, height = rect.get_width(), rect.get_height()
        x, y = rect.get_x(), rect.get_y()
        if height > 0:
            label_index = int(x + width / 2)
            total = data[ylabel].iloc[label_index]
            percentage = f'{height / total:.1%}'
            label = f'{int(height)} ({percentage})'
            ax.text(x + width / 2, y + height / 2, label, ha='center', va='center', fontsize=10, color='black')

    for i, total in enumerate(data[ylabel]):
        ax.annotate(f"{total}", (i, total), ha='center', va='bottom', fontsize=10, color='black')

    text = xlabel + "_" + ylabel + "_" + ylabel2
    plt.tight_layout()
    if log:
        plt.yscale("log")
        generateFileChart(file, text, "hist_pivot_with_log")
    else:
        generateFileChart(file, text, "hist_pivot")

    plt.show()