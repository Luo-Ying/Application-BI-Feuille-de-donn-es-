from scriptReadSql import create_df_from_query
from scriptGraphics.drawBoxPlot import (
    draw_box_plot,
    draw_box_plot_multiple,
    draw_box_plot_special,
)
from scriptGraphics.drawHist import (
    draw_hist,
    draw_custom_hist,
    draw_hist_with_errors,
    draw_bar,
)
from tabulate import tabulate
from scriptReadSql import *


def script_single(connexion):
    #################################################
    ##################### Lots ######################
    #################################################
    """correctionsNb"""
    # draw_correctionsNb(connexion)
    """cancelled"""
    # draw_cancelled(connexion)
    """awardDate"""
    # draw_awardDate(connexion, 5)
    # draw_awardDate(connexion, 10)
    # draw_awardDate(connexion, 15)
    # draw_awardDate(connexion, 20)
    """awardEstimatedPrice"""
    # draw_award_estimated_price(connexion, "awardEstimatedPrice")
    """awardPrice"""
    # draw_award_price(connexion, "awardPrice")
    """cpv"""
    # draw_cpv_lots(connexion)
    """numberTenders"""
    # draw_numberTenders(connexion)
    """fraEstimated"""
    # draw_fraEstimated(connexion)
    """lotsNumber"""
    # draw_lotsNumber(connexion)
    """numberTendersSme"""
    # draw_numberTendersSme(connexion)
    """typeOfContract"""
    # draw_typeOfContract(connexion)
    """topType"""
    # draw_topType(connexion)
    """contractDuration"""
    # draw_contract_duration(connexion, "contractDuration")
    """publicityDuration"""
    # draw_publicityDuration(connexion)
    #################################################
    #################### Agents #####################
    #################################################
    """siret"""
    # draw_siret(connexion)
    """department"""
    # draw_departement(connexion)
    #################################################
    ################### Criteria ####################
    #################################################
    """weight"""
    # draw_weight(connexion)
    """type"""
    # draw_type(connexion)
    """totalLots"""
    # draw_totalLots(connexion, "totalLots")


def draw_departement(conn):
    df = create_df_from_query(
        conn,
        "SELECT distinct department, count(department) as 'Nombre Agents' FROM Agents WHERE department IS NOT null GROUP BY department;",
    )
    draw_hist(
        df, "department", "Nombre Agents", "Nombre Agents par département", "Agents"
    )
    df.drop(columns=["department"], inplace=True)
    draw_box_plot_special(
        df,
        "Nombre Agents",
        "Nombre Agents",
        "Nombre d'Agents par département",
        "Agents",
    )


def draw_siret(conn):
    df = create_df_from_query(
        conn,
        "SELECT siret FROM Agents WHERE siret is not null",
    )

    data_group = {}

    df["siret_prefix"] = df["siret"].str[:9]

    groups = df.groupby(
        "siret_prefix"
    )  # 9 premières chiffre => le siren de l'entreprise
    group_sizes = groups.size()

    for name, size in group_sizes.items():
        data_group[name] = size

    # print(df)
    new_df = pd.DataFrame(
        {"siret_prefix": group_sizes.index, "count": group_sizes.values}
    )
    # print(new_df["count"])
    # print(data_group)
    draw_box_plot_special(
        new_df, "count", "count", "Nombre de famile pour les même sirens", "Agents"
    )


