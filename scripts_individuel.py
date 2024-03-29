from scriptReadSql import create_df_from_query
from scriptGraphics.drawBoxPlot import draw_box_plot, draw_box_plot_multiple
from scriptGraphics.drawHist import draw_hist, draw_custom_hist, draw_hist_with_errors
from tabulate import tabulate


def scripts_individuel(connexion):
    # # Type (Criteria)
    # df = create_df_from_query(connexion, "SELECT type, count(type) AS 'NbType' FROM Criteria GROUP BY type ORDER BY NbType DESC")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist(df, 'type', 'NbType', "Distribution des types avec échelle logarithmique", "Criteria", False)
    #
    # # Weight (Criteria)
    # df = create_df_from_query(connexion, "SELECT weight, count(weight) AS 'NbWeight' FROM Criteria GROUP BY weight")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, 'weight', 'weight', "Boxplot des poids avec échelle logarithmique", "Criteria", True)
    # draw_custom_hist(df, 'weight', 'NbWeight', "Distribution des poids par tranche de 50000", "Criteria", 0, 500000, 50000)
    #
    # # topType (Lots)
    # df = create_df_from_query(connexion, "SELECT topType, count(toptype) AS 'NbToptype' FROM Lots GROUP BY topType ORDER BY NbTopType DESC")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist(df, 'topType', 'NbToptype', "Distribution des topType", "Lots")
    #
    # # multipleCae (Lots)
    # df = create_df_from_query(connexion, "SELECT multipleCae, count(multipleCae) AS 'NbMultipleCae' FROM Lots GROUP BY multipleCae UNION ALL SELECT 'NaN' AS multipleCae, COUNT(*) AS NbMultipleCae FROM Lots WHERE multipleCae IS NULL ORDER BY NbMultipleCae DESC")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'multipleCae', 'NbMultipleCae', "Distribution des multipleCae", "Lots")
    #
    # # numberTendersSme (Lots)
    # colonne_1 = "numberTenders"
    # df = create_df_from_query(connexion, f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1}")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, f'{colonne_1}', f'{colonne_1}', f"Boxplot des {colonne_1} avec échelle logarithmique", "Lots", True)
    # draw_custom_hist(df, f'{colonne_1}', f'Nb{colonne_1}', f"Occurences des {colonne_1} par tranche de 100", "Lots", 0, 1000, 100)
    #
    # # numberTendersSme (Lots)
    # df = create_df_from_query(connexion, "SELECT numberTendersSme, count(numberTendersSme) AS 'NbNumberTendersSme' FROM Lots GROUP BY numberTendersSme")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, 'numberTendersSme', 'numberTendersSme', "Boxplot des numberTendersSme sans échelle logarithmique", "Lots")
    # draw_custom_hist(df, 'numberTendersSme', 'NbNumberTendersSme', "Distribution des numberTendersSme par tranche de 100", "Lots", 0, 1000, 100)
    #
    # # contractorSme (Lots)
    # df = create_df_from_query(connexion, "SELECT contractorSme, count(contractorSme) AS 'NbContractorSme' FROM Lots GROUP BY contractorSme UNION ALL SELECT '1' AS contractorSme, COUNT(*) AS NbContractorSme FROM Lots WHERE contractorSme IS NULL;")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'contractorSme', 'NbContractorSme', "Distribution des numberTendersSme", "Lots")
    #
    # # accelerated (Lots)
    # df = create_df_from_query(connexion, "SELECT 'NaN' AS accelerated, COUNT(*) AS NbAccelerated FROM Lots WHERE accelerated IS NULL UNION ALL SELECT '1' AS accelerated, COUNT(*) AS NbAccelerated FROM Lots WHERE accelerated IS NOT NULL;")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'accelerated', 'NbAccelerated', "Distribution des accelerated", "Lots")
    #
    # # lotsNumber (Lots)
    # df = create_df_from_query(connexion, "SELECT lotsNumber, count(lotsNumber) AS 'NbLotsNumber' FROM Lots GROUP BY lotsNumber UNION ALL SELECT 'NaN' AS lotsNumber, COUNT(*) AS 'NbLotsNumber' FROM Lots WHERE lotsNumber IS NULL ORDER BY NbLotsNumber DESC")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'lotsNumber', 'NbLotsNumber', "Distribution des lotsNumber", "Lots")
    # draw_custom_hist(df, 'lotsNumber', 'NbLotsNumber', "Distribution des lotsNumber par tranche de 25000", "Lots", 0, 250000, 25000)
    #
    # # fraEstimated (Lots)
    # df = create_df_from_query(connexion, "SELECT fraEstimated, count(fraEstimated) AS 'NbFraEstimated' FROM Lots GROUP BY fraEstimated UNION ALL SELECT 'NaN' AS fraEstimated, COUNT(*) AS 'NbFraEstimated' FROM Lots WHERE fraEstimated IS NULL ORDER BY NbFraEstimated DESC")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'fraEstimated', 'NbFraEstimated', "Distribution des fraEstimated", "Lots")
    #
    # # contractDuration (Lots)
    df = create_df_from_query(connexion, "SELECT contractDuration, count(contractDuration) AS 'NbContractDuration' FROM Lots GROUP BY contractDuration UNION ALL SELECT 'NaN' AS contractDuration, COUNT(*) AS 'NbContractDuration' FROM Lots WHERE contractDuration IS NULL ORDER BY NbContractDuration DESC")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'contractDuration', 'NbContractDuration', "Distribution des contractDuration", "Lots")
    draw_box_plot(df, 'contractDuration', 'contractDuration', "Boxplot des contractDuration avec échelle logarithmique", "Lots", True)
    #
    # # publicityDuration (Lots)
    # df = create_df_from_query(connexion, "SELECT publicityDuration, count(publicityDuration) AS 'NbPublicityDuration' FROM Lots GROUP BY publicityDuration UNION ALL SELECT 'NaN' AS publicityDuration, COUNT(*) AS 'NbPublicityDuration' FROM Lots WHERE publicityDuration IS NULL ORDER BY NbPublicityDuration DESC")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'publicityDuration', 'NbPublicityDuration', "Distribution des publicityDuration", "Lots")
    # draw_box_plot(df, 'publicityDuration', 'NbPublicityDuration', "Boxplot des publicityDuration avec échelle logarithmique", "Lots", True)
    #
    # awardPrice (Lots)
    # df = create_df_from_query(connexion, "SELECT awardPrice, COUNT(awardPrice) AS 'NbAwardPrice' FROM Lots GROUP BY awardPrice UNION ALL SELECT 'NaN' AS awardPrice, COUNT(*) AS 'NbAwardPrice' FROM Lots WHERE awardPrice IS NULL ORDER BY NbAwardPrice DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, 'awardPrice', 'awardPrice', "Boxplot des awardPrice avec échelle logarithmique", "Lots", True)
    # draw_custom_hist(df, 'awardPrice', 'NbAwardPrice', "Occurences des awardPrice par tranche de 1000", "Lots", 0, 17000, 1000)
    #
    # # awardEstimatedPrice (Lots)
    # colonne_1 = "awardEstimatedPrice"
    # df = create_df_from_query(connexion, f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} UNION ALL SELECT 'NaN' AS {colonne_1}, COUNT(*) AS 'Nb{colonne_1}' FROM Lots WHERE {colonne_1} IS NULL ORDER BY Nb{colonne_1} DESC")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, f'{colonne_1}', f'{colonne_1}', f"Boxplot des {colonne_1} avec échelle logarithmique", "Lots", True)
    # draw_custom_hist(df, f'{colonne_1}', f'Nb{colonne_1}', f"Occurences des {colonne_1} par tranche de 100", "Lots", 0, 2500, 100)
    #
    # # awardEstimatedPrice (Lots)
    # colonne_1 = "correctionsNb"
    # df = create_df_from_query(connexion, f"SELECT {colonne_1} FROM Lots")
    # # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, f'{colonne_1}', f'{colonne_1}', f"Boxplot des {colonne_1} avec échelle logarithmique", "Lots", log=False)

    # df = create_df_from_query(connexion, "SELECT count(contractorSme) as NullCount, SUM(CASE WHEN contractorSme IS NULL then 1 else 0 end) as notNullCount FROM Lots;")
    # print(tabulate(df, headers='keys', tablefmt='psql'))

    # # typeOfContract (Lots)
    # colonne_1 = "typeOfContract"
    # df = create_df_from_query(connexion, f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} UNION ALL SELECT 'NaN' AS {colonne_1}, COUNT(*) AS 'Nb{colonne_1}' FROM Lots WHERE {colonne_1} IS NULL ORDER BY Nb{colonne_1} DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, f'{colonne_1}', f'{colonne_1}', f"Boxplot des {colonne_1} avec échelle logarithmique", "Lots", True)
    # draw_hist_with_er rors(df, f'{colonne_1}', f'Nb{colonne_1}', f"Distribution des {colonne_1}", "Lots", True)