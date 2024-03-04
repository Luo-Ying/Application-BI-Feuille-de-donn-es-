import pandas as pd
import numpy as np
import sys
import os
import matplotlib.pyplot as plotter
import math
import pygal
import lxml

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
    print ("Les diagrammes disponibles sont : Camembert , Combo chart, Line Chart, Top 5, Boite moustache, Nuage de points, Tableau, Gauge, Tree map, Radar ")
    print("Veuillez choisir un type de diagramme : ")
    return input()

def draw_Diagram(diagram, df, column):
    match diagram:
        case 'Camembert':
            draw_Pie_Chart(diagram, df, column)
        case 'Nuage de points':
            draw_Scatter_Chart(diagram, df, column)
        case 'Gauge':
            draw_Gauge_Chart(diagram, df, column)
        case 'Radar':
            draw_Radar_Chart(diagram, df, column)


# Graphs with pie charts: correctionsNb, cancelled, onBehalf, jointProcurement, fraAgreement, fraEstimated
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

# Graphs cpv, numberTenders,lotsNumber, numberTendersSme, contractorSme, contractDuration, publicityDuration works but takes time and is incomprehensible, must zoom to see clearly
# Graphs with too many labels and values do not work. Maybe should group labels?
def draw_Scatter_Chart(diagram, df, column):
    newTableCount = df[column].value_counts(dropna=False).reset_index(name='count')
    pieLabels = newTableCount[column].astype(str)

    # Can work with mean average, variances , etc.. Not just count, should discuss with the group
    pieValues = newTableCount['count']

    #Define the axes
    plotter.scatter(pieLabels,pieValues)

    # Draw the scatter chart
    plotter.title('Nuage de points')
    plotter.xlabel('Labels')
    plotter.ylabel('Compte')
    plotter.show()

# Radars work with columns having few labels else it is horrible :(
def draw_Radar_Chart(diagram, df, column):
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
    
    plotter.show()


def draw_Gauge_Chart(diagram, df, column):
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
        gauge.add(value, [{'value': pieValues[i], 'max_value': maxValue}],formatter=formatter)
    
    gauge.render_in_browser()


if __name__ == '__main__':
    input_csv_path = sys.argv[1]
    read_csv(input_csv_path)