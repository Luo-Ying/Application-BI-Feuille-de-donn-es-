import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tabulate import tabulate

from scriptGraphics.generateFileChart import generateFileChart


def draw_hist(data, xlabel, ylabel, title, file, log=False, dropNaN=True):
    if dropNaN:
        data = data.dropna(subset=[xlabel, ylabel])

    keys = list(data[xlabel].astype(str))
    values = list(data[ylabel].astype(int))

    fig, ax = plt.subplots(figsize=(20, 10))

    # Création de l'histogramme avec échelle logarithmique
    bars = ax.bar(keys, values, color="maroon", width=0.4, log=True)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    # Rotation des étiquettes de l'axe des x pour une meilleure lisibilité
    plt.xticks(rotation=45)

    # Ajout du nombre au-dessus des barres
    for bar in bars:
        height = bar.get_height()
        ax.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points de décalage vertical
                    textcoords="offset points",
                    ha='center', va='bottom')

    if log:
        plt.yscale("log")
        generateFileChart(file, xlabel, "hist_with_log")
    else:
        generateFileChart(file, xlabel, "hist")
    plt.show()


def draw_hist_with_errors(data, xlabel, ylabel, title, file, log=False, dropNaN=True):
    data['Group'] = data.apply(group_values, xlabel=xlabel, axis=1)
    grouped_data = data.groupby('Group')[ylabel].sum().reset_index()
    print(tabulate(grouped_data, headers='keys', tablefmt='psql'))
    draw_hist(grouped_data, 'Group', ylabel, title, file, log=log, dropNaN=dropNaN)


def group_values(row, xlabel):
    if pd.isnull(row[xlabel]) or row[xlabel] in ['NaN', 'None']:
        return 'Valeurs vides'
    elif (isinstance(row[xlabel], int) or isinstance(row[xlabel], float)) and row[xlabel] > 0: # Si lettre ['0', '1']
        return 'Valeurs correctes'
    # elif row[xlabel] in ['K', 'A', 'C', 'KA', 'AC', 'KC', 'KAC']: # Si lettre ['0', '1']
    #     return row[xlabel]
    else:
        return 'Valeurs erronées'


def draw_custom_hist(data, xlabel, ylabel, title, file, value_min, value_max, bin_size):
    # Calcul des bornes des tranches
    bins = np.arange(value_min, value_max + bin_size, bin_size)

    fig, ax = plt.subplots(figsize=(20, 10))

    counts, _, bars = ax.hist(data[ylabel], bins=bins, color="maroon", edgecolor='black')

    ax.set_xlabel(xlabel)
    ax.set_ylabel('Nombre d’occurrences')
    ax.set_title(title)

    # Définir les étiquettes de l'axe des x pour qu'elles correspondent au milieu de chaque tranche
    tick_labels = [f"{int(bins[i])}-{int(bins[i + 1])}" for i in range(len(bins) - 1)]
    plt.xticks(ticks=np.arange(value_min + bin_size / 2, value_max, bin_size), labels=tick_labels, rotation=45)

    # Ajout du nombre au-dessus des barres
    for count, bar in zip(counts, bars):
        height = bar.get_height()
        ax.annotate('{}'.format(int(count)),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points de décalage vertical
                    textcoords="offset points",
                    ha='center', va='bottom')

    plt.yscale("log")
    generateFileChart(file, xlabel, "hist")

    plt.show()
