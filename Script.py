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

""" 
J'ai crée quand même une liste pour stocker les colonnes du fichier qui m'en sert plus tard, mais là je mets qu'un seul 
parce que pour moi on lance chaque fois le programme pour les fichiers différents
--Yingqi
"""
all_columns = []


def read_csv(input_csv_path):
    match os.path.basename(input_csv_path):
        case "Lots.csv":
            df = pd.read_csv(input_csv_path, dtype=DTYPE_DICT_LOTS, sep=",")
            draw_Diagram(
                df, DTYPE_DICT_LOTS
            )  # J'ai ajouter un paramètre encore de dictionnaire pour m'en servir dans la fonction de show_Column_Info(df, column, dtype) .. --Yingqi
        case _:
            print("Action par defaut")


def read_user_column(df, dtype):
    print("Voici les colonnes disponibles : ")
    for col in df.columns:
        print(col)
        all_columns.append(col)
    print("Veuillez selectionner une colonne : ")
    column_selected = input()
    show_Column_Info(df, column_selected, dtype)
    return column_selected


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
        "Les diagrammes disponibles sont : Camembert , Combo chart, Line Chart, Top 5, Boite moustache, Nuage de points, Tableau, Gauge, Tree map "
    )
    print("Veuillez choisir un type de diagramme : ")
    return input()


# J'ai bougé les fonctions read_user_column(df) et choose_Diagram() ici dans la fonction draw_Diagram(df) Parce qu'on va faire plusieurs graphe dans un même programme --Yingqi
def draw_Diagram(df, dtype):
    next = True
    while next:
        column = read_user_column(df, dtype)
        diagram = choose_Diagram()
        match diagram:
            case "Camembert":
                draw_Pie_Chart(df, column)
            case "Top 5":
                get_Top5_Candidate(df, column)
            case "Worst 5":
                get_Worst5_Candidate(df, column)
            case _:
                print("Il faut choisir un diagramme pour déssiner.")
        print("Continuer ? (n/y)")
        next = True if input() == "y" else False


# Les graphes qui peuvent être des camemberts sont : correctionsNb, cancelled, onBehalf, jointProcurement, fraAgreement, fraEstimated
def draw_Pie_Chart(df, column):
    newTableCount = df[column].value_counts(dropna=False).reset_index(name="count")
    pieLabels = newTableCount[column]
    pieValues = newTableCount["count"]

    figureObject, axesObject = plotter.subplots()

    # Draw the pie chart
    axesObject.pie(pieValues, labels=pieLabels, autopct="%1.2f", startangle=90)

    # Aspect ratio - equal means pie is a circle
    axesObject.axis("equal")
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

    # plotter.figtext(
    #     0.5,
    #     0.01,
    #     table,
    #     ha="center",
    #     va="center",
    #     fontsize=10,
    #     bbox={"facecolor": "gray", "alpha": 0.5},
    # )

    plotter.show()

    index_labels = ["Candidat " + str(n) for n in range(1, 6)]
    table = pd.DataFrame(data=table.values, index=index_labels, columns=all_columns)
    print(table)


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


if __name__ == "__main__":
    input_csv_path = sys.argv[1]
    read_csv(input_csv_path)