def draw_type(conn):
    df = create_df_from_query(
        conn,
        "SELECT type, count(type) AS 'NbType' FROM Criteria GROUP BY type ORDER BY NbType DESC",
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_hist(
        df,
        "type",
        "NbType",
        "Distribution des types avec échelle logarithmique",
        "Criteria",
        False,
    )


def draw_weight(conn):
    df = create_df_from_query(
        conn, "SELECT weight, count(weight) AS 'NbWeight' FROM Criteria GROUP BY weight"
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_box_plot(
        df,
        "weight",
        "weight",
        "Boxplot des poids avec échelle logarithmique",
        "Criteria",
        True,
    )
    draw_custom_hist(
        df,
        "weight",
        "NbWeight",
        "Distribution des poids par tranche de 50000",
        "Criteria",
        0,
        500000,
        50000,
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
    draw_hist_with_errors(
        df,
        "publicityDuration",
        "NbPublicityDuration",
        "Distribution des publicityDuration",
        "Lots",
    )


def draw_topType(conn):
    df = create_df_from_query(
        conn,
        "SELECT topType, count(toptype) AS 'NbToptype' FROM Lots GROUP BY topType ORDER BY NbTopType DESC",
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_hist(df, "topType", "NbToptype", "Distribution des topType", "Lots")


def draw_typeOfContract(conn):
    colonne_1 = "typeOfContract"
    df2 = create_df_from_query(
        conn,
        f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} ORDER BY Nb{colonne_1} DESC",
    )
    draw_hist(
        df2,
        f"{colonne_1}",
        f"Nb{colonne_1}",
        f"Distribution des {colonne_1} avec échelle logarithmique",
        "Lots",
        True,
    )


def draw_numberTendersSme(conn):
    df = create_df_from_query(
        conn,
        "SELECT numberTendersSme, count(numberTendersSme) AS 'NbNumberTendersSme' FROM Lots GROUP BY numberTendersSme",
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_box_plot(
        df,
        "numberTendersSme",
        "numberTendersSme",
        "Boxplot des numberTendersSme sans échelle logarithmique",
        "Lots",
    )
    draw_custom_hist(
        df,
        "numberTendersSme",
        "NbNumberTendersSme",
        "Distribution des numberTendersSme par tranche de 100",
        "Lots",
        0,
        1000,
        100,
    )


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

    # print(data_date_appearances_by_each_year)

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

    # print(data_date_appearances_by_each_decade)
    draw_bar(
        data_date_appearances_by_each_decade,
        f"Chaque {rangeStr} ans",
        "Nombre d'appaîtion",
        "awardDate",
        "Lots",
        False,
    )


def draw_cpv_lots(connexion):
    df = create_df_from_query(
        connexion,
        "SELECT SUBSTR(cpv,1,2) AS cpv, COUNT(*) AS count FROM Lots GROUP BY SUBSTR(cpv,1,2)",
    )
    df2 = create_df_from_query(
        connexion,
        "SELECT SUBSTR(cpv,1,3) AS cpv, COUNT(*) AS count FROM Lots GROUP BY SUBSTR(cpv,1,3) ORDER BY count DESC LIMIT 45",
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_hist(
        df, "cpv", "count", "Distribution des cpv par 2 premiers chiffres", "Lots"
    )
    draw_hist(
        df2,
        "cpv",
        "count",
        "Distribution des 45 premiers cpv par 3 premiers chiffres",
        "Lots",
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


def draw_award_estimated_price(connexion, colonne_1):
    df = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} UNION ALL SELECT 'NaN' AS {colonne_1}, COUNT(*) AS 'Nb{colonne_1}' FROM Lots WHERE {colonne_1} IS NULL ORDER BY Nb{colonne_1} DESC",
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_box_plot_special(
        df,
        f"{colonne_1}",
        f"{colonne_1}",
        f"Boxplot des {colonne_1} avec échelle logarithmique",
        "Lots",
        True,
        True,
    )
    draw_awardEstimatedPrice_2(connexion)


def draw_awardEstimatedPrice_2(conn):
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


def draw_award_price(connexion, colonne_1):
    df = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} UNION ALL SELECT 'NaN' AS {colonne_1}, COUNT(*) AS 'Nb{colonne_1}' FROM Lots WHERE {colonne_1} IS NULL ORDER BY Nb{colonne_1} DESC",
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_box_plot_special(
        df,
        f"{colonne_1}",
        f"{colonne_1}",
        f"Boxplot des {colonne_1} avec échelle logarithmique",
        "Lots",
        True,
        True,
    )
    draw_awardPrice_2(connexion)


def draw_awardPrice_2(conn):
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


def draw_fraEstimated(conn):
    df = create_df_from_query(
        conn,
        "SELECT fraEstimated, count(fraEstimated) AS 'NbFraEstimated' FROM Lots GROUP BY fraEstimated UNION ALL SELECT 'NaN' AS fraEstimated, COUNT(*) AS 'NbFraEstimated' FROM Lots WHERE fraEstimated IS NULL ORDER BY NbFraEstimated DESC",
    )
    draw_hist(df, "fraEstimated", "NbFraEstimated", "fraEstimated", "Lots", True)


def draw_contract_duration(connexion, colonne_1):
    df = create_df_from_query(
        connexion,
        f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} UNION ALL SELECT 'NaN' AS {colonne_1}, COUNT(*) AS 'Nb{colonne_1}' FROM Lots WHERE {colonne_1} IS NULL ORDER BY Nb{colonne_1} DESC",
    )
    # print(tabulate(df, headers='keys', tablefmt='psql'))
    draw_box_plot_special(
        df,
        f"{colonne_1}",
        f"{colonne_1}",
        f"Boxplot des {colonne_1} avec échelle logarithmique",
        "Lots",
        True,
        True,
    )
    # print(df)
    draw_hist_with_errors(
        df,
        "contractDuration",
        "NbcontractDuration",
        "Distribution des contractDuration",
        "Lots",
    )

def draw_totalLots(conn, colonne_1): 
    df = create_df_from_query(
        conn,
         f"SELECT {colonne_1} FROM Lots",
    )

    draw_box_plot(
        df,
        colonne_1,
        colonne_1,
        f"Boxplot des {colonne_1} avec échelle logarithmique",
        "Lots",
        True,
    )