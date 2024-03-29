from scriptGraphics.db import create_df_from_query
from scriptGraphics.drawBoxPlot import draw_box_plot, draw_box_plot_multiple
from scriptGraphics.drawHist import draw_hist, draw_custom_hist, draw_hist_with_errors
from tabulate import tabulate

def scripts_paires(connexion):
    # cancelled - awardEstimatedPrice
    df = create_df_from_query(connexion, "SELECT cancelled, awardEstimatedPrice FROM Lots")
    draw_box_plot_multiple(df, 'cancelled', 'awardEstimatedPrice', "Boxplot des cancelled en fonction des awardEstimatedPrice avec échelle logarithmique", "Lots", True)

    # cancelled - awardPrice
    df = create_df_from_query(connexion, "SELECT cancelled, awardPrice FROM Lots")
    draw_box_plot_multiple(df, 'cancelled', 'awardPrice', "Boxplot des cancelled en fonction des awardPrice avec échelle logarithmique", "Lots", True)

    # cancelled - numberTenders
    df = create_df_from_query(connexion, "SELECT cancelled, numberTenders FROM Lots")
    draw_box_plot_multiple(df, 'cancelled', 'numberTenders', "Boxplot des cancelled en fonction des numberTenders avec échelle logarithmique", "Lots", True)

    # cancelled - numberTenders
    colonne_1 = "cancelled"
    colonne_2 = "numberTendersSme"
    df = create_df_from_query(connexion, f"SELECT {colonne_1}, numberTendersSme FROM Lots")
    draw_box_plot_multiple(df, f'{colonne_1}', f'{colonne_2}', f"Boxplot des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique", "Lots", True)
