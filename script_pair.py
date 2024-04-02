import re

from scriptGraphics.drawScatterPlots import draw_scatter_plots2
from scriptGraphics.drawTop import get_top_multiple, get_top
from scriptReadSql import create_df_from_query
from scriptGraphics.drawBoxPlot import *
from scriptGraphics.drawHist import *
from scriptReadSql import *
from tabulate import tabulate


def script_pair(connexion):
    ##############################################
    ################ Criteria a###################
    ##############################################

    ##############################################
    ################# Agents a####################
    ##############################################

    ##############################################
    ################# weight a####################
    ##############################################
    """cancelleed & numberTenders"""
    # draw_cancelled_numberTenders(connexion)
    """cancelleed & numberTendersSme"""
    # draw_canccelled_numberTendersSme(connexion)
    """cancelled & fraEstimateed"""
    # draw_cancelled_fraEstimated(connexion, "cancelled", "fraEstimated")
    """cancelled & typeOfContract"""
    # draw_cancelled_typeOfContract(connexion, "cancelled", "typeOfContract")
    """cancelled & awardEstimatedPrice"""
    # draw_cancelled_awardEstimatedPrice(connexion)
    """cancelled & awardPrice"""
    # draw_cancelled_awardPrice(connexion)
    """cancelled & topType"""
    # draw_cancelled_topType(connexion, "cancelled", "topType")
    """awardEstimatedPrice & awardPrice"""
    # draw_awardPrice_awardEstimatedPrice(connexion, "awardPrice", "awardEstimatedPrice")
    """numberTenders & numberTendersSme"""
    # draw_numberTenders_numberTendersSme(connexion)
    """numberTenders & typeOfContract"""
    # draw_numberTenders_typeOfContract(connexion)
    """awardEstimatedPrice & lotsNumber"""
    # draw_awardEstimatedPrice_lotsNumber(connexion)
    """onBehalf & typeOfContract"""
    # draw_onBehalf_typeOfContract(connexion)
    """awardPrice & typeOfContracted"""
    # draw_awardPrice_subContracted(connexion)
    """awardPrice & numberTendersSme"""
    # draw_awardPrice_numberTendersSme(connexion)
    """awardPrice & lotsNumber"""
    draw_awardPrice_lotsNumber(connexion)
    """awardPrice & jointProcurement"""
    # draw_awardPrice_jointProcurement(connexion)


def draw_awardPrice_jointProcurement(conn):
    df = create_df_from_query(
        conn,
        "SELECT awardPrice, jointProcurement From Lots WHERE awardPrice IS NOT null and jointProcurement IS NOT null ORDER BY awardPrice ASC",
    )
    print(df)
    draw_box_plot_multiple(
        df,
        f"jointProcurement",
        f"awardPrice",
        f"Boxplot des awardPrice en fonction des jointProcurement avec échelle logarithmique",
        "Lots",
        True,
    )


def draw_awardPrice_lotsNumber(conn):
    df = create_df_from_query(
        conn,
        "SELECT awardPrice, lotsNumber From Lots WHERE awardPrice IS NOT null AND LotsNumber IS NOT null AND lotsNumber NOT GLOB '*[a-zA-Z]*' AND lotsNumber NOT LIKE '%-%' AND lotsNumber NOT LIKE '%*%' AND lotsNumber NOT LIKE '%;%' ORDER BY lotsNumber ASC",
    )
    print(df)
    df['lotsNumber'] = pd.to_numeric(df['lotsNumber'], errors='coerce')
    draw_scatter_plots2(
        df,
        "awardPrice",
        "lotsNumber",
        "Nombre d'occurence de lotsNumber pour chaque element de awardPrice",
        False,
        True
    )


def draw_awardPrice_numberTendersSme(conn):
    df = create_df_from_query(
        conn,
        "SELECT awardPrice, numberTendersSme From Lots WHERE awardPrice IS NOT null and numberTendersSme IS NOT null ORDER BY awardPrice ASC",
    )

    print(df)
    draw_box_plot_multiple_numberTenders_NumberTendersSme(
        df,
        "numberTendersSme",
        "awardPrice",
        "Boxplot des awardPrice en fonction des numberTendersSme avec échelle logarithmique",
        "Lots",
        True,
    )


def draw_awardPrice_subContracted(conn):
    df = create_df_from_query(
        conn,
        "SELECT awardPrice, subContracted From Lots WHERE awardPrice IS NOT null and subContracted IS NOT null ORDER BY awardPrice ASC",
    )
    print(df)
    draw_box_plot_multiple(
        df,
        f"subContracted",
        f"awardPrice",
        f"Boxplot des awardPrice en fonction des subContracted avec échelle logarithmique",
        "Lots",
        True,
    )


def draw_awardPrice_typeOfContract(conn):
    df = create_df_from_query(
        conn,
        "SELECT awardPrice, typeOfContract From Lots WHERE awardPrice IS NOT null and typeOfContract IS NOT null ORDER BY awardPrice ASC",
    )
    print(df)
    draw_box_plot_multiple(
        df,
        f"typeOfContract",
        f"awardPrice",
        f"Boxplot des awardPrice en fonction des typeOfContract avec échelle logarithmique",
        "Lots",
        True,
    )


def draw_onBehalf_typeOfContract(conn):
    df = create_df_from_query(
        conn,
        "SELECT onBehalf, typeOfContract, count(onBehalf) AS 'NbonBehalf' FROM Lots GROUP BY onBehalf, typeOfContract",
    )
    print(df)
    hist_pivot(
        df,
       "typeOfContract",
       "onBehalf",
       "Histogramme cumulé des onBehalf en fonction des typeOfContract",
       "Lots",
       False,
    )


def draw_awardEstimatedPrice_lotsNumber(conn):
    df = create_df_from_query(
        conn,
        "SELECT awardEstimatedPrice, lotsNumber From Lots WHERE awardEstimatedPrice IS NOT null AND LotsNumber IS NOT null AND lotsNumber NOT GLOB '*[a-zA-Z]*' AND lotsNumber NOT LIKE '%-%' AND lotsNumber NOT LIKE '%*%' AND lotsNumber NOT LIKE '%;%' ORDER BY lotsNumber ASC",
    )
    print(df)
    df['lotsNumber'] = pd.to_numeric(df['lotsNumber'], errors='coerce')
    draw_scatter_plots2(
        df,
        "awardEstimatedPrice",
        "lotsNumber",
        "Nombre d'occurence de lotsNumber pour chaque element de awardEstimatedPrice",
        False,
        True
    )


def draw_numberTenders_typeOfContract(conn):
    df = create_df_from_query(
        conn,
        "SELECT typeOfContract, numberTenders From Lots WHERE numberTenders IS NOT null and numberTendersSme IS NOT null ORDER BY numberTenders ASC",
    )
    print(df)
    draw_box_plot_multiple(
        df,
        "typeOfContract",
        "numberTenders",
        "Boxplot des typeOfContract en fonction des numberTenders",
        "Lots",
        False,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT typeOfContract as typeOfContract, 'occurence' as numberTenders, count(numberTenders) as count
            FROM Lots
            WHERE typeOfContract IS NOT NULL
            GROUP BY typeOfContract

            UNION

            SELECT typeOfContract as typeOfContract, 'nullCount' as numberTenders, SUM(CASE WHEN numberTenders IS NULL THEN 1 ELSE 0 END) as count
            FROM Lots
            WHERE typeOfContract IS NOT NULL
            GROUP BY typeOfContract
        """,
    )
    draw_multiple_hist(
        df2,
        "typeOfContract",
        "numberTenders",
        "Nombre d'occurence de numberTenders pour chaque element de typeOfContract",
        "Lots",
        True,
    )


def draw_numberTenders_numberTendersSme(conn):
    df = create_df_from_query(
        conn,
        "SELECT numberTenders, numberTendersSme From Lots WHERE numberTenders IS NOT null and numberTendersSme IS NOT null ORDER BY numberTenders ASC",
    )

    print(df)
    draw_box_plot_multiple_numberTenders_NumberTendersSme(
        df,
        "numberTenders",
        "numberTendersSme",
        "Boxplot des numberTenders en fonction des numberTendersSme avec échelle logarithmique",
        "Lots",
        True,
    )


def draw_cancelled_awardPrice(conn):
    df = create_df_from_query(conn, "SELECT cancelled, awardPrice FROM Lots")
    draw_box_plot_multiple(
        df,
        "cancelled",
        "awardPrice",
        "Boxplot des cancelled en fonction des awardPrice avec échelle logarithmique",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT cancelled as cancelled, 'occurence' as awardPrice, count(awardPrice) as count
        FROM Lots
        WHERE cancelled IS NOT NULL
        GROUP BY cancelled

        UNION

        SELECT cancelled as cancelled, 'nullCount' as awardPrice, SUM(CASE WHEN awardPrice IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE cancelled IS NOT NULL
        GROUP BY cancelled;""",
    )
    draw_multiple_hist(
        df2,
        "cancelled",
        "awardPrice",
        "Nombre d'occurence de awardPrice pour chaque element de cancelled",
        "Lots",
        True,
    )


def draw_cancelled_awardEstimatedPrice(conn):
    df = create_df_from_query(conn, "SELECT cancelled, awardEstimatedPrice FROM Lots")
    print(df)
    draw_box_plot_multiple(
        df,
        "cancelled",
        "awardEstimatedPrice",
        "Boxplot des cancelled en fonction des awardEstimatedPrice avec échelle logarithmique",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT cancelled as cancelled, 'occurence' as awardEstimatedPrice, count(awardEstimatedPrice) as count
        FROM Lots
        WHERE cancelled IS NOT NULL
        GROUP BY cancelled

        UNION

        SELECT cancelled as cancelled, 'nullCount' as awardEstimatedPrice, SUM(CASE WHEN awardEstimatedPrice IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE cancelled IS NOT NULL
        GROUP BY cancelled;""",
    )
    draw_multiple_hist(
        df2,
        "cancelled",
        "awardEstimatedPrice",
        "Nombre d'occurence de awardEstimatedPrice pour chaque element de cancelled",
        "Lots",
        True,
    )


def draw_canccelled_numberTendersSme(conn):
    colonne_1 = "cancelled"
    colonne_2 = "numberTendersSme"
    df = create_df_from_query(conn, f"SELECT {colonne_1}, numberTendersSme FROM Lots")
    draw_box_plot_multiple(
        df,
        f"{colonne_1}",
        f"{colonne_2}",
        f"Boxplot des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT cancelled as cancelled, 'occurence' as numberTendersSme, count(numberTendersSme) as count
        FROM Lots
        WHERE cancelled IS NOT NULL
        GROUP BY cancelled

        UNION

        SELECT cancelled as cancelled, 'nullCount' as numberTendersSme, SUM(CASE WHEN numberTendersSme IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE cancelled IS NOT NULL
        GROUP BY cancelled;""",
    )
    draw_multiple_hist(
        df2,
        "cancelled",
        "numberTendersSme",
        "Nombre d'occurence de numberTendersSme pour chaque element de cancelled",
        "Lots",
        True,
    )


def draw_cancelled_numberTenders(conn):
    df = create_df_from_query(conn, "SELECT cancelled, numberTenders FROM Lots")
    draw_box_plot_multiple(
        df,
        "cancelled",
        "numberTenders",
        "Boxplot des cancelled en fonction des numberTenders avec échelle logarithmique",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT cancelled as cancelled, 'occurence' as numberTenders, count(numbertenders) as count
        FROM Lots
        WHERE cancelled IS NOT NULL
        GROUP BY cancelled

        UNION

        SELECT cancelled as cancelled, 'nullCount' as numberTenders, SUM(CASE WHEN numberTenders IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE cancelled IS NOT NULL
        GROUP BY cancelled;""",
    )
    draw_multiple_hist(
        df2,
        "cancelled",
        "numberTenders",
        "Nombre d'occurence de numberTenders pour chaque element de cancelled",
        "Lots",
        True,
    )


def draw_cancelled_fraEstimated(connexion, colonne_1, colonne_2):
    df = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, {colonne_2}, COUNT(*) AS count FROM Lots GROUP BY {colonne_1}, {colonne_2}",
    )
    print(df)
    draw_multiple_hist(
        df,
        f"{colonne_1}",
        f"{colonne_2}",
        f"Histogramme des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique",
        "Lots",
        True,
        True,
        20,
        90,
    )


def draw_cancelled_typeOfContract(connexion, colonne_1, colonne_2):
    df = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, {colonne_2}, COUNT(*) AS count FROM Lots GROUP BY {colonne_1}, {colonne_2}",
    )
    draw_multiple_hist(
        df,
        f"{colonne_1}",
        f"{colonne_2}",
        f"Histogramme des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique",
        "Lots",
        True,
        True,
        None,
        90,
    )


def draw_cancelled_topType(connexion, colonne_1, colonne_2):
    df = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, {colonne_2}, COUNT(*) AS count FROM Lots GROUP BY {colonne_1}, {colonne_2}",
    )
    draw_multiple_hist(
        df,
        f"{colonne_1}",
        f"{colonne_2}",
        f"Histogramme des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique",
        "Lots",
        True,
        True,
        20,
        90,
    )


def draw_awardPrice_awardEstimatedPrice(connexion, colonne_1, colonne_2):
    df = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, {colonne_2}, ({colonne_1} - {colonne_2}) AS difference FROM Lots WHERE {colonne_1} IS NOT NULL AND {colonne_2} IS NOT NULL",
    )
    draw_box_plot_special(
        df,
        "difference",
        "difference",
        f"Boxplot de la différence des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique",
        "Lots",
        False,
        False,
    )
