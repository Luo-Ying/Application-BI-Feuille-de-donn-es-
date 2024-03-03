import pandas as pd
import sys
import os
import matplotlib.pyplot as plt

DTYPE_DICT_LOTS = {
    'lotId': 'Int64', 'tedCanId': 'Int64', 'correctionsNb': 'Int64', 'cancelled': 'Int64',
    'awardDate': 'object', 'awardEstimatedPrice': 'Float64', 'awardPrice': 'Float64',
    'cpv': 'Int64', 'numberTenders': 'Int64', 'onBehalf': 'object', 'jointProcurement': 'object',
    'fraAgreement': 'object', 'fraEstimated': 'object', 'lotsNumber': 'object',
    'accelerated': 'object', 'outOfDirectives': 'Int64', 'contractorSme': 'object',
    'numberTendersSme': 'Float64', 'subContracted': 'object', 'gpa': 'object',
    'multipleCae': 'object', 'typeOfContract': 'object', 'topType': 'object',
    'renewal': 'object', 'contractDuration': 'Float64', 'publicityDuration': 'Float64'
}


def read_csv(input_csv_path):
    if os.path.basename(input_csv_path) == 'Lots.csv':
        df = pd.read_csv(input_csv_path, dtype=DTYPE_DICT_LOTS, sep=',')
        column = read_user_column(df)
        diagram = choose_diagram()
        draw_diagram(diagram, df, column)
    else:
        print("Action par défaut")


def read_user_column(df):
    print("Voici les colonnes disponibles : ")
    for i, col in enumerate(df.columns):
        print(f"{i + 1}. {col}")

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


def choose_diagram():
    print(
        "Les diagrammes disponibles sont : Camembert, Combo chart, Line Chart, Top 5, Boite à moustaches, Nuage de points, Tableau, Gauge, Tree map")
    print("Veuillez choisir un type de diagramme : ")
    return input().lower()


def draw_diagram(diagram, df, column):
    if diagram == 'camembert':
        draw_pie_chart(df, column)
    elif diagram == 'tree map':
        draw_tree_map(df, column)
    elif diagram == 'box plot':
        draw_box_plot(df, column)
    elif diagram == 'tab':
        for nameColumn in df.columns:
            draw_table(df, nameColumn, os.path.basename(input_csv_path).replace('.csv', ''))
            getType(df, nameColumn)
    else:
        print("Le diagramme n'est pas encore disponible")


def draw_pie_chart(df, column):
    new_table_count = df[column].value_counts(dropna=False).reset_index(name='count')
    pie_labels = new_table_count[column]
    pie_values = new_table_count['count']

    fig, ax = plt.subplots()

    # Dessiner le diagramme en camembert
    ax.pie(pie_values, labels=pie_labels, autopct='%1.2f', startangle=90)

    # Aspect ratio - equal means pie is a circle
    ax.axis('equal')
    plt.show()


def draw_tree_map(df, column):
    import squarify

    new_table_count = df[column].value_counts(dropna=False).reset_index(name='count')
    tree_labels = new_table_count[column]
    tree_values = new_table_count['count']

    plt.figure(figsize=(10, 8))
    squarify.plot(sizes=tree_values, label=tree_labels, alpha=0.7)
    plt.axis('off')
    plt.show()


def draw_box_plot(df, column):
    plt.figure(figsize=(10, 8))
    df.boxplot(column=column)
    plt.title(f'Box plot - {column}')
    plt.show()


def draw_table(df, column, nom_fichier):
    # Vérifier si la colonne spécifiée existe dans le CSV
    # if col not in df.columns:
    #     print(f"La colonne '{col}' n'existe pas dans le CSV.")
    #     return

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


if __name__ == '__main__':
    input_csv_path = sys.argv[1] if len(sys.argv) > 1 else ""
    if input_csv_path:
        read_csv(input_csv_path)
    else:
        print("Veuillez fournir le chemin du fichier CSV en tant qu'argument de ligne de commande.")
