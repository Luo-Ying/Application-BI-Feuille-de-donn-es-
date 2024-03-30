from scriptReadSql import *
from scriptGraphics.drawHist import *
from scriptGraphics.drawBoxPlot import *


def draw_correctionsNb(conn):
    df = create_df_from_query(
        conn,
        "SELECT correctionsNb FROM Lots",
    )
    draw_box_plot(
        df,
        "correctionsNb",
        "correctionsNb",
        "Boxplot des correctionNb avec échelle logarithmique",
        "Lots",
        log=False,
    )


def draw_cancelled(conn):

    rows = select_cancelled_count_diff_elements(conn)
    data_count_elements = {}

    for row in rows:
        data_count_elements[str(row[0])] = row[1]

    draw_bar(
        data_count_elements, "Les éléments", "nombre d'appaîtion", "cancelled", True
    )


def draw_awardDate(conn, range):
    rangeLoop = range - 1
    rangeStr = str(range)
    rows = select_awardDate_get_date_appearances(conn)

    data_date_appearances_by_each_year = {}
    data_date_appearances_by_each_decade = {}

    for row in rows:
        data_date_appearances_by_each_year[row[0]] = (
            row[2]
            if str(row[0]) not in data_date_appearances_by_each_year
            else data_date_appearances_by_each_year[row[0]] + row[2]
        )

    print(data_date_appearances_by_each_year)

    year_start = 0
    year_end = 0
    appearances = 0
    keys = list(data_date_appearances_by_each_year.keys())
    length = len(keys)
    for index, key in enumerate(keys):
        value = data_date_appearances_by_each_year[key]
        year_end = int(key)
        if year_start == 0:
            year_start = int(key)
        appearances += value
        if year_end - year_start >= rangeLoop or index == length - 1:
            data_date_appearances_by_each_decade[f"{year_start}-{year_end}"] = (
                appearances
            )
            appearances = 0
            year_start = year_end
            year_end = 0

    print(data_date_appearances_by_each_decade)
    draw_bar(
        data_date_appearances_by_each_decade,
        f"Chaque {rangeStr} ans",
        "Nombre d'appaîtion",
        "awardDate",
        "Lots",
        False,
    )


def draw_publicityDuration(conn):
    df = create_df_from_query(
        conn,
        "SELECT publicityDuration, count(publicityDuration) AS 'NbPublicityDuration' FROM Lots GROUP BY publicityDuration UNION ALL SELECT 'NaN' AS publicityDuration, COUNT(*) AS 'NbPublicityDuration' FROM Lots WHERE publicityDuration IS NULL ORDER BY NbPublicityDuration DESC",
    )
    draw_box_plot(
        df,
        "publicityDuration",
        "NbPublicityDuration",
        "Boxplot des publicityDuration avec échelle logarithmique",
        "Lots",
        True,
    )


def draw_awardEstimatedPrice(conn):
    colonne_1 = "awardEstimatedPrice"
    df = create_df_from_query(
        conn,
        f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} UNION ALL SELECT 'NaN' AS {colonne_1}, COUNT(*) AS 'Nb{colonne_1}' FROM Lots WHERE {colonne_1} IS NULL ORDER BY Nb{colonne_1} DESC",
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_box_plot(
        df,
        f"{colonne_1}",
        f"{colonne_1}",
        f"Boxplot des {colonne_1} avec échelle logarithmique",
        "Lots",
        True,
    )
    draw_custom_hist(
        df,
        f"{colonne_1}",
        f"Nb{colonne_1}",
        f"Occurences des {colonne_1} par tranche de 100",
        "Lots",
        0,
        2500,
        100,
    )


def draw_awardPrice(conn):
    df = create_df_from_query(
        conn,
        "SELECT awardPrice, COUNT(awardPrice) AS 'NbAwardPrice' FROM Lots GROUP BY awardPrice UNION ALL SELECT 'NaN' AS awardPrice, COUNT(*) AS 'NbAwardPrice' FROM Lots WHERE awardPrice IS NULL ORDER BY NbAwardPrice DESC",
    )
    # print(tabulate(df, headers="keys", tablefmt="psql"))
    draw_box_plot(
        df,
        "awardPrice",
        "awardPrice",
        "Boxplot des awardPrice avec échelle logarithmique",
        "Lots",
        True,
    )
    draw_custom_hist(
        df,
        "awardPrice",
        "NbAwardPrice",
        "Occurences des awardPrice par tranche de 1000",
        "Lots",
        0,
        17000,
        1000,
    )


def draw_numberTenders(conn):
    colonne_1 = "numberTenders"
    df = create_df_from_query(
        conn,
        f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1}",
    )
    # print(tabulate(df, headers="keys", tablefmt="psql"))
    draw_box_plot(
        df,
        f"{colonne_1}",
        f"{colonne_1}",
        f"Boxplot des {colonne_1} avec échelle logarithmique",
        "Lots",
        True,
    )
    draw_custom_hist(
        df,
        f"{colonne_1}",
        f"Nb{colonne_1}",
        f"Occurences des {colonne_1} par tranche de 100",
        "Lots",
        0,
        1000,
        100,
    )


def draw_fraEstimated(conn):
    df = create_df_from_query(
        conn,
        "SELECT fraEstimated, count(fraEstimated) AS 'NbFraEstimated' FROM Lots GROUP BY fraEstimated UNION ALL SELECT 'NaN' AS fraEstimated, COUNT(*) AS 'NbFraEstimated' FROM Lots WHERE fraEstimated IS NULL ORDER BY NbFraEstimated DESC",
    )
    draw_hist(df, "fraEstimated", "NbFraEstimated", "fraEstimated", "Lots", True)


def draw_lotsNumber(conn):
    df = create_df_from_query(
        conn,
        "SELECT lotsNumber, count(lotsNumber) AS 'NbLotsNumber' FROM Lots GROUP BY lotsNumber UNION ALL SELECT 'NaN' AS lotsNumber, COUNT(*) AS 'NbLotsNumber' FROM Lots WHERE lotsNumber IS NULL ORDER BY NbLotsNumber DESC",
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_hist_with_errors(
        df, "lotsNumber", "NbLotsNumber", "Distribution des lotsNumber", "Lots"
    )
    draw_custom_hist(
        df,
        "lotsNumber",
        "NbLotsNumber",
        "Distribution des lotsNumber par tranche de 25000",
        "Lots",
        0,
        250000,
        25000,
    )


def draw_topType(conn):
    df = create_df_from_query(
        conn,
        "SELECT topType, count(toptype) AS 'NbToptype' FROM Lots GROUP BY topType ORDER BY NbTopType DESC",
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_hist(df, "topType", "NbToptype", "Distribution des topType", "Lots")
