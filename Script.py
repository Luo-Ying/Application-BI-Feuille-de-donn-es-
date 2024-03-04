import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plotter
import math

DTYPE_DICT_LOTS = {
    "lotId": "Int64",
    "tedCanId": "Int64",
    "correctionsNb": "Int64",
    "cancelled": "Int64",
    "awardDate": "object",
    "awardEstimatedPrice": "Float64",
    "awardPrice": "Float64",
    "cpv": "Int64",
    "numberTenders": "Int64",
    "onBehalf": "object",
    "jointProcurement": "object",
    "fraAgreement": "object",
    "fraEstimated": "object",
    "lotsNumber": "object",
    "accelerated": "object",
    "outOfDirectives": "Int64",
    "contractorSme": "object",
    "numberTendersSme": "Float64",
    "subContracted": "object",
    "gpa": "object",
    "multipleCae": "object",
    "typeOfContract": "object",
    "topType": "object",
    "renewal": "object",
    "contractDuration": "Float64",
    "publicityDuration": "Float64",
}


all_columns = []

def read_csv(input_csv_path):
    match os.path.basename(input_csv_path):
        case "Lots.csv":
            df = pd.read_csv(input_csv_path, dtype=DTYPE_DICT_LOTS, sep=",")
            draw_Diagram(
                df, DTYPE_DICT_LOTS
            )
        case _:
            print("Action par defaut")

def read_user_column(df, dtype):
    print("Voici les colonnes disponibles : ")
    for i, col in enumerate(df.columns):
        print(f"{i + 1}. {col}")
        all_columns.append(col)

    print("Veuillez sélectionner une colonne par son nom ou son ID : ")
    user_input = input()

    try:
        # Essayer de convertir l'entrée en entier (ID)
        column_id = int(user_input)
        if 1 <= column_id <= len(df.columns):
            return df.columns[column_id - 1]
    except ValueError:
        # Si la conversion échoue, traiter l'entrée comme le nom de la colonne
        if user_input in df.columns:
            return user_input

    print("Entrée invalide. Veuillez choisir une colonne valide.")
    return read_user_column(df)

def choose_Diagram():
    print(
        "Les diagrammes disponibles sont : Camembert , Combo chart, Line Chart, Top 5, Boite moustache, Nuage de points, Tableau, Gauge, Tree map "
    )
    print("Veuillez choisir un type de diagramme : ")
    return input().lower()


# J'ai bougé les fonctions read_user_column(df) et choose_Diagram() ici dans la fonction draw_Diagram(df) Parce qu'on va faire plusieurs graphe dans un même programme --Yingqi
def draw_Diagram(df, dtype):
    next = True
    while next:
        column = read_user_column(df, dtype)
        diagram = choose_Diagram()
        match diagram:
            case "camembert":
                draw_Pie_Chart(df, column)
            case "top 5":
                get_Top5_Candidate(df, column)
            case "worst 5":
                get_Worst5_Candidate(df, column)
            case 'tree map':
                draw_tree_map(df, column)
            case 'box plot':
                draw_box_plot(df, column)
            case 'tab':
                for nameColumn in df.columns:
                    draw_table(df, nameColumn, os.path.basename(input_csv_path).replace('.csv', ''))
                    getType(df, nameColumn)
            case _:
                print("Il faut choisir un diagramme pour déssiner.")
        print("Continuer ? (n/y)")
        next = True if input() == "y" else False


# Les graphes qui peuvent être des camemberts sont : correctionsNb, cancelled, onBehalf, jointProcurement, fraAgreement, fraEstimated
def draw_Pie_Chart(diagram, df, column):
    newTableCount = df[column].value_counts(dropna=False).reset_index(name='count')
    pieLabels = newTableCount[column]
    pieValues = newTableCount['count']

    figureObject, axesObject = plotter.subplots()

    # Draw the pie chart
    axesObject.pie(pieValues, labels=pieLabels, autopct='%1.2f', startangle=90)

    # Aspect ratio - equal means pie is a circle
    axesObject.axis('equal')
    plotter.show()


def get_Top5_Candidate(df, column):
    table = df.nlargest(n=5, columns=[column])

    x = ["Candidat " + str(n) for n in range(5, 0, -1)]

    # getting values against each value of y
    y = table[column].to_list()
    y.reverse()
    print(x)

    plotter.xscale("log")
    plotter.barh(x, y)

    for index, value in enumerate(y):
        plotter.text(value, index, str(value))

    index_labels = ["Candidat " + str(n) for n in range(1, 6)]
    table = pd.DataFrame(data=table.values, index=index_labels, columns=all_columns)
    print(table)

    plotter.show()


def get_Worst5_Candidate(df, column):
    table = df.nsmallest(n=5, columns=[column])

    x = ["Candidat " + str(n) for n in range(5)]

    # getting values against each value of y
    y = table[column].to_list()
    print(x)

    plotter.barh(x, y)

    for index, value in enumerate(y):
        plotter.text(value, index, str(value))
    plotter.show()


def get_Min_Value(df, column):
    return df[column].min()


def get_Max_Value(df, column):
    return df[column].max()


def get_Mean_Value(df, column):
    return df[column].mean()


def get_Standard_deviation(df, column):
    return df[column].std()


def get_median(df, column):
    return df[column].median()


def draw_tree_map(df, column):
    import squarify

    new_table_count = df[column].value_counts(dropna=False).reset_index(name='count')
    tree_labels = new_table_count[column]
    tree_values = new_table_count['count']

    plotter.figure(figsize=(10, 8))
    squarify.plot(sizes=tree_values, label=tree_labels, alpha=0.7)
    plotter.axis('off')
    plotter.show()


def draw_box_plot(df, column):
    plotter.figure(figsize=(10, 8))
    df.boxplot(column=column)
    plotter.title(f'Box plot - {column}')
    plotter.show()


def draw_table(df, column, nom_fichier):

    # Nombre total de lignes dans la colonne spécifiée
    nombre_total_lignes = len(df[column])

    # Nombre de lignes différentes
    nombre_lignes_differentes = df[column].nunique()

    # Nombre d'occurrences pour chaque valeur différente
    occurrences = df[column].value_counts()

    # Nombre de lignes vides et non vides dans la colonne spécifiée
    nombre_lignes_vides = df[column].isna().sum()
    nombre_lignes_non_vides = nombre_total_lignes - nombre_lignes_vides

    # Créer un nouveau DataFrame pour stocker les résultats
    resultats = pd.DataFrame({
        'Nombre total de lignes': [nombre_total_lignes],
        'Nombre de lignes différentes': [nombre_lignes_differentes],
        'Nombre de lignes vides': [nombre_lignes_vides],
        'Nombre de lignes non vides': [nombre_lignes_non_vides]
    })

    # Ajouter les colonnes d'occurrences au DataFrame
    resultats_occurrences = pd.DataFrame({
        'Occurrences': occurrences.index,
        'Nombre d\'occurrences': occurrences.values
    })

    # mean_value = df[column].mean()
    # min_value = df[column].min()
    # max_value = df[column].max()
    # median_value = df[column].median()
    # std_dev = df[column].std()

    # Create a DataFrame to store the statistics
    # result_stats = pd.DataFrame({
    #     'Statistic': ['Mean', 'Min', 'Max', 'Median', 'Standard Deviation'],
    #     'Value': [mean_value, min_value, max_value, median_value, std_dev]
    # })

    resultats = pd.concat([resultats, resultats_occurrences], ignore_index=True)

    generateFile(nom_fichier, column, resultats)


def getType(df, column):
    print(f'{df[column].name} est de type {df[column].dtype}')


def generateFile(nom_fichier, filename, content):
    # Enregistrer les résultats dans un fichier CSV
    extension = 'output'
    nom_fichier_sortie = f'Output\\{nom_fichier}\\{nom_fichier}_{filename}_{extension}.csv'

    isExist = os.path.exists(sys.path[0] + f'\\Output\\{nom_fichier}')
    if not isExist:
        os.makedirs(sys.path[0] + f'\\Output\\{nom_fichier}')

    content.to_csv(sys.path[0] + f'\\{nom_fichier_sortie}', index=False)
    print(f"Résultats enregistrés dans {nom_fichier_sortie}")


if __name__ == "__main__":
    input_csv_path = sys.argv[1]
    read_csv(input_csv_path)
