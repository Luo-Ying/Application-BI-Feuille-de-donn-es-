import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plotter
import math

DTYPE_DICT_LOTS = {'lotId': 'Int64', 'tedCanId': 'Int64', 'correctionsNb': 'Int64', 'cancelled': 'Int64', 'awardDate': 'object', 'awardEstimatedPrice': 'Float64',
'awardPrice': 'Float64', "cpv" : 'Int64', 'numberTenders' : 'Int64', 'onBehalf': 'object' , 'jointProcurement' : 'object' , 'fraAgreement' : 'object',
'fraEstimated' : 'object', 'lotsNumber' : 'object', 'accelerated' : 'object', 'outOfDirectives': 'Int64', 'contractorSme' : 'object', 'numberTendersSme' : 'Float64' ,
'subContracted' : 'object', 'gpa' : 'object', 'multipleCae': 'object', 'typeOfContract': 'object', 'topType' : 'object', 'renewal': 'object', 'contractDuration': 'Float64',
'publicityDuration' : 'Float64'}

def read_csv(input_csv_path):
    match os.path.basename(input_csv_path):
        case 'Lots.csv':
            df = pd.read_csv(input_csv_path, dtype=DTYPE_DICT_LOTS, sep=',')
            column = read_user_column(df)
            diagram = choose_Diagram()
            draw_Diagram(diagram, df, column)
        case _:
            print("Action par defaut")

def read_user_column(df):
    print("Voici les colonnes disponibles : ")
    for col in df.columns:
        print(col)
    print("Veuillez selectionner une colonne : ")
    return input()

def choose_Diagram():
    print ("Les diagrammes disponibles sont : Camembert , Combo chart, Line Chart, Top 5, Boite moustache, Nuage de points, Tableau, Gauge, Tree map ")
    print("Veuillez choisir un type de diagramme : ")
    return input()

def draw_Diagram(diagram, df, column):
    match diagram:
        case 'Camembert':
            draw_Pie_Chart(diagram, df, column)


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

if __name__ == '__main__':
    input_csv_path = sys.argv[1]
    read_csv(input_csv_path)