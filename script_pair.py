import re

from scriptReadSql import create_df_from_query
from scriptGraphics.drawBoxPlot import *
from scriptGraphics.drawHist import *
from scriptGraphics.drawScatterPlots import *
from scriptGraphics.drawLineChart import *
from scriptReadSql import *
from tabulate import tabulate


def script_pair(connexion):
    # ##############################################
    # ################ Criteria a###################
    # ##############################################

    # ##############################################
    # ################# Agents a####################
    # ##############################################

    # ##############################################
    # ################# weight a####################
    # ##############################################
    """cancelled & numberTenders"""
    # draw_cancelled_numberTenders(connexion)
    # """cancelled & numberTendersSme"""
    # draw_canccelled_numberTendersSme(connexion)
    # """cancelled & fraEstimated"""
    # draw_cancelled_fraEstimated(connexion, "cancelled", "fraEstimated")
    # """cancelled & typeOfContract"""
    # draw_cancelled_typeOfContract(connexion, "cancelled", "typeOfContract")
    # """cancelled & awardEstimatedPrice"""
    # draw_cancelled_awardEstimatedPrice(connexion)
    # """cancelled & awardPrice"""
    # draw_cancelled_awardPrice(connexion)
    # """cancelled & topType"""
    # draw_cancelled_topType(connexion, "cancelled", "topType")
    # """awardEstimatedPrice & awardPrice"""
    # draw_awardPrice_awardEstimatedPrice(connexion, "awardPrice", "awardEstimatedPrice")
    # """numberTenders & numberTendersSme"""
    # draw_numberTenders_numberTendersSme(connexion)
    # """numberTenders & contractorSme (à voir)"""
    # draw_numberTenders_contractorSme(connexion)
    # """numberTenders & topType"""
    # draw_numberTendedrs_topType(connexion)
    # """numberTenders & awardEstimatedPrice"""
    # draw_numberTenders_awardEstimatedPrice(connexion)
    # """numberTendersSme & awardEstimatedPrice"""
    # draw_numberTendersSme_awardEstimatedPrice(connexion)
    # """numberTenders & awardPrice"""
    # draw_numberTenders_awardPrice(connexion)
    # """numberTendersSme & typeOfContract"""
    # draw_numberTendersSme_typeOfContract(
    #     connexion, "numberTendersSme", "typeOfContract"
    # )
    # """awardPrice & cpv"""
    # draw_awardPrice_cpv(connexion, "awardPrice", "cpv")
    # """awardPrice & fraAgreement"""
    # draw_awardPrice_fraAgreement(connexion, "awardPrice", "fraAgreement")
    # """accelerated & awardEstimatedPrice"""
    # draw_accelerated_awardEstimatedPrice(connexion)
    # """accelerated & typeOfContract"""
    # draw_accelerated_typeOfContract(connexion)
    # """accelerated & topType"""
    # draw_accelerated_topType(connexion)
    # """accelerateed & publicityDuration"""
    # draw_accelerated_publicityDuration(connexion)
    # """awardPrice & publicityDuration"""
    # draw_awardPrice_publicityDuration(connexion)
    # """awardPrice & contractDuration"""
    # draw_awardPrice_contractDuration(connexion)
    # """awardPrice & topType"""
    # draw_awardPrice_topType(connexion)
    # """awardPrice & multipleCae"""
    # draw_awardPrice_multipleCae(connexion)
    # """awardPrice & accelerated"""
    # draw_awardPrice_accelerated(connexion)
    # """awardPrice & outOfDirectives"""
    # draw_awardPrice_outOfDirectives(connexion)
    # """awardPrice & onBehalf"""
    # draw_awardPrice_onBehalf(connexion)
    # """numberTenders & typeOfContract"""
    # draw_numberTenders_typeOfContract(connexion)
    # """awardEstimatedPrice & lotsNumber"""
    # draw_awardEstimatedPrice_lotsNumber(connexion)
    # """onBehalf & typeOfContract"""
    # draw_onBehalf_typeOfContract(connexion)
    # """awardPrice & typeOfContract"""
    # # draw_awardPrice_typeOfContract(connexion)
    # """awardPrice & subContracted"""
    # draw_awardPrice_subContracted(connexion)
    # """awardPrice & numberTendersSme"""
    # draw_awardPrice_numberTendersSme(connexion)
    # """awardPrice & lotsNumber"""
    # draw_awardPrice_lotsNumber(connexion)
    # """awardPrice & jointProcurement"""
    # draw_awardPrice_jointProcurement(connexion)


def draw_awardPrice_jointProcurement(conn):
    df_contratS = create_df_from_query(
        conn,
        "SELECT awardPrice, jointProcurement From Lots WHERE typeOfContract = 'S'",
    )
    df_contratW = create_df_from_query(
        conn,
        "SELECT awardPrice, jointProcurement From Lots WHERE typeOfContract = 'W'",
    )
    df_contratU = create_df_from_query(
        conn,
        "SELECT awardPrice, jointProcurement From Lots WHERE typeOfContract = 'U'",
    )
    draw_box_plot_multiple(
        df_contratS,
        f"jointProcurement",
        f"awardPrice",
        f"Boxplot des awardPrice en fonction des jointProcurement en type de contrat 'S'",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contratW,
        f"jointProcurement",
        f"awardPrice",
        f"Boxplot des awardPrice en fonction des jointProcurement en type de contrat 'W'",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contratU,
        f"jointProcurement",
        f"awardPrice",
        f"Boxplot des awardPrice en fonction des jointProcurement en type de contrat 'U'",
        "Lots",
        True,
    )


def draw_awardPrice_lotsNumber(conn):
    df_contractS = create_df_from_query(
        conn,
        "SELECT lotsNumber, awardPrice From Lots WHERE typeOfContract = 'S' AND lotsNumber IS NOT null AND awardPrice IS NOT null AND awardPrice NOT GLOB '*[a-zA-Z]*' AND awardPrice NOT LIKE '%-%' AND awardPrice NOT LIKE '%*%' AND awardPrice NOT LIKE '%;%' ORDER BY awardPrice ASC",
    )
    df_contractW = create_df_from_query(
        conn,
        "SELECT lotsNumber, awardPrice From Lots WHERE typeOfContract = 'W' AND lotsNumber IS NOT null AND awardPrice IS NOT null AND awardPrice NOT GLOB '*[a-zA-Z]*' AND awardPrice NOT LIKE '%-%' AND awardPrice NOT LIKE '%*%' AND awardPrice NOT LIKE '%;%' ORDER BY awardPrice ASC",
    )
    df_contractU = create_df_from_query(
        conn,
        "SELECT lotsNumber, awardPrice From Lots WHERE typeOfContract = 'U' AND lotsNumber IS NOT null AND awardPrice IS NOT null AND awardPrice NOT GLOB '*[a-zA-Z]*' AND awardPrice NOT LIKE '%-%' AND awardPrice NOT LIKE '%*%' AND awardPrice NOT LIKE '%;%' ORDER BY awardPrice ASC",
    )
    df_contractS["lotsNumber"] = pd.to_numeric(
        df_contractS["lotsNumber"], errors="coerce"
    )
    df_contractW["lotsNumber"] = pd.to_numeric(
        df_contractW["lotsNumber"], errors="coerce"
    )
    df_contractU["lotsNumber"] = pd.to_numeric(
        df_contractU["lotsNumber"], errors="coerce"
    )
    draw_scatter_plots2(
        df_contractS,
        "lotsNumber",
        "awardPrice",
        "Scatterplot de awardPrice pour chaque element de lotsNumber en type de contrat S",
        "Lots",
        True,
        True,
    )
    draw_scatter_plots2(
        df_contractW,
        "lotsNumber",
        "awardPrice",
        "Scatterplot de awardPrice pour chaque element de lotsNumber en type de contrat W",
        "Lots",
        True,
        True,
    )
    draw_scatter_plots2(
        df_contractU,
        "lotsNumber",
        "awardPrice",
        "Scatterplot de awardPrice pour chaque element de lotsNumber en type de contrat U",
        "Lots",
        True,
        True,
    )


def draw_awardPrice_numberTendersSme(conn):
    df = create_df_from_query(
        conn,
        "SELECT awardPrice, numberTendersSme From Lots WHERE awardPrice IS NOT null and numberTendersSme IS NOT null ORDER BY awardPrice ASC",
    )
    draw_box_plot_multiple_numberTenders_NumberTendersSme(
        df,
        "numberTendersSme",
        "awardPrice",
        "Boxplot des awardPrice en fonction des numberTendersSme avec échelle logarithmique",
        "Lots",
        True,
    )
    df_contractS = create_df_from_query(
        conn,
        "SELECT awardPrice, numberTendersSme From Lots WHERE typeOfContract = 'S'",
    )
    df_contractW = create_df_from_query(
        conn,
        "SELECT awardPrice, numberTendersSme From Lots WHERE typeOfContract = 'W'",
    )
    df_contractU = create_df_from_query(
        conn,
        "SELECT awardPrice, numberTendersSme From Lots WHERE typeOfContract = 'U'",
    )
    draw_scatter_plots2(
        df_contractS,
        "awardPrice",
        "numberTendersSme",
        "Nuage de points des awardPrice et numberTendersSme de type de contrat 'S'",
        "Lots",
        True,
        True,
    )
    draw_scatter_plots2(
        df_contractW,
        "awardPrice",
        "numberTendersSme",
        "Nuage de points des awardPrice et numberTendersSme de type de contrat  'W'",
        "Lots",
        True,
        True,
    )
    draw_scatter_plots2(
        df_contractU,
        "awardPrice",
        "numberTendersSme",
        "Nuage de points des awardPrice et numberTendersSme de type de contrat  'U'",
        "Lots",
        True,
        True,
    )


def draw_awardPrice_subContracted(conn):
    df_contractS = create_df_from_query(
        conn,
        "SELECT awardPrice, subContracted From Lots WHERE typeOfContract = 'S' AND awardPrice IS NOT null and subContracted IS NOT null ORDER BY awardPrice ASC",
    )
    df_contractW = create_df_from_query(
        conn,
        "SELECT awardPrice, subContracted From Lots WHERE typeOfContract = 'W' AND awardPrice IS NOT null and subContracted IS NOT null ORDER BY awardPrice ASC",
    )
    df_contractU = create_df_from_query(
        conn,
        "SELECT awardPrice, subContracted From Lots WHERE typeOfContract = 'U' AND awardPrice IS NOT null and subContracted IS NOT null ORDER BY awardPrice ASC",
    )
    # print(df)
    draw_box_plot_multiple(
        df_contractS,
        f"subContracted",
        f"awardPrice",
        f"Boxplot des awardPrice en fonction des subContracted en type contrat 'S'",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contractW,
        f"subContracted",
        f"awardPrice",
        f"Boxplot des awardPrice en fonction des subContracted en type contrat 'W'",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contractU,
        f"subContracted",
        f"awardPrice",
        f"Boxplot des awardPrice en fonction des subContracted en type contrat 'U'",
        "Lots",
        True,
    )


# def draw_awardPrice_typeOfContract(conn):
#     df_contratS = create_df_from_query(
#         conn,
#         "SELECT awardPrice, typeOfContract From Lots WHERE typeOfContract = 'S'",
#     )
#     df_contratW = create_df_from_query(
#         conn,
#         "SELECT awardPrice, typeOfContract From Lots WHERE typeOfContract = 'W'",
#     )
#     df_contratU = create_df_from_query(
#         conn,
#         "SELECT awardPrice, typeOfContract From Lots WHERE typeOfContract = 'U'",
#     )
#     draw_box_plot_multiple(
#         df_contratS,
#         f"typeOfContract",
#         f"awardPrice",
#         f"Boxplot des awardPrice en fonction des typeOfContract de type 'S'",
#         "Lots",
#         True,
#     )
#     draw_box_plot_multiple(
#         df_contratW,
#         f"typeOfContract",
#         f"awardPrice",
#         f"Boxplot des awardPrice en fonction des typeOfContract de type 'W'",
#         "Lots",
#         True,
#     )
#     draw_box_plot_multiple(
#         df_contratU,
#         f"typeOfContract",
#         f"awardPrice",
#         f"Boxplot des awardPrice en fonction des typeOfContract de type 'U'",
#         "Lots",
#         True,
#     )


def draw_onBehalf_typeOfContract(conn):
    df = create_df_from_query(
        conn,
        "SELECT onBehalf, typeOfContract, count(onBehalf) AS 'NbonBehalf' FROM Lots GROUP BY onBehalf, typeOfContract",
    )
    # print(df)
    hist_pivot(
        df,
        "typeOfContract",
        "onBehalf",
        "Histogramme cumulé des onBehalf en fonction des typeOfContract",
        "Lots",
        False,
    )


def draw_awardEstimatedPrice_lotsNumber(conn):
    df_contractS = create_df_from_query(
        conn,
        "SELECT lotsNumber, awardEstimatedPrice From Lots WHERE typeOfContract = 'S' AND awardEstimatedPrice IS NOT null AND LotsNumber IS NOT null AND lotsNumber NOT GLOB '*[a-zA-Z]*' AND lotsNumber NOT LIKE '%-%' AND lotsNumber NOT LIKE '%*%' AND lotsNumber NOT LIKE '%;%' ORDER BY lotsNumber ASC",
    )
    df_contractW = create_df_from_query(
        conn,
        "SELECT lotsNumber, awardEstimatedPrice From Lots WHERE typeOfContract = 'W' AND awardEstimatedPrice IS NOT null AND LotsNumber IS NOT null AND lotsNumber NOT GLOB '*[a-zA-Z]*' AND lotsNumber NOT LIKE '%-%' AND lotsNumber NOT LIKE '%*%' AND lotsNumber NOT LIKE '%;%' ORDER BY lotsNumber ASC",
    )
    df_contractU = create_df_from_query(
        conn,
        "SELECT lotsNumber, awardEstimatedPrice From Lots WHERE typeOfContract = 'U' AND awardEstimatedPrice IS NOT null AND LotsNumber IS NOT null AND lotsNumber NOT GLOB '*[a-zA-Z]*' AND lotsNumber NOT LIKE '%-%' AND lotsNumber NOT LIKE '%*%' AND lotsNumber NOT LIKE '%;%' ORDER BY lotsNumber ASC",
    )
    # print(df)
    df_contractS["lotsNumber"] = pd.to_numeric(
        df_contractS["lotsNumber"], errors="coerce"
    )
    df_contractW["lotsNumber"] = pd.to_numeric(
        df_contractW["lotsNumber"], errors="coerce"
    )
    df_contractU["lotsNumber"] = pd.to_numeric(
        df_contractU["lotsNumber"], errors="coerce"
    )
    draw_scatter_plots2(
        df_contractS,
        "lotsNumber",
        "awardEstimatedPrice",
        "Scatterplot de lotsNumber pour chaque element de awardEstimatedPrice en type de contrat S",
        "Lots",
        True,
        True,
    )
    draw_scatter_plots2(
        df_contractW,
        "lotsNumber",
        "awardEstimatedPrice",
        "Scatterplot de lotsNumber pour chaque element de awardEstimatedPrice en type de contrat W",
        "Lots",
        True,
        True,
    )
    draw_scatter_plots2(
        df_contractU,
        "lotsNumber",
        "awardEstimatedPrice",
        "Scatterplot de lotsNumber pour chaque element de awardEstimatedPrice en type de contrat U",
        "Lots",
        True,
        True,
    )


def draw_awardPrice_onBehalf(conn):
    df_contract_S = create_df_from_query(
        conn, "SELECT onBehalf, awardPrice FROM Lots WHERE typeOfContract = 'S'"
    )
    df_contract_W = create_df_from_query(
        conn, "SELECT onBehalf, awardPrice FROM Lots WHERE typeOfContract = 'W'"
    )
    df_contract_U = create_df_from_query(
        conn, "SELECT onBehalf, awardPrice FROM Lots WHERE typeOfContract = 'U'"
    )
    draw_box_plot_multiple(
        df_contract_S,
        "onBehalf",
        "awardPrice",
        "Boxplot des onBehalf en fonction des awardPrice en type de contrat 'S'",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contract_W,
        "onBehalf",
        "awardPrice",
        "Boxplot des onBehalf en fonction des awardPrice en type de contrat 'W'",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contract_U,
        "onBehalf",
        "awardPrice",
        "Boxplot des onBehalf en fonction des awardPrice en type de contrat 'U",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT onBehalf as onBehalf, 'occurence' as awardPrice, count(awardPrice) as count
        FROM Lots
        WHERE onBehalf IS NOT NULL
        GROUP BY onBehalf

        UNION

        SELECT onBehalf as onBehalf, 'nullCount' as awardPrice, SUM(CASE WHEN awardPrice IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE onBehalf IS NOT NULL
        GROUP BY onBehalf;""",
    )
    draw_multiple_hist(
        df2,
        "onBehalf",
        "awardPrice",
        "Nombre d'occurence de awardPrice pour chaque element de onBehalf",
        "Lots",
        True,
    )


def draw_awardPrice_outOfDirectives(conn):
    df_contractS = create_df_from_query(
        conn, "SELECT outOfDirectives, awardPrice FROM Lots WHERE typeOfContract = 'S'"
    )
    df_contractW = create_df_from_query(
        conn, "SELECT outOfDirectives, awardPrice FROM Lots WHERE typeOfContract = 'W'"
    )
    df_contractU = create_df_from_query(
        conn, "SELECT outOfDirectives, awardPrice FROM Lots WHERE typeOfContract = 'U'"
    )
    draw_box_plot_multiple(
        df_contractS,
        "outOfDirectives",
        "awardPrice",
        "Boxplot des outOfDirectives en fonction des awardPrice en type de contrat S",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contractW,
        "outOfDirectives",
        "awardPrice",
        "Boxplot des outOfDirectives en fonction des awardPrice en type de contrat W",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contractU,
        "outOfDirectives",
        "awardPrice",
        "Boxplot des outOfDirectives en fonction des awardPrice en type de contrat U",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT outOfDirectives as outOfDirectives, 'occurence' as awardPrice, count(awardPrice) as count
        FROM Lots
        WHERE outOfDirectives IS NOT NULL
        GROUP BY outOfDirectives

        UNION

        SELECT outOfDirectives as outOfDirectives, 'nullCount' as awardPrice, SUM(CASE WHEN awardPrice IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE outOfDirectives IS NOT NULL
        GROUP BY outOfDirectives;""",
    )
    draw_multiple_hist(
        df2,
        "outOfDirectives",
        "awardPrice",
        "Nombre d'occurence de awardPrice pour chaque element de outOfDirectives",
        "Lots",
        True,
    )


def draw_awardPrice_accelerated(conn):
    df_contractS = create_df_from_query(
        conn, "SELECT accelerated, awardPrice FROM Lots WHERE typeOfContract = 'S'"
    )
    df_contractW = create_df_from_query(
        conn, "SELECT accelerated, awardPrice FROM Lots WHERE typeOfContract = 'W'"
    )
    df_contractU = create_df_from_query(
        conn, "SELECT accelerated, awardPrice FROM Lots WHERE typeOfContract = 'U'"
    )
    draw_box_plot_multiple(
        df_contractS,
        "accelerated",
        "awardPrice",
        "Boxplot des accelerated en fonction des awardPrice en type de contrat S",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contractW,
        "accelerated",
        "awardPrice",
        "Boxplot des accelerated en fonction des awardPrice en type de contrat W",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contractU,
        "accelerated",
        "awardPrice",
        "Boxplot des accelerated en fonction des awardPrice en type de contrat U",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT accelerated as accelerated, 'occurence' as awardPrice, count(awardPrice) as count
        FROM Lots
        WHERE accelerated IS NOT NULL
        GROUP BY accelerated

        UNION

        SELECT accelerated as accelerated, 'nullCount' as awardPrice, SUM(CASE WHEN awardPrice IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE accelerated IS NOT NULL
        GROUP BY accelerated;""",
    )
    draw_multiple_hist(
        df2,
        "accelerated",
        "awardPrice",
        "Nombre d'occurence de awardPrice pour chaque element de accelerated",
        "Lots",
        True,
    )


def draw_awardPrice_multipleCae(conn):
    df_contractS = create_df_from_query(
        conn, "SELECT multipleCae, awardPrice FROM Lots WHERE typeOfContract = 'S'"
    )
    df_contractW = create_df_from_query(
        conn, "SELECT multipleCae, awardPrice FROM Lots WHERE typeOfContract = 'W'"
    )
    df_contractU = create_df_from_query(
        conn, "SELECT multipleCae, awardPrice FROM Lots WHERE typeOfContract = 'U'"
    )
    # print(df)
    draw_box_plot_multiple(
        df_contractS,
        "multipleCae",
        "awardPrice",
        "Boxplot des multipleCae en fonction des awardPrice en type de contrat S",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contractW,
        "multipleCae",
        "awardPrice",
        "Boxplot des multipleCae en fonction des awardPrice en type de contrat W",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contractU,
        "multipleCae",
        "awardPrice",
        "Boxplot des multipleCae en fonction des awardPrice en type de contrat U",
        "Lots",
        True,
    )


def draw_awardPrice_topType(conn):
    df = create_df_from_query(conn, "SELECT topType, awardPrice FROM Lots")
    # print(df)
    draw_box_plot_multiple_dense_show_moy_med_up_and_down(
        df,
        "topType",
        "awardPrice",
        "Boxplot des topType en fonction des awardPrice avec échelle logarithmique",
        "Lots",
        True,
    )


def draw_awardPrice_contractDuration(conn):
    df_contratS = create_df_from_query(
        conn,
        "SELECT contractDuration, awardPrice FROM Lots WHERE typeOfContract = 'S' AND contractDuration IS NOT null AND awardPrice IS NOT null",
    )
    df_contraW = create_df_from_query(
        conn,
        "SELECT contractDuration, awardPrice FROM Lots WHERE typeOfContract = 'W' AND contractDuration IS NOT null AND awardPrice IS NOT null",
    )
    df_contratU = create_df_from_query(
        conn,
        "SELECT contractDuration, awardPrice FROM Lots WHERE typeOfContract = 'U' AND contractDuration IS NOT null AND awardPrice IS NOT null",
    )
    # print(df)
    draw_scatter_plots(
        df_contratS["contractDuration"],
        df_contratS["awardPrice"],
        "contractDuration",
        "awardPrice",
        "Scatter Plot of contractDuration vs awardPrice en type de contrat 'S'",
        False,
        True,
    )
    draw_scatter_plots(
        df_contraW["contractDuration"],
        df_contraW["awardPrice"],
        "contractDuration",
        "awardPrice",
        "Scatter Plot of contractDuration vs awardPrice en type de contrat 'W'",
        False,
        True,
    )
    draw_scatter_plots(
        df_contratU["contractDuration"],
        df_contratU["awardPrice"],
        "contractDuration",
        "awardPrice",
        "Scatter Plot of contractDuration vs awardPrice en type de contrat 'U'",
        False,
        True,
    )


def draw_awardPrice_publicityDuration(conn):
    df_contractS = create_df_from_query(
        conn,
        "SELECT publicityDuration, awardPrice FROM Lots WHERE typeOfContract = 'S' AND publicityDuration IS NOT null AND awardPrice IS NOT null",
    )
    df_contractW = create_df_from_query(
        conn,
        "SELECT publicityDuration, awardPrice FROM Lots WHERE typeOfContract = 'W' AND publicityDuration IS NOT null AND awardPrice IS NOT null",
    )
    df_contractU = create_df_from_query(
        conn,
        "SELECT publicityDuration, awardPrice FROM Lots WHERE typeOfContract = 'U' AND publicityDuration IS NOT null AND awardPrice IS NOT null",
    )
    # print(df)
    draw_scatter_plots(
        df_contractS["publicityDuration"],
        df_contractS["awardPrice"],
        "publicityDuration",
        "awardPrice",
        "Scatter Plot of publicityDuration vs awardPrice en type de contrast 'S'",
        False,
        True,
    )
    draw_scatter_plots(
        df_contractW["publicityDuration"],
        df_contractW["awardPrice"],
        "publicityDuration",
        "awardPrice",
        "Scatter Plot of publicityDuration vs awardPrice en type de contrast 'W'",
        False,
        True,
    )
    draw_scatter_plots(
        df_contractU["publicityDuration"],
        df_contractU["awardPrice"],
        "publicityDuration",
        "awardPrice",
        "Scatter Plot of publicityDuration vs awardPrice en type de contrast 'U'",
        False,
        True,
    )


def draw_accelerated_publicityDuration(conn):
    df = create_df_from_query(conn, "SELECT accelerated, publicityDuration FROM Lots")
    draw_box_plot_multiple(
        df,
        "accelerated",
        "publicityDuration",
        "Boxplot des accelerated en fonction des publicityDuration avec échelle logarithmique",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT accelerated as accelerated, 'occurence' as publicityDuration, count(publicityDuration) as count
        FROM Lots
        WHERE accelerated IS NOT NULL
        GROUP BY accelerated

        UNION

        SELECT accelerated as accelerated, 'nullCount' as publicityDuration, SUM(CASE WHEN publicityDuration IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE accelerated IS NOT NULL
        GROUP BY accelerated;""",
    )
    draw_multiple_hist(
        df2,
        "accelerated",
        "publicityDuration",
        "Nombre d'occurence de publicityDuration pour chaque element de accelerated",
        "Lots",
        True,
    )


def draw_accelerated_topType(conn):
    df = create_df_from_query(
        conn,
        f"SELECT topType, accelerated, COUNT(*) AS count FROM Lots GROUP BY topType, accelerated",
    )
    draw_multiple_hist(
        df,
        "topType",
        "accelerated",
        "Histogramme des accelerated en fonction des topType avec échelle logarithmique",
        "Lots",
        True,
        True,
        None,
        90,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT accelerated as accelerated, 'occurence' as topType, count(topType) as count
        FROM Lots
        WHERE accelerated IS NOT NULL
        GROUP BY accelerated

        UNION

        SELECT accelerated as accelerated, 'nullCount' as topType, SUM(CASE WHEN topType IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE accelerated IS NOT NULL
        GROUP BY accelerated;""",
    )
    draw_multiple_hist(
        df2,
        "accelerated",
        "topType",
        "Nombre d'occurence de topType pour chaque element de accelerated",
        "Lots",
        True,
    )


def draw_accelerated_typeOfContract(conn):
    df = create_df_from_query(
        conn,
        f"SELECT typeOfContract, accelerated, COUNT(*) AS count FROM Lots GROUP BY typeOfContract, accelerated",
    )
    draw_multiple_hist(
        df,
        "typeOfContract",
        "accelerated",
        "Histogramme des accelerated en fonction des typeOfContract avec échelle logarithmique",
        "Lots",
        False,
        False,
        None,
        90,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT accelerated as accelerated, 'occurence' as typeOfContract, count(typeOfContract) as count
        FROM Lots
        WHERE accelerated IS NOT NULL
        GROUP BY accelerated

        UNION

        SELECT accelerated as accelerated, 'nullCount' as typeOfContract, SUM(CASE WHEN typeOfContract IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE accelerated IS NOT NULL
        GROUP BY accelerated;""",
    )
    draw_multiple_hist(
        df2,
        "accelerated",
        "typeOfContract",
        "Nombre d'occurence de typeOfContract pour chaque element de accelerated",
        "Lots",
        False,
    )


def draw_accelerated_awardEstimatedPrice(conn):
    df_contractS = create_df_from_query(
        conn,
        "SELECT accelerated, awardEstimatedPrice FROM Lots WHERE typeOfContract = 'S'",
    )
    df_contractW = create_df_from_query(
        conn,
        "SELECT accelerated, awardEstimatedPrice FROM Lots WHERE typeOfContract = 'W'",
    )
    df_contractU = create_df_from_query(
        conn,
        "SELECT accelerated, awardEstimatedPrice FROM Lots WHERE typeOfContract = 'U'",
    )
    draw_box_plot_multiple(
        df_contractS,
        "accelerated",
        "awardEstimatedPrice",
        "Boxplot des accelerated en fonction des awardEstimatedPrice en type de contrast 'S'",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contractW,
        "accelerated",
        "awardEstimatedPrice",
        "Boxplot des accelerated en fonction des awardEstimatedPrice en type de contrast 'W'",
        "Lots",
        True,
    )
    draw_box_plot_multiple(
        df_contractU,
        "accelerated",
        "awardEstimatedPrice",
        "Boxplot des accelerated en fonction des awardEstimatedPrice en type de contrast 'U'",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT accelerated as accelerated, 'occurence' as awardEstimatedPrice, count(awardEstimatedPrice) as count
        FROM Lots
        WHERE accelerated IS NOT NULL
        GROUP BY accelerated

        UNION

        SELECT accelerated as accelerated, 'nullCount' as awardEstimatedPrice, SUM(CASE WHEN awardEstimatedPrice IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE accelerated IS NOT NULL
        GROUP BY accelerated;""",
    )
    draw_multiple_hist(
        df2,
        "accelerated",
        "awardEstimatedPrice",
        "Nombre d'occurence de awardEstimatedPrice pour chaque element de accelerated",
        "Lots",
        False,
    )


def draw_numberTenders_awardPrice(conn):
    df_contractS = create_df_from_query(
        conn,
        "SELECT numberTenders, awardPrice FROM Lots WHERE typeOfContract = 'S' AND numberTenders IS NOT null AND awardPrice IS NOT null",
    )
    df_contractW = create_df_from_query(
        conn,
        "SELECT numberTenders, awardPrice FROM Lots WHERE typeOfContract = 'W' AND numberTenders IS NOT null AND awardPrice IS NOT null",
    )
    df_contractU = create_df_from_query(
        conn,
        "SELECT numberTenders, awardPrice FROM Lots WHERE typeOfContract = 'U' AND numberTenders IS NOT null AND awardPrice IS NOT null",
    )
    # print(df)
    draw_scatter_plots(
        df_contractS["numberTenders"],
        df_contractS["awardPrice"],
        "numberTenders",
        "awardPrice",
        "Scatter Plot of numberTenders vs awardPrice en type de contrast 'S'",
        False,
        True,
    )
    draw_scatter_plots(
        df_contractW["numberTenders"],
        df_contractW["awardPrice"],
        "numberTenders",
        "awardPrice",
        "Scatter Plot of numberTenders vs awardPrice en type de contrast 'W'",
        False,
        True,
    )
    draw_scatter_plots(
        df_contractU["numberTenders"],
        df_contractU["awardPrice"],
        "numberTenders",
        "awardPrice",
        "Scatter Plot of numberTenders vs awardPrice en type de contrast 'U'",
        False,
        True,
    )


def draw_numberTendersSme_awardEstimatedPrice(conn):
    df_contractS = create_df_from_query(
        conn,
        "SELECT numberTendersSme, awardEstimatedPrice FROM Lots WHERE typeOfContract = 'S' AND numberTendersSme IS NOT null AND awardEstimatedPrice IS NOT null",
    )
    df_contractW = create_df_from_query(
        conn,
        "SELECT numberTendersSme, awardEstimatedPrice FROM Lots WHERE typeOfContract = 'W' AND numberTendersSme IS NOT null AND awardEstimatedPrice IS NOT null",
    )
    df_contractU = create_df_from_query(
        conn,
        "SELECT numberTendersSme, awardEstimatedPrice FROM Lots WHERE typeOfContract = 'U' AND numberTendersSme IS NOT null AND awardEstimatedPrice IS NOT null",
    )
    # print(df)
    draw_scatter_plots(
        df_contractS["numberTendersSme"],
        df_contractS["awardEstimatedPrice"],
        "numberTendersSme",
        "awardEstimatedPrice",
        "Scatter Plot of numberTendersSme vs awardEstimatedPrice en type de contrast 'S'",
        False,
        True,
    )
    draw_scatter_plots(
        df_contractW["numberTendersSme"],
        df_contractW["awardEstimatedPrice"],
        "numberTendersSme",
        "awardEstimatedPrice",
        "Scatter Plot of numberTendersSme vs awardEstimatedPrice en type de contrast 'W'",
        False,
        True,
    )
    draw_scatter_plots(
        df_contractU["numberTendersSme"],
        df_contractU["awardEstimatedPrice"],
        "numberTendersSme",
        "awardEstimatedPrice",
        "Scatter Plot of numberTendersSme vs awardEstimatedPrice en type de contrast 'U'",
        False,
        True,
    )


def draw_numberTenders_awardEstimatedPrice(conn):
    df_contratS = create_df_from_query(
        conn,
        "SELECT numberTenders, awardEstimatedPrice FROM Lots WHERE typeOfContract = 'S' AND numberTenders IS NOT null AND awardEstimatedPrice IS NOT null",
    )
    df_contraW = create_df_from_query(
        conn,
        "SELECT numberTenders, awardEstimatedPrice FROM Lots WHERE typeOfContract = 'W' AND numberTenders IS NOT null AND awardEstimatedPrice IS NOT null",
    )
    df_contratU = create_df_from_query(
        conn,
        "SELECT numberTenders, awardEstimatedPrice FROM Lots WHERE typeOfContract = 'U' AND numberTenders IS NOT null AND awardEstimatedPrice IS NOT null",
    )

    # print(df)
    draw_scatter_plots(
        df_contratS["numberTenders"],
        df_contratS["awardEstimatedPrice"],
        "numberTenders",
        "awardEstimatedPrice",
        "Scatter Plot of numberTenders vs awardEstimatedPrice en type de contrast 'S'",
        False,
        True,
    )
    draw_scatter_plots(
        df_contraW["numberTenders"],
        df_contraW["awardEstimatedPrice"],
        "numberTenders",
        "awardEstimatedPrice",
        "Scatter Plot of numberTenders vs awardEstimatedPrice en type de contrast 'W'",
        False,
        True,
    )
    draw_scatter_plots(
        df_contratU["numberTenders"],
        df_contratU["awardEstimatedPrice"],
        "numberTenders",
        "awardEstimatedPrice",
        "Scatter Plot of numberTenders vs awardEstimatedPrice en type de contrast 'U'",
        False,
        True,
    )


def draw_numberTendedrs_topType(conn):
    df = create_df_from_query(conn, "SELECT topType, numberTenders FROM Lots")
    draw_box_plot_multiple_dense(
        df,
        "topType",
        "numberTenders",
        "Boxplot des topType en fonction des numberTenders avec échelle logarithmique",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT topType as topType, 'occurence' as numberTenders, count(numberTenders) as count
            FROM Lots
            WHERE topType IS NOT NULL
            GROUP BY topType

            UNION

            SELECT topType as topType, 'nullCount' as numberTenders, SUM(CASE WHEN numberTenders IS NULL THEN 1 ELSE 0 END) as count
            FROM Lots
            WHERE topType IS NOT NULL
            GROUP BY topType
        """,
    )
    draw_multiple_hist(
        df2,
        "topType",
        "numberTenders",
        "Nombre d'occurence de numberTenders pour chaque element de topType",
        "Lots",
        True,
        True,
        30,
    )


def draw_numberTenders_contractorSme(conn):
    df = create_df_from_query(conn, "SELECT contractorSme, numberTenders FROM Lots")
    draw_box_plot_multiple(
        df,
        "contractorSme",
        "numberTenders",
        "Boxplot des contractorSme en fonction des numberTenders avec échelle logarithmique",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        conn,
        """SELECT contractorSme as contractorSme, 'occurence' as numberTenders, count(numberTenders) as count
        FROM Lots
        WHERE contractorSme IS NOT NULL
        GROUP BY contractorSme

        UNION

        SELECT contractorSme as contractorSme, 'nullCount' as numberTenders, SUM(CASE WHEN numberTenders IS NULL THEN 1 ELSE 0 END) as count
        FROM Lots
        WHERE contractorSme IS NOT NULL
        GROUP BY contractorSme;""",
    )
    draw_multiple_hist(
        df2,
        "contractorSme",
        "numberTenders",
        "Nombre d'occurence de numberTenders pour chaque element de contractorSme",
        "Lots",
        True,
    )


def draw_numberTenders_typeOfContract(conn):

    df = create_df_from_query(
        conn,
        "SELECT typeOfContract, numberTenders From Lots WHERE numberTenders IS NOT null and typeOfContract IS NOT null ORDER BY numberTenders ASC",
    )
    # print(df)
    draw_box_plot_multiple(
        df,
        "typeOfContract",
        "numberTenders",
        "Boxplot des typeOfContract en fonction des numberTenders",
        "Lots",
        True,
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
    df3 = create_df_from_query(
        conn,
        "SELECT typeOfContract, count(numberTenders) as 'NbnumberTenders', count(numberTendersSme) as 'NbnumberTendersSme' From Lots GROUP BY typeOfContract ORDER BY numberTenders ASC",
    )
    hist_pivot_multplie(
        df3,
        "typeOfContract",
        "NbnumberTenders",
        "NbnumberTendersSme",
        "Nombre d'occurence de numberTenders pour chaque element de typeOfContract",
        "Lots",
    )


def draw_numberTenders_numberTendersSme(conn):

    df = create_df_from_query(
        conn,
        "SELECT numberTenders, numberTendersSme From Lots WHERE numberTenders IS NOT null and numberTendersSme IS NOT null ORDER BY numberTenders ASC",
    )

    # print(df)
    draw_scatter_plots2(
        df,
        "numberTenders",
        "numberTendersSme",
        "Nuage de points des numberTendersSme en fonction des numberTenders",
        "Lots",
        True,
        True,
    )

    df_contratS = create_df_from_query(
        conn,
        "SELECT numberTenders, numberTendersSme From Lots WHERE typeOfContract = 'S' AND numberTenders IS NOT null and numberTendersSme IS NOT null ORDER BY numberTenders ASC",
    )
    df_contratW = create_df_from_query(
        conn,
        "SELECT numberTenders, numberTendersSme From Lots WHERE typeOfContract = 'W' AND numberTenders IS NOT null and numberTendersSme IS NOT null ORDER BY numberTenders ASC",
    )
    df_contratU = create_df_from_query(
        conn,
        "SELECT numberTenders, numberTendersSme From Lots WHERE typeOfContract = 'U' AND numberTenders IS NOT null and numberTendersSme IS NOT null ORDER BY numberTenders ASC",
    )

    draw_scatter_plots2(
        df_contratS,
        "numberTenders",
        "numberTendersSme",
        "Nuage de points des numberTendersSme en fonction des numberTenders en type de contrat 'S'",
        "Lots",
        True,
        True,
    )
    draw_scatter_plots2(
        df_contratW,
        "numberTenders",
        "numberTendersSme",
        "Nuage de points des numberTendersSme en fonction des numberTenders en type de contrat 'W'",
        "Lots",
        True,
        True,
    )
    draw_scatter_plots2(
        df_contratU,
        "numberTenders",
        "numberTendersSme",
        "Nuage de points des numberTendersSme en fonction des numberTenders en type de contrat 'U'",
        "Lots",
        True,
        True,
    )

    # print(df)
    draw_box_plot_multiple_numberTenders_NumberTendersSme(
        df_contratS,
        "numberTenders",
        "numberTendersSme",
        "Nombre d'occurence de numberTendersSme pour chaque element de numberTenders en type de contrast 'S'",
        "Lots",
        False,
        True,
    )
    draw_box_plot_multiple_numberTenders_NumberTendersSme(
        df_contratW,
        "numberTenders",
        "numberTendersSme",
        "Nombre d'occurence de numberTendersSme pour chaque element de numberTenders en type de contrast W'",
        "Lots",
        False,
        True,
    )
    draw_box_plot_multiple_numberTenders_NumberTendersSme(
        df_contratU,
        "numberTenders",
        "numberTendersSme",
        "Nombre d'occurence de numberTendersSme pour chaque element de numberTenders en type de contrast 'U'",
        "Lots",
        False,
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
    # print(df)
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
    df = create_df_from_query(
        conn,
        "SELECT cancelled, numberTenders FROM Lots WHERE cancelled IS NOT null AND numberTenders IS NOT null",
    )
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
        f"SELECT {colonne_1}, {colonne_2}, COUNT(*) AS count FROM Lots WHERE {colonne_1} = 1 GROUP BY {colonne_1}, {colonne_2}",
    )
    # print(df)
    draw_multiple_hist(
        df,
        f"{colonne_1}",
        f"{colonne_2}",
        f"Histogramme des {colonne_1} en fonction des {colonne_2} when cancelled is True",
        "Lots",
        True,
        True,
        20,
        90,
    )


def draw_cancelled_typeOfContract(connexion, colonne_1, colonne_2):
    df = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, {colonne_2}, COUNT(*) AS count FROM Lots WHERE {colonne_1} = 1 GROUP BY {colonne_1}, {colonne_2}",
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
    df_diff_contract = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, {colonne_2}, typeOfContract, ({colonne_1} - {colonne_2}) AS difference FROM Lots WHERE {colonne_1} IS NOT NULL AND {colonne_2} IS NOT NULL",
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
    draw_box_plot_multiple(
        df_diff_contract,
        "typeOfContract",
        "difference",
        f"Boxplot des différences des {colonne_1} et {colonne_2} en type de contrat",
        "Lots",
        True,
    )
    df_contratS = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, {colonne_2} FROM Lots WHERE typeOfContract = 'S' AND {colonne_1} IS NOT null AND {colonne_2} IS NOT null",
    )
    df_contraW = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, {colonne_2} FROM Lots WHERE typeOfContract = 'W' AND {colonne_1} IS NOT null AND {colonne_2} IS NOT null",
    )
    df_contratU = create_df_from_query(
        connexion,
        f"SELECT  {colonne_1}, {colonne_2} FROM Lots WHERE typeOfContract = 'U' AND {colonne_1} IS NOT null AND {colonne_2} IS NOT null",
    )
    # print(df)
    draw_scatter_plots(
        df_contratS[colonne_2],
        df_contratS[colonne_1],
        f"{colonne_2}",
        f"{colonne_1}",
        f"Nuage de points des {colonne_2} et {colonne_1} de type de contrat 'S'",
    )
    draw_scatter_plots(
        df_contraW[colonne_2],
        df_contraW[colonne_1],
        f"{colonne_2}",
        f"{colonne_1}",
        f"Nuage de points des {colonne_2} et {colonne_1} de type de contrat 'W'",
    )
    draw_scatter_plots(
        df_contratU[colonne_2],
        df_contratU[colonne_1],
        f"{colonne_2}",
        f"{colonne_1}",
        f"Nuage de points des {colonne_2} et {colonne_1} de type de contrat  'U'",
    )


def draw_numberTendersSme_typeOfContract(connexion, colonne_1, colonne_2):
    df = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, {colonne_2} from Lots WHERE {colonne_1} IS NOT NULL",
    )
    draw_box_plot_multiple(
        df,
        f"{colonne_2}",
        f"{colonne_1}",
        f"Boxplot des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique",
        "Lots",
        True,
    )


def draw_awardPrice_cpv(connexion, colonne_1, colonne_2):
    df = create_df_from_query(
        connexion,
        f"SELECT SUBSTR(CAST({colonne_2} AS TEXT), 1, 2)  AS {colonne_2}, {colonne_1} FROM Lots WHERE {colonne_1} IS NOT NULL",
    )
    draw_box_plot_multiple_simple_stats(
        df,
        f"{colonne_2}",
        f"{colonne_1}",
        f"Boxplot des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique",
        "Lots",
        True,
    )
    df2 = create_df_from_query(
        connexion,
        f"SELECT SUBSTR(CAST({colonne_2} AS TEXT), 1, 3) AS {colonne_2}, {colonne_1} FROM Lots WHERE {colonne_1} IS NOT NULL AND SUBSTR(CAST({colonne_2} AS TEXT), 1, 3) IN ( SELECT {colonne_2} FROM (SELECT SUBSTR(CAST({colonne_2} AS TEXT), 1, 3) AS {colonne_2}, COUNT(*) FROM Lots WHERE {colonne_1} IS NOT NULL GROUP BY SUBSTR(CAST({colonne_2} AS TEXT), 1, 3) ORDER BY COUNT(*) DESC LIMIT 45));",
    )
    draw_box_plot_multiple_simple_stats(
        df2,
        f"{colonne_2}",
        f"{colonne_1}",
        f"Boxplot des {colonne_1} en fonction des top 45 occurences de {colonne_2} avec échelle logarithmique",
        "Lots",
        True,
    )


def draw_awardPrice_fraAgreement(connexion, colonne_1, colonne_2):
    df = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, {colonne_2} from Lots WHERE {colonne_1} IS NOT NULL",
    )
    draw_box_plot_multiple(
        df,
        f"{colonne_2}",
        f"{colonne_1}",
        f"Boxplot des {colonne_1} en fonction des {colonne_2} avec échelle logarithmique",
        "Lots",
        True,
    )
