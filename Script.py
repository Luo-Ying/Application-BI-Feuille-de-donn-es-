import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plotter
import sys
import os
import math
import pygal
import lxml
import sqlite3

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

DTYPE_DICT_AGENTS = {
    "agentId": "Int64",
    "name": "object",
    "siret": "object",
    "address": "object",
    "city": "object",
    "zipcode": "object",
    "country": "object",
    "department": "object",
    "longitude": "object",
    "latitude": "object",
}

DTYPE_DICT_CRITERIA = {
    "criterionId": "Int64",
    "lotId": "Int64",
    "name": "object",
    "weight": "Float64",
    "type": "object"
}

DTYPE_DICT_LOTBUYERS = {
    "lotId": "Int64",
    "agentId": "Int64"
}

DTYPE_DICT_LOTSUPPLIERS = {
    "lotId": "Int64",
    "agentId": "Int64"
}

DTYPE_DICT_NAMES = {
    "agentId": "Int64",
    "name": ""
}

N = 50
all_columns = []
diagrams = ["camembert", f"top {N}", f"worst {N}", "nuage de points", "gauge", "radar", "tree map", "box plot",
            "violin plot",
            "histogram", "tab"]


def read_csv(input_csv_path):
    filename = os.path.basename(input_csv_path)
    if filename in ["Lots.csv", "Agents.csv", "Criteria.csv", "LotBuyers.csv", "LotSuppliers.csv", "Names.csv"]:
        df = pd.read_csv(input_csv_path, dtype=DTYPE_DICT_LOTS, sep=",")
        draw_Diagram(
            df, get_dtype(filename)
        )
    else:
        print("Action par defaut")


def get_dtype(filename):
    if filename == "Lots.csv":
        return DTYPE_DICT_LOTS
    elif filename == "Agents.csv":
        return DTYPE_DICT_AGENTS
    elif filename == "Criteria.csv":
        return DTYPE_DICT_CRITERIA
    elif filename == "LotBuyers.csv":
        return DTYPE_DICT_LOTBUYERS
    elif filename == "LotSuppliers.csv":
        return DTYPE_DICT_LOTSUPPLIERS
    elif filename == "Names.csv":
        return DTYPE_DICT_NAMES
    else:
        return


def read_user_column(df, dtype):
    print("Voici les colonnes disponibles : ")
    for i, col in enumerate(df.columns):
        print(f"{i + 1}. {col}")
        all_columns.append(col)

    user_input = input("Veuillez sélectionner une colonne par son nom ou son ID : ")

    try:
        # Essayer de convertir l'entrée en entier (ID)
        column_id = int(user_input)
        if 1 <= column_id <= len(df.columns):
            show_Column_Info(df, df.columns[column_id - 1], dtype)
            return df.columns[column_id - 1]
    except ValueError:
        # Si la conversion échoue, traiter l'entrée comme le nom de la colonne
        if user_input in df.columns:
            show_Column_Info(df, user_input, dtype)
            return user_input

    print("Entrée invalide. Veuillez choisir une colonne valide.")
    return read_user_column(df, dtype)


def show_Column_Info(df, column, dtype):
    print("\nDes ionformation global de la colonne >>>>>>> ")
    print(f"Colonne choisi: {column}")
    print(dtype[column])
    if dtype[column] == "Int64" or dtype[column] == "Float64":
        print(f"La valeur minimun : {get_Min_Value(df, column)}")
        print(f"La valeur maximum : {get_Max_Value(df, column)}")
        print(f"La valeur médianne : {get_median(df, column)}")
        print(f"La valeur mean : {get_Mean_Value(df, column)}")
        print(f"La valeur écart-type : {get_Standard_deviation(df, column)}")
    print("\n")


def choose_Diagram():
    print(
        "Les diagrammes disponibles sont : Camembert , Combo chart, Line Chart, Top 5, Boite moustache, Nuage de points, Tableau, Gauge, Tree map, Radar ")
    for i, col in enumerate(diagrams):
        print(f"{i + 1}. {col}")

    user_input = input("Veuillez sélectionner un diagramme par son nom ou son ID : ")

    try:
        # Essayer de convertir l'entrée en entier (ID)
        column_id = int(user_input)
        if 1 <= column_id <= len(diagrams):
            return diagrams[column_id - 1]
    except ValueError:
        # Si la conversion échoue, traiter l'entrée comme le nom de la colonne
        if user_input in diagrams:
            return user_input.lower()

    print("Veuillez choisir un diagramme valide.")
    return choose_Diagram().lower()


