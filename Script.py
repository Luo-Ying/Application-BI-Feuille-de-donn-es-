import pandas as pd
import sqlite3

from scriptGraphics.drawBoxPlot import draw_box_plot, draw_box_plot_multiple
from scriptGraphics.drawHist import draw_hist, draw_custom_hist, draw_hist_with_errors
from tabulate import tabulate

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plotter
import sys
import os
import math
import pygal
import lxml

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

DTYPE_DICT_NAMES = {
    "agentId": "Int64",
    "name": "object",
}

DTYPE_DICT_CRITERIA = {
    "criterionId": "Int64",
    "lotId": "Int64",
    "name": "object",
    "weight": "Float64",
    "type": "object",
}

all_columns = []
diagrams = ["camembert", "top 5", "worst 5", "nuage de points", "gauge", "radar", "tree map", "box plot", "violin plot",
            "histogram", "tab"]


def connect_db(db_path):
    return sqlite3.connect(db_path)


def close_db(connexion):
    connexion.close()


def create_df_from_query(connexion, query):
    return pd.read_sql_query(query, connexion)


def get_sql_request(connexion):
    cursor = connexion.cursor()
    query_select = input("Entrer votre SQL: ")
    cursor.execute(query_select)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def getType(df, column):
    print(f'{df[column].name} est de type {df[column].dtype}')


