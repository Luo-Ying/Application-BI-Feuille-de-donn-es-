from scriptReadSql import create_df_from_query
from scriptGraphics.drawBoxPlot import draw_box_plot, draw_box_plot_multiple
from scriptGraphics.drawHist import draw_hist, draw_custom_hist, draw_hist_with_errors
from tabulate import tabulate

def script_pair(connexion):
    draw_cancelled_fraEstimated(connexion,"cancelled", "fraEstimated")

def draw_cancelled_fraEstimated(connexion, colonne_1, colonne_2):
    df = create_df_from_query(connexion, f"SELECT {colonne_1}, {colonne_2} FROM Lots")
    draw_box_plot_multiple(df, f'{colonne_1}', f'{colonne_2}', f"Boxplot des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique", "Lots", True)