def draw_Diagram(df, dtype):
    next = True
    while next:
        column = read_user_column(df, dtype)
        diagram = choose_Diagram()
        if diagram == "camembert":
            draw_Pie_Chart(df, column, os.path.basename(input_csv_path).replace('.csv', ''))
        elif diagram == f"top {N}":
            get_Top5_Candidate(df, column, os.path.basename(input_csv_path).replace('.csv', ''))
        elif diagram == f"worst {N}":
            get_Worst5_Candidate(df, column, os.path.basename(input_csv_path).replace('.csv', ''))
        elif diagram == 'nuage de points':
            draw_Scatter_Chart(diagram, df, column, os.path.basename(input_csv_path).replace('.csv', ''))
        elif diagram == 'gauge':
            draw_Gauge_Chart(diagram, df, column, os.path.basename(input_csv_path).replace('.csv', ''))
        elif diagram == 'radar':
            draw_Radar_Chart(diagram, df, column, os.path.basename(input_csv_path).replace('.csv', ''))
        elif diagram == 'tree map':
            draw_tree_map(df, column, os.path.basename(input_csv_path).replace('.csv', ''))
        elif diagram == 'box plot':
            draw_box_plot(df, column, os.path.basename(input_csv_path).replace('.csv', ''))
        elif diagram == 'violin plot':
            draw_violin_plot(df, column, os.path.basename(input_csv_path).replace('.csv', ''))
        elif diagram == 'histogram':
            draw_hist(df, column, os.path.basename(input_csv_path).replace('.csv', ''))
        elif diagram == 'tab':
            for nameColumn in df.columns:
                draw_table(df, nameColumn, os.path.basename(input_csv_path).replace('.csv', ''))
                getType(df, nameColumn)
        else:
            print("Il faut choisir un diagramme pour déssiner.")
        print("Continuer ? (n/y)")
        next = True if input() == "y" else False


# Les graphes qui peuvent être des camemberts sont : correctionsNb, cancelled, onBehalf, jointProcurement, fraAgreement, fraEstimated
def draw_Pie_Chart(df, column, nom_fichier):
    # newTableCount = df[column].value_counts(dropna=False).reset_index(name='count')
    # pieLabels = newTableCount[column]
    # pieValues = newTableCount['count']

    nombre_total_lignes = len(df[column])
    nombre_lignes_vides = df[column].isna().sum()
    nombre_lignes_non_vides = nombre_total_lignes - nombre_lignes_vides

    resultats = pd.DataFrame({
        'count': [nombre_lignes_vides, nombre_lignes_non_vides]},
        index=['Nombre de lignes vides', 'Nombre de lignes vides'])

    # numeric_values = pd.to_numeric(df[column], errors='coerce')
    # nb_integers = numeric_values[pd.notna(numeric_values)].astype(int).count()
    #
    # nb_strings = nombre_total_lignes - nb_integers - nombre_lignes_vides
    #
    # resultats = pd.DataFrame({
    #     'count': [nombre_lignes_vides, nb_integers, nb_strings]},
    #     index=['Nombre de lignes vides', 'Nombre de lignes correctes', 'Nombre d\'erreurs'])

    figureObject, axesObject = plotter.subplots()

    # Draw the pie chart
    # axesObject.pie(pieValues, labels=pieLabels, autopct='%1.2f', startangle=90)
    axesObject.pie(resultats['count'], labels=resultats.index, autopct='%1.2f', startangle=90)

    # Aspect ratio - equal means pie is a circle
    axesObject.axis('equal')
    generateFileChart(nom_fichier, column, "pieChart")
    plotter.show()


# Graphs cpv, numberTenders,lotsNumber, numberTendersSme, contractorSme, contractDuration, publicityDuration works but takes time and is incomprehensible, must zoom to see clearly
# Graphs with too many labels and values do not work. Maybe should group labels?
def draw_Scatter_Chart(diagram, df, column, nom_fichier):
    newTableCount = df[column].value_counts(dropna=False).reset_index(name='count')
    pieLabels = newTableCount[column].astype(str)

    # Can work with mean average, variances , etc.. Not just count, should discuss with the group
    pieValues = newTableCount['count']

    # Define the axes
    # plotter.scatter(pieLabels, pieValues)
    # plotter.axvline(x=19, color='r', linewidth=1)
    plotter.scatter(pieLabels.head(20), pieValues.head(20))

    # Draw the scatter chart
    plotter.title('Nuage de points')
    plotter.xlabel('Labels')
    plotter.ylabel('Compte')
    generateFileChart(nom_fichier, column, "nuageDePoints")
    plotter.show()


# Radars work with columns having few labels else it is horrible :(
def draw_Radar_Chart(diagram, df, column, nom_fichier):
    newTableCount = df[column].value_counts(dropna=False).reset_index(name='count')
    pieLabels = newTableCount[column].astype(str)
    pieValues = newTableCount['count']

    # Calculate angle for each segment
    angles = np.linspace(0, 2 * np.pi, len(pieLabels), endpoint=False).tolist()
    pieValues = pieValues.tolist()
    pieValues += pieValues[:1]
    angles += angles[:1]

    # Draw the radar
    fig, ax = plotter.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, pieValues, color='skyblue', alpha=0.7)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(pieLabels)
    ax.set_yticklabels([])
    ax.set_title('Radar')
    # ax.set_rscale('symlog', linthresh=0.01)
    generateFileChart(nom_fichier, column, "radar")
    plotter.show()


def draw_Gauge_Chart(diagram, df, column, nom_fichier):
    newTableCount = df[column].value_counts(dropna=False).reset_index(name='count')
    pieLabels = newTableCount[column].astype(str)
    pieValues = newTableCount['count']
    maxValue = sum(pieValues)

    # Draw the gauge
    gauge = pygal.SolidGauge(
        half_pie=True, inner_radius=0.70,
        style=pygal.style.styles['default'](value_font_size=10))

    formatter = lambda x: '{:.10g}'.format(x)

    # Maybe should be more interesting to do top 5 or top 10
    for i, value in enumerate(pieLabels):
        gauge.add(value, [{'value': pieValues[i], 'max_value': maxValue}], formatter=formatter)

    generateFileChart(nom_fichier, column, "gauge")
    gauge.render_in_browser()


def get_Top5_Candidate(df, column, nom_fichier):
    # df[column] = pd.to_numeric(df[column], errors='coerce')
    table = df.nlargest(n=N, columns=[column])

    x = ["Candidat " + str(n) for n in range(N, 0, -1)]

    # getting values against each value of y
    y = table[column].to_list()
    y.reverse()
    print(x)

    # plotter.xscale("log")
    plotter.barh(x, y)

    for index, value in enumerate(y):
        plotter.text(value, index, str(value))

    index_labels = ["Candidat " + str(n) for n in range(1, N + 1)]
    table = pd.DataFrame(data=table.values, index=index_labels, columns=all_columns)
    print(table)

    generateFileChart(nom_fichier, column, "top")
    plotter.show()


def get_Worst5_Candidate(df, column, nom_fichier):
    table = df.nsmallest(n=N, columns=[column])

    x = ["Candidat " + str(n) for n in range(N)]

    # getting values against each value of y
    y = table[column].to_list()
    print(x)

    plotter.barh(x, y)

    for index, value in enumerate(y):
        plotter.text(value, index, str(value))

    index_labels = ["Candidat " + str(n) for n in range(1, N + 1)]
    table = pd.DataFrame(data=table.values, index=index_labels, columns=all_columns)
    print(table)

    generateFileChart(nom_fichier, column, "worst")
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


def draw_tree_map(df, column, nom_fichier):
    import squarify

    new_table_count = df[column].value_counts(dropna=False).reset_index(name='count')
    tree_labels = new_table_count[column]
    tree_values = new_table_count['count']

    plotter.figure(figsize=(10, 8))
    squarify.plot(sizes=tree_values, label=tree_labels, alpha=0.7)
    plotter.axis('off')
    generateFileChart(nom_fichier, column, "treeMap")
    plotter.show()


def draw_box_plot(df, column, nom_fichier):
    newTableCount = df[column].value_counts(dropna=False).reset_index(name='count')
    plotter.figure(figsize=(10, 8))
    newTableCount.boxplot(column=column)
    plotter.title(f'Box plot - {column}')
    plotter.yscale("log")
    generateFileChart(nom_fichier, column, "boxPlot")
    plotter.show()


def draw_violin_plot(df, column, nom_fichier):
    newTableCount = df[column].value_counts(dropna=False).reset_index(name='count')
    plotter.figure(figsize=(10, 8))
    sns.violinplot(data=newTableCount[column])
    plotter.title(f'Violin plot - {column}')
    # plotter.yscale("log")
    generateFileChart(nom_fichier, column, "violinPlot")
    plotter.show()


def draw_hist(df, column, nom_fichier):
    if column == 'numberTendersSme':
        newTableCount = df[column].value_counts(dropna=False).reset_index(name='count')
        # plotter.hist(newTableCount['count'], bins=[0,100,200,300,400,500,600,700,800,900,1000] , color='skyblue', edgecolor='black')
        plotter.hist(newTableCount['count'], bins=[0, 200, 400, 600, 800, 1000],
                     color='skyblue', edgecolor='black', log=True)
        plotter.xlabel(f'Number of occurences of {column} with intervals 200')
        plotter.ylabel('Frequency')
        plotter.title(f'Histogram occurencies of {column}')
        generateFileChart(nom_fichier, column, "hist")
        plotter.show()
    elif column == 'lotsNumber':
        nombre_total_lignes = len(df[column])
        nombre_lignes_vides = df[column].isna().sum()
        numeric_values = pd.to_numeric(df[column], errors='coerce')
        nb_integers = numeric_values[pd.notna(numeric_values)].astype(int).count()

        nb_strings = nombre_total_lignes - nb_integers - nombre_lignes_vides

        resultats = pd.DataFrame({
            'count': [nombre_lignes_vides, nb_integers, nb_strings],
            'nb': ['Nombre de lignes vides', 'Nombre de lignes correctes', 'Nombre d\'erreurs']})

        plotter.bar(resultats['nb'].astype(str), resultats['count'], color='skyblue', edgecolor='black')
        plotter.title(f'Histogramme - {column}')
        plotter.xlabel(column)
        plotter.ylabel('Fréquence')
        # plotter.yscale("log")
        generateFileChart(nom_fichier, column, "hist")
        plotter.show()
    else:
        newTableCount = df[column].value_counts(dropna=False).reset_index(name='count')
        # newTableCount[column].fillna('NaN', inplace=True)

        plotter.figure(figsize=(10, 8))
        plotter.bar(newTableCount[column].astype(str), newTableCount['count'], color='skyblue', edgecolor='black')
        plotter.title(f'Histogramme - {column}')
        plotter.xlabel(column)
        plotter.ylabel('Fréquence')
        plotter.yscale("log")
        generateFileChart(nom_fichier, column, "hist")
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

    if DTYPE_DICT_LOTS[column] == "Int64" or DTYPE_DICT_LOTS[column] == "Float64":
        mean_value = get_Mean_Value(df, column),
        min_value = get_Min_Value(df, column),
        max_value = get_Max_Value(df, column),
        median_value = get_median(df, column),
        std_dev = get_Standard_deviation(df, column)
        result_stats = pd.DataFrame({
            'Statistiques': ['Moyenne', 'Valeur Minimale', 'Valeur Maximale', 'Médiane', 'Écart type'],
            'Valeurs': [mean_value, min_value, max_value, median_value, std_dev]
        })
        print(result_stats)
        resultats = pd.concat([resultats, resultats_occurrences, result_stats], ignore_index=True)
    else:
        resultats = pd.concat([resultats, resultats_occurrences], ignore_index=True)

    generateFileTab(nom_fichier, column, resultats)


def getType(df, column):
    print(f'{df[column].name} est de type {df[column].dtype}')


def generateFileChart(nom_fichier, filename, type):
    nom_fichier_sortie = f'fig\\{nom_fichier}\\{nom_fichier}_{filename}_{type}'
    isExist = os.path.exists(sys.path[0] + f'\\fig')
    if not isExist:
        os.makedirs(sys.path[0] + f'\\fig')

    isExist = os.path.exists(sys.path[0] + f'\\fig\\{nom_fichier}')
    if not isExist:
        os.makedirs(sys.path[0] + f'\\fig\\{nom_fichier}')
    plotter.savefig(f'fig/{nom_fichier}/{nom_fichier}_{filename}_{type}')
    print(f"Résultats enregistrés dans {nom_fichier_sortie}")


def generateFileTab(nom_fichier, filename, content):
    # Enregistrer les résultats dans un fichier CSV
    extension = 'output'
    nom_fichier_sortie = f'Output\\{nom_fichier}\\{nom_fichier}_{filename}_{extension}.csv'

    isExist = os.path.exists(sys.path[0] + f'\\Output\\{nom_fichier}')
    if not isExist:
        os.makedirs(sys.path[0] + f'\\Output\\{nom_fichier}')

    content.to_csv(sys.path[0] + f'\\{nom_fichier_sortie}', index=False)
    print(f"Résultats enregistrés dans {nom_fichier_sortie}")


def connect_db(db_path):
    return sqlite3.connect(db_path)


def close_db(connexion):
    connexion.close()


def get_sql_request(connexion):
    cursor = connexion.cursor()
    # SELECT * FROM Lots LIMIT 5;
    query_select = input("Entrer votre SQL: ")
    cursor.execute(query_select)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


if __name__ == "__main__":
    db_path = 'Input\\Foppa.db'
    connexion = connect_db(db_path)
    get_sql_request(connexion)
    close_db(connexion)

    input_csv_path = sys.argv[1]
    read_csv(input_csv_path)