if __name__ == "__main__":
    db_path = 'Input\\Foppa.db'
    connexion = connect_db(db_path)

    # Type (Criteria)
    # df = create_df_from_query(connexion, "SELECT type, count(type) AS 'NbType' FROM Criteria GROUP BY type ORDER BY NbType DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist(df, 'type', 'NbType', "Distribution des types avec échelle logarithmique", "Criteria", False)

    # Weight (Criteria)
    # df = create_df_from_query(connexion, "SELECT weight, count(weight) AS 'NbWeight' FROM Criteria GROUP BY weight")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, 'weight', 'NbWeight', "Boxplot des poids avec échelle logarithmique", "Criteria", True)
    # draw_custom_hist(df, 'weight', 'NbWeight', "Distribution des poids par tranche de 50000", "Criteria", 0, 500000, 50000)

    # topType (Lots)
    # df = create_df_from_query(connexion, "SELECT topType, count(toptype) AS 'NbToptype' FROM Lots GROUP BY topType ORDER BY NbTopType DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist(df, 'topType', 'NbToptype', "Distribution des topType", "Lots")

    # multipleCae (Lots)
    # df = create_df_from_query(connexion, "SELECT multipleCae, count(multipleCae) AS 'NbMultipleCae' FROM Lots GROUP BY multipleCae UNION ALL SELECT 'NaN' AS multipleCae, COUNT(*) AS NbMultipleCae FROM Lots WHERE multipleCae IS NULL ORDER BY NbMultipleCae DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'multipleCae', 'NbMultipleCae', "Distribution des multipleCae", "Lots")

    # numberTendersSme (Lots)
    # df = create_df_from_query(connexion, "SELECT numberTendersSme, count(numberTendersSme) AS 'NbNumberTendersSme' FROM Lots GROUP BY numberTendersSme")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, 'numberTendersSme', 'NbNumberTendersSme', "Boxplot des numberTendersSme sans échelle logarithmique", "Lots")
    # draw_custom_hist(df, 'numberTendersSme', 'NbNumberTendersSme', "Distribution des numberTendersSme par tranche de 100", "Lots", 0, 1000, 100)

    # contractorSme (Lots)
    # df = create_df_from_query(connexion, "SELECT contractorSme, count(contractorSme) AS 'NbContractorSme' FROM Lots GROUP BY contractorSme")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'contractorSme', 'NbContractorSme', "Distribution des numberTendersSme", "Lots")

    # accelerated (Lots)
    # df = create_df_from_query(connexion, "SELECT 'NaN' AS accelerated, COUNT(*) AS NbAccelerated FROM Lots WHERE accelerated IS NULL UNION ALL SELECT '1' AS accelerated, COUNT(*) AS NbAccelerated FROM Lots WHERE accelerated IS NOT NULL;")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'accelerated', 'NbAccelerated', "Distribution des accelerated", "Lots")

    # lotsNumber (Lots)
    # df = create_df_from_query(connexion, "SELECT lotsNumber, count(lotsNumber) AS 'NbLotsNumber' FROM Lots GROUP BY lotsNumber UNION ALL SELECT 'NaN' AS lotsNumber, COUNT(*) AS 'NbLotsNumber' FROM Lots WHERE lotsNumber IS NULL ORDER BY NbLotsNumber DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'lotsNumber', 'NbLotsNumber', "Distribution des lotsNumber", "Lots")
    # draw_custom_hist(df, 'lotsNumber', 'NbLotsNumber', "Distribution des lotsNumber par tranche de 25000", "Lots", 0, 250000, 25000)

    # fraEstimated (Lots)
    # df = create_df_from_query(connexion, "SELECT fraEstimated, count(fraEstimated) AS 'NbFraEstimated' FROM Lots GROUP BY fraEstimated UNION ALL SELECT 'NaN' AS fraEstimated, COUNT(*) AS 'NbFraEstimated' FROM Lots WHERE fraEstimated IS NULL ORDER BY NbFraEstimated DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'fraEstimated', 'NbFraEstimated', "Distribution des fraEstimated", "Lots")

    # contractDuration (Lots)
    # df = create_df_from_query(connexion, "SELECT contractDuration, count(contractDuration) AS 'NbContractDuration' FROM Lots GROUP BY contractDuration UNION ALL SELECT 'NaN' AS contractDuration, COUNT(*) AS 'NbContractDuration' FROM Lots WHERE contractDuration IS NULL ORDER BY NbContractDuration DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'contractDuration', 'NbContractDuration', "Distribution des contractDuration", "Lots")
    # draw_box_plot(df, 'contractDuration', 'NbContractDuration', "Boxplot des contractDuration avec échelle logarithmique", "Lots", True)

    # publicityDuration (Lots)
    # df = create_df_from_query(connexion, "SELECT publicityDuration, count(publicityDuration) AS 'NbPublicityDuration' FROM Lots GROUP BY publicityDuration UNION ALL SELECT 'NaN' AS publicityDuration, COUNT(*) AS 'NbPublicityDuration' FROM Lots WHERE publicityDuration IS NULL ORDER BY NbPublicityDuration DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_hist_with_errors(df, 'publicityDuration', 'NbPublicityDuration', "Distribution des publicityDuration", "Lots")
    # draw_box_plot(df, 'publicityDuration', 'NbPublicityDuration', "Boxplot des publicityDuration avec échelle logarithmique", "Lots", True)

    # awardPrice (Lots)
    # df = create_df_from_query(connexion, "SELECT awardPrice, COUNT(awardPrice) AS 'NbAwardPrice' FROM Lots GROUP BY awardPrice UNION ALL SELECT 'NaN' AS awardPrice, COUNT(*) AS 'NbAwardPrice' FROM Lots WHERE awardPrice IS NULL ORDER BY NbAwardPrice DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, 'awardPrice', 'NbAwardPrice', "Boxplot des awardPrice avec échelle logarithmique", "Lots")
    # draw_custom_hist(df, 'awardPrice', 'NbAwardPrice', "Occurences des awardPrice par tranche de 1000", "Lots", 0, 17000, 1000)


    # awardEstimatedPrice (Lots)
    # df = create_df_from_query(connexion, "SELECT awardEstimatedPrice, COUNT(awardEstimatedPrice) AS 'NbAwardEstimatedPrice' FROM Lots GROUP BY awardEstimatedPrice UNION ALL SELECT 'NaN' AS awardEstimatedPrice, COUNT(*) AS 'NbAwardEstimatedPrice' FROM Lots WHERE awardEstimatedPrice IS NULL ORDER BY NbAwardEstimatedPrice DESC")
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    # draw_box_plot(df, 'awardEstimatedPrice', 'NbAwardEstimatedPrice', "Boxplot des awardPrice avec échelle logarithmique", "Lots")
    # draw_custom_hist(df, 'awardEstimatedPrice', 'NbAwardEstimatedPrice', "Occurences des awardEstimatedPrice par tranche de 100", "Lots", 0, 2500, 100)

    # cancelled - awardEstimatedPrice
    # df = create_df_from_query(connexion, "SELECT cancelled, awardEstimatedPrice FROM Lots")
    # draw_box_plot_multiple(df, 'cancelled', 'awardEstimatedPrice', "Boxplot des cancelled en fonction des awardEstimatedPrice avec échelle logarithmique", "Lots", True)

    df = create_df_from_query(connexion, "SELECT cancelled, awardPrice FROM Lots")
    draw_box_plot_multiple(df, 'cancelled', 'awardPrice', "Boxplot des cancelled en fonction des awardPrice avec échelle logarithmique", "Lots", True)

    close_db(connexion)