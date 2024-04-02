from scriptReadSql import create_df_from_query
from scriptGraphics.drawBoxPlot import *
from scriptGraphics.drawHist import *
from scriptGraphics.drawScatterPlots import *
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
    """numberTenders & contractorSme (à voir)"""
    # draw_numberTenders_contractorSme(connexion)
    """numberTenders & topType"""
    # draw_numberTendedrs_topType(connexion)
    """numberTenders & typeOfContract"""
    # draw_numberTenders_typeOfContract(connexion)
    """numberTenders & awardEstimatedPrice"""
    # draw_numberTenders_awardEstimatedPrice(connexion)
    """numberTendersSme & awardEstimatedPrice"""
    # draw_numberTendersSme_awardEstimatedPrice(connexion)
    """numberTenders & awardPrice"""
    # draw_numberTenders_awardPrice(connexion)
    """accelerated & awardEstimatedPrice"""
    # draw_accelerated_awardEstimatedPrice(connexion)
    """accelerated & typeOfContract"""
    # draw_accelerated_typeOfContract(connexion)
    """accelerated & topType"""
    draw_accelerated_topType(connexion)


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
        True,
        True,
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
        True,
    )


def draw_accelerated_awardEstimatedPrice(conn):
    df = create_df_from_query(conn, "SELECT accelerated, awardEstimatedPrice FROM Lots")
    draw_box_plot_multiple(
        df,
        "accelerated",
        "awardEstimatedPrice",
        "Boxplot des accelerated en fonction des awardEstimatedPrice avec échelle logarithmique",
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
        True,
    )


def draw_numberTenders_awardPrice(conn):
    df = create_df_from_query(
        conn,
        "SELECT numberTendersSme, awardPrice FROM Lots WHERE numberTendersSme IS NOT null AND awardPrice IS NOT null",
    )
    print(df)
    draw_scatter_plots(
        df["numberTendersSme"],
        df["awardPrice"],
        "numberTendersSme",
        "awardPrice",
        "Scatter Plot of numberTendersSme vs awardPrice",
        False,
        True,
    )


def draw_numberTendersSme_awardEstimatedPrice(conn):
    df = create_df_from_query(
        conn,
        "SELECT numberTendersSme, awardEstimatedPrice FROM Lots WHERE numberTendersSme IS NOT null AND awardEstimatedPrice IS NOT null",
    )
    print(df)
    draw_scatter_plots(
        df["numberTendersSme"],
        df["awardEstimatedPrice"],
        "numberTendersSme",
        "awardEstimatedPrice",
        "Scatter Plot of numberTendersSme vs awardEstimatedPrice",
        False,
        True,
    )


def draw_numberTenders_awardEstimatedPrice(conn):
    df = create_df_from_query(
        conn,
        "SELECT numberTenders, awardEstimatedPrice FROM Lots WHERE numberTenders IS NOT null AND awardEstimatedPrice IS NOT null",
    )
    print(df)
    draw_scatter_plots(
        df["numberTenders"],
        df["awardEstimatedPrice"],
        "numberTenders",
        "awardEstimatedPrice",
        "Scatter Plot of numberTenders vs awardEstimatedPrice",
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
