from scriptReadSql import create_df_from_query
from scriptGraphics.drawBoxPlot import *
from scriptGraphics.drawHist import *
from tabulate import tabulate

def script_pair(connexion):
    # draw_cancelled_fraEstimated(connexion,"cancelled", "fraEstimated")
    # draw_cancelled_typeOfContract(connexion,"cancelled", "typeOfContract")
    # draw_cancelled_topType(connexion,"cancelled", "topType")
    draw_awardPrice_awardEstimatedPrice(connexion,"awardPrice", "awardEstimatedPrice")

def draw_cancelled_fraEstimated(connexion, colonne_1, colonne_2):
    df = create_df_from_query(connexion, f"SELECT {colonne_1}, {colonne_2}, COUNT(*) AS count FROM Lots GROUP BY {colonne_1}, {colonne_2}")
    draw_multiple_hist(df, f'{colonne_1}', f'{colonne_2}', f"Histogramme des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique", "Lots", True,True,20,90)


def draw_cancelled_typeOfContract(connexion, colonne_1, colonne_2):
    df = create_df_from_query(connexion, f"SELECT {colonne_1}, {colonne_2}, COUNT(*) AS count FROM Lots GROUP BY {colonne_1}, {colonne_2}")
    draw_multiple_hist(df, f'{colonne_1}', f'{colonne_2}', f"Histogramme des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique", "Lots", True,True,None,90)

def draw_cancelled_topType(connexion, colonne_1, colonne_2):
    df = create_df_from_query(connexion, f"SELECT {colonne_1}, {colonne_2}, COUNT(*) AS count FROM Lots GROUP BY {colonne_1}, {colonne_2}")
    draw_multiple_hist(df, f'{colonne_1}', f'{colonne_2}', f"Histogramme des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique", "Lots", True,True,20,90)

def draw_awardPrice_awardEstimatedPrice(connexion, colonne_1, colonne_2):
    df = create_df_from_query(connexion, f"SELECT {colonne_1}, {colonne_2}, ({colonne_1} - {colonne_2}) AS difference FROM Lots WHERE {colonne_1} IS NOT NULL AND {colonne_2} IS NOT NULL")
    draw_box_plot_special(df, 'difference', 'difference', f"Boxplot de la différence des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique", "Lots", False,False)