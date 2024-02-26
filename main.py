import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


def lire_csv_et_analyser(nom_fichier):
    nom_fichier_entree = f'Input\\{nom_fichier}.csv'
    # Charger le CSV en utilisant pandas
    return pd.read_csv(sys.path[0] + f'\\{nom_fichier_entree}', delimiter=',', low_memory=False)


def createTable(df):
    for col in df.columns:
        # Vérifier si la colonne spécifiée existe dans le CSV
        # if col not in df.columns:
        #     print(f"La colonne '{col}' n'existe pas dans le CSV.")
        #     return

        # Nombre total de lignes dans la colonne spécifiée
        nombre_total_lignes = len(df[col])

        # Nombre de lignes différentes
        nombre_lignes_differentes = df[col].nunique()

        # Nombre d'occurrences pour chaque valeur différente
        occurrences = df[col].value_counts()

        # Nombre de lignes vides et non vides dans la colonne spécifiée
        nombre_lignes_vides = df[col].isna().sum()
        nombre_lignes_non_vides = nombre_total_lignes - nombre_lignes_vides

        # Afficher les résultats
        # print(f"Nombre total de lignes dans la colonne '{col}': {nombre_total_lignes}")
        # print(f"Nombre de lignes différentes dans la colonne '{col}': {nombre_lignes_differentes}")
        # print(f"Occurrences pour chaque valeur différente dans la colonne '{col}':\n{occurrences}")

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

        resultats = pd.concat([resultats, resultats_occurrences], ignore_index=True)
        generateFile(nom_fichier, col, resultats)


def getType(column):
    print(f'{df[column].name} est de type {df[column].dtype}')


def createTable(column):
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


def draw():
    # pie_chart(df, 'onBehalf')
    print(topBest('awardPrice', 5))
    print(topWorst('awardPrice', 5))
    # table_plot('onBehalf')
    # box_plot('awardPrice')
    for column in df.columns:
        createTable(column)
        getType(column)
    #     print("")
    #     # print(topBest(column, 5))
    #     # print(topWorst(column, 5))
    #
    #     # line_chart(column, column2)
    #     # box_plot(column)
    #     # scatter_plot(column, 'another_column')
    #     pie_chart(column)


def line_chart(x_column, y_column):
    plt.figure(figsize=(10, 6))
    df_days_calories = pd.DataFrame(
        {x_column: df[x_column],
         y_column: df[y_column],
         }
    )
    ax = plt.gca()
    df_days_calories.plot(x=x_column, y=y_column, ax=ax)
    df_days_calories.plot(x='Subject', y='Grade', ax=ax)
    plt.show()


def box_plot(column):
    b_plot = df.boxplot(column=column)
    b_plot.plot()
    plt.show()


def scatter_plot(x_column, y_column):
    sc_plot = df.plot.scatter(x=x_column, y=y_column)
    sc_plot.plot()
    plt.show()


def pie_chart(column):
    plt.figure(figsize=(10, 6))
    plt.pie(df[column].value_counts(dropna=False), labels=df[column].unique(), autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Pie Chart')
    plt.show()


def topBest(column, n):
    print(f'Top {n} des meilleurs {column}')
    result = df[column].value_counts(dropna=False).reset_index(name='count')
    result_sorted = result.sort_values(by='count', ascending=False)
    return result_sorted.head(n)


def topWorst(column, n):
    print(f'Top {n} des pires {column}')
    result = df[column].value_counts(dropna=False).reset_index(name='count')
    result_sorted = result.sort_values(by='count', ascending=True)
    return result_sorted.head(n)


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
    # Exemple d'utilisation : python3 main.py Lots
    nom_fichier = sys.argv[1]
    df = lire_csv_et_analyser(nom_fichier)
    draw()
