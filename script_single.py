from scriptReadSql import create_df_from_query
from scriptGraphics.drawBoxPlot import draw_box_plot, draw_box_plot_multiple, draw_box_plot_special
from scriptGraphics.drawHist import draw_hist, draw_custom_hist, draw_hist_with_errors
from tabulate import tabulate

def script_single(connexion):
    # draw_cpv_lots(connexion)
    # draw_award_estimated_price(connexion, "awardEstimatedPrice")
    # draw_award_price(connexion, "awardPrice")
    draw_contract_duration(connexion, "contractDuration")
    

def draw_cpv_lots(connexion):
    df = create_df_from_query(connexion, "SELECT SUBSTR(cpv,1,2) AS cpv, COUNT(*) AS count FROM Lots GROUP BY SUBSTR(cpv,1,2)")
    df2 = create_df_from_query(connexion, "SELECT SUBSTR(cpv,1,3) AS cpv, COUNT(*) AS count FROM Lots GROUP BY SUBSTR(cpv,1,3) ORDER BY count DESC LIMIT 45")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_hist(df, 'cpv', 'count', "Distribution des cpv par 2 premiers chiffres", "Lots")
    draw_hist(df2, 'cpv', 'count', "Distribution des 45 premiers cpv par 3 premiers chiffres", "Lots")

def draw_award_estimated_price(connexion, colonne_1):
    df = create_df_from_query(connexion, f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} UNION ALL SELECT 'NaN' AS {colonne_1}, COUNT(*) AS 'Nb{colonne_1}' FROM Lots WHERE {colonne_1} IS NULL ORDER BY Nb{colonne_1} DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_box_plot_special(df, f'{colonne_1}', f'{colonne_1}', f"Boxplot des {colonne_1} avec échelle logarithmique", "Lots", True, True)

def draw_award_price(connexion, colonne_1):
    df = create_df_from_query(connexion, f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} UNION ALL SELECT 'NaN' AS {colonne_1}, COUNT(*) AS 'Nb{colonne_1}' FROM Lots WHERE {colonne_1} IS NULL ORDER BY Nb{colonne_1} DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_box_plot_special(df, f'{colonne_1}', f'{colonne_1}', f"Boxplot des {colonne_1} avec échelle logarithmique", "Lots", True, True)

def draw_contract_duration(connexion, colonne_1):
    df = create_df_from_query(connexion, f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} UNION ALL SELECT 'NaN' AS {colonne_1}, COUNT(*) AS 'Nb{colonne_1}' FROM Lots WHERE {colonne_1} IS NULL ORDER BY Nb{colonne_1} DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_box_plot_special(df, f'{colonne_1}', f'{colonne_1}', f"Boxplot des {colonne_1} avec échelle logarithmique", "Lots", True, True)