from scriptReadSql import create_df_from_query
from scriptGraphics.drawBoxPlot import *
from scriptGraphics.drawHist import *
from tabulate import tabulate
from scriptReadSql import *


def script_single(connexion, cleaned):
    #################################################
    ##################### Lots ######################
    #################################################
    """correctionsNb"""
    draw_correctionsNb(connexion)
    """cancelled"""
    draw_cancelled(connexion)
    """awardDate"""
    draw_awardDate(connexion, 3)
    draw_awardDate(connexion, 5)
    draw_awardDate(connexion, 10)
    """cpv"""
    draw_cpv_lots(connexion)
    """numberTenders"""
    draw_numberTenders(connexion)
    """fraEstimated"""
    draw_fraEstimated(connexion)
    """numberTendersSme"""
    draw_numberTendersSme(connexion)
    """typeOfContract"""
    draw_typeOfContract(connexion)
    """topType"""
    draw_topType(connexion)
    """contractDuration"""
    draw_contract_duration(connexion)
    """publicityDuration"""
    draw_publicityDuration(connexion)
    #################################################
    #################### Agents #####################
    #################################################
    """siret"""
    draw_siret(connexion)
    """department"""
    draw_departement(connexion)
    #################################################
    ################### Criteria ####################
    #################################################
    """weight"""
    draw_weight(connexion)
    """type"""
    draw_type(connexion)
    if cleaned:
        """totalLots"""
        draw_totalLots(connexion, "totalLots")
        """awardEstimatedPrice"""
        draw_award_estimated_price(connexion, False)
        """awardPrice"""
        draw_award_price(connexion, False)
        draw_awardDate(connexion, 1)
    else:
        """lotsNumber"""
        draw_lotsNumber(connexion)
        """awardEstimatedPrice"""
        draw_award_estimated_price(connexion, True)
        """awardPrice"""
        draw_award_price(connexion, True)


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

    new_df = pd.DataFrame(
        {"siret_prefix": group_sizes.index, "count": group_sizes.values}
    )
    draw_box_plot_special(
        new_df, "count", "count", "Nombre de famile pour les même sirens", "Agents"
    )
    top_50_df = new_df.sort_values(by=["count"], ascending=False).head(50)
    draw_hist(
        top_50_df,
        "siret_prefix",
        "count",
        "Top 50 des entreprises avec le bâtiment",
        "Agents",
        True,
    )


def draw_type(conn):
    df = create_df_from_query(
        conn,
        "SELECT type, count(type) AS 'NbType' FROM Criteria GROUP BY type ORDER BY NbType DESC",
    )
    draw_hist(
        df,
        "type",
        "NbType",
        "Distribution des types avec échelle logarithmique",
        "Criteria",
        False,
    )


def draw_weight(conn):
    df = create_df_from_query(conn, "SELECT weight, type FROM Criteria")
    draw_box_plot_multiple_dense(
        df,
        "type",
        "weight",
        "Boxplot des poids avec échelle logarithmique",
        "Criteria",
        False,
    )
    df2 = create_df_from_query(
        conn, "SELECT weight FROM Criteria WHERE weight IS NOT NULL"
    )
    draw_custom_hist(
        df2,
        "weight",
        "weight",
        "Distribution des poids par tranche de 10",
        "Criteria",
        0,
        100,
        10,
    )


def draw_publicityDuration(conn):
    df = create_df_from_query(
        conn,
        "SELECT publicityDuration, count(publicityDuration) AS 'NbPublicityDuration' FROM Lots GROUP BY publicityDuration UNION ALL SELECT 'NaN' AS publicityDuration, COUNT(*) AS 'NbPublicityDuration' FROM Lots WHERE publicityDuration IS NULL ORDER BY NbPublicityDuration DESC",
    )
    draw_hist_with_errors(
        df,
        "publicityDuration",
        "NbPublicityDuration",
        "Distribution des publicityDuration",
        "Lots",
    )
    # Ajouter le catégorie en terme type contrat
    df2 = create_df_from_query(
        conn,
        f"SELECT typeOfContract, publicityDuration From Lots WHERE publicityDuration IS NOT null and typeOfContract IS NOT null ORDER BY publicityDuration ASC",
    )
    # draw_box_plot(
    #     df2,
    #     "publicityDuration",
    #     "publicityDuration",
    #     "Boxplot des publicityDuration",
    #     "Lots",
    #     True,
    # )
    draw_box_plot_multiple_dense(
        df2,
        "typeOfContract",
        "publicityDuration",
        "Boxplot des publicityDuration en fonction du type de contrat",
        "Lots",
        True,
    )


def draw_topType(conn):
    df = create_df_from_query(
        conn,
        "SELECT topType, count(toptype) AS 'NbToptype' FROM Lots GROUP BY topType ORDER BY NbTopType DESC",
    )
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
    draw_box_plot(
        df,
        "numberTendersSme",
        "numberTendersSme",
        "Boxplot des numberTendersSme avec échelle logarithmique",
        "Lots",
        True,
    )
    df3 = create_df_from_query(
        conn,
        "SELECT numberTendersSme FROM Lots WHERE numberTendersSme IS NOT NULL",
    )
    draw_custom_hist(
        df3,
        "numberTendersSme",
        "numberTendersSme",
        "Distribution des numberTendersSme par tranche de 10",
        "Lots",
        0,
        80,
        10,
    )
    df2 = create_df_from_query(
        conn,
        f"SELECT typeOfContract, numberTendersSme From Lots WHERE numberTendersSme IS NOT null and typeOfContract IS NOT null ORDER BY numberTendersSme ASC",
    )
    draw_box_plot_multiple_dense(
        df2,
        "typeOfContract",
        "numberTendersSme",
        "Boxplot des numberTendersSme en fonction du type de contrat",
        "Lots",
        True,
    )


def draw_lotsNumber(conn):
    df = create_df_from_query(
        conn,
        "SELECT lotsNumber, count(lotsNumber) AS 'NbLotsNumber' FROM Lots GROUP BY lotsNumber UNION ALL SELECT 'NaN' AS lotsNumber, COUNT(*) AS 'NbLotsNumber' FROM Lots WHERE lotsNumber IS NULL ORDER BY NbLotsNumber DESC",
    )
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
    df2 = create_df_from_query(
        conn,
        f"""SELECT lotsNumber, typeOfContract FROM Lots WHERE lotsNumber
        IS NOT NULL AND lotsNumber NOT GLOB '*[a-zA-Z]*' AND lotsNumber
        NOT LIKE '%-%' AND lotsNumber NOT LIKE '%*%' AND lotsNumber NOT LIKE '%;%' 
        AND lotsNumber NOT LIKE '% %' AND lotsNumber NOT LIKE '%.%' 
        AND lotsNumber NOT LIKE '%/%' AND lotsNumber NOT LIKE '%+%'
        AND lotsNumber NOT LIKE '%&%' AND lotsNumber NOT LIKE '%''%'""",
    )

    draw_box_plot_multiple_dense(
        df2,
        "typeOfContract",
        "lotsNumber",
        "Boxplot des lotsNumber en fonction du type de contrat",
        "Lots",
        True,
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
        data_count_elements,
        "Les éléments",
        "Nombre d'apparîtion",
        "Nombre d'apparitions de cancelled",
        "Lots",
        "cancelled",
        True,
    )


def draw_awardDate(conn, yearRange):
    rangeLoop = yearRange - 1
    rangeStr = str(yearRange)
    rows = select_awardDate_get_date_appearances(conn)

    data_date_appearances_by_each_year = {}
    data_date_appearances_by_each_decade = {}

    for row in rows:
        data_date_appearances_by_each_year[row[0]] = (
            row[2]
            if str(row[0]) not in data_date_appearances_by_each_year
            else data_date_appearances_by_each_year[row[0]] + row[2]
        )

    year_start = 0
    year_end = 0
    appearances = 0
    keys = list(data_date_appearances_by_each_year.keys())
    length = len(keys)

    year_start = keys[0]
    year_end = keys[-1]

    nbOfRange = (int(year_end) - int(year_start)) // yearRange

    for i in range(nbOfRange):
        year_range_end = int(year_start) + yearRange - 1
        data_date_appearances_by_each_decade[f"{year_start}-{year_range_end}"] = 0
        year_start = year_range_end + 1

    for index, key in enumerate(keys):
        value = data_date_appearances_by_each_year[key]
        current_year = int(key)
        for key in data_date_appearances_by_each_decade.keys():
            keySplit = key.split("-")
            if int(keySplit[0]) <= current_year and current_year <= int(keySplit[1]):

                data_date_appearances_by_each_decade[key] = (
                    data_date_appearances_by_each_decade[key] + value
                )
            else:
                appearances = 0

    filtered_data_date_appearances_by_each_decade = {
        key: value
        for key, value in data_date_appearances_by_each_decade.items()
        if value != 0
    }

    filtered_data_date_appearances_by_each_decade = pd.DataFrame(
        filtered_data_date_appearances_by_each_decade.items(),
        columns=[f"Chaque {yearRange} ans", "Value"],
    )
    draw_hist(
        filtered_data_date_appearances_by_each_decade,
        f"Chaque {yearRange} ans",
        "Value",
        f"awardDate_chaque_{yearRange}_ans",
        "Lots",
        True,
        45,
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
        f"SELECT {colonne_1} FROM Lots WHERE {colonne_1} IS NOT NULL",
    )
    draw_custom_hist(
        df,
        f"{colonne_1}",
        f"{colonne_1}",
        f"Occurences des {colonne_1} par tranche de 10",
        "Lots",
        0,
        130,
        10,
    )
    df2 = create_df_from_query(
        conn,
        f"SELECT typeOfContract, numberTenders From Lots WHERE numberTenders IS NOT null and typeOfContract IS NOT null ORDER BY numberTenders ASC",
    )
    draw_box_plot_special(
        df2,
        "numberTenders",
        "numberTenders",
        f"Boxplot des numberTenders avec échelle logarithmique",
        "Lots",
        True,
        True,
    )
    draw_box_plot_multiple_dense(
        df2,
        "typeOfContract",
        "numberTenders",
        "Boxplot des typeOfContract en fonction des numberTenders",
        "Lots",
        True,
    )
    df3 = create_df_from_query(
        conn,
        f"SELECT {colonne_1}, numberTendersSme FROM Lots WHERE {colonne_1} IS NOT NULL",
    )
    draw_custom_hist_cumul(
        df3,
        colonne_1,
        "numberTendersSme",
        f"Occurences des {colonne_1} par rapport au TendersSme par tranche de 10",
        "Lots",
        0,
        130,
        10,
    )


def draw_award_estimated_price(connexion, log):
    df = create_df_from_query(
        connexion,
        f"SELECT awardEstimatedPrice, COUNT(awardEstimatedPrice) AS 'NbawardEstimatedPrice' FROM Lots GROUP BY awardEstimatedPrice UNION ALL SELECT 'NaN' AS awardEstimatedPrice, COUNT(*) AS 'NbawardEstimatedPrice' FROM Lots WHERE awardEstimatedPrice IS NULL ORDER BY NbawardEstimatedPrice DESC",
    )
    draw_awardEstimatedPrice_2(connexion, log)
    df2 = create_df_from_query(
        connexion,
        f"SELECT typeOfContract, awardEstimatedPrice From Lots WHERE awardEstimatedPrice IS NOT null and typeOfContract IS NOT null ORDER BY awardEstimatedPrice ASC",
    )
    draw_box_plot_special(
        df2,
        "awardEstimatedPrice",
        "awardEstimatedPrice",
        f"Boxplot des awardEstimatedPrice avec échelle logarithmique",
        "Lots",
        log,
        True,
    )
    draw_box_plot_multiple_dense(
        df2,
        "typeOfContract",
        "awardEstimatedPrice",
        "Boxplot des typeOfContract en fonction des awardEstimatedPrice",
        "Lots",
        log,
    )


def draw_awardEstimatedPrice_2(conn, log):
    colonne_1 = "awardEstimatedPrice"
    df = create_df_from_query(
        conn,
        f"SELECT {colonne_1}, COUNT({colonne_1}) AS 'Nb{colonne_1}' FROM Lots GROUP BY {colonne_1} UNION ALL SELECT 'NaN' AS {colonne_1}, COUNT(*) AS 'Nb{colonne_1}' FROM Lots WHERE {colonne_1} IS NULL ORDER BY Nb{colonne_1} DESC",
    )
    df_cleaned = df.dropna(subset=["awardEstimatedPrice"])

    # Convert 'awardEstimatedPrice' to numeric type
    df_cleaned["awardEstimatedPrice"] = pd.to_numeric(
        df_cleaned["awardEstimatedPrice"], errors="coerce"
    )
    draw_custom_hist(
        df,
        f"{colonne_1}",
        f"Nb{colonne_1}",
        f"Occurences des {colonne_1} par tranche de 100",
        "Lots",
        df_cleaned["awardEstimatedPrice"].min(),
        df_cleaned["awardEstimatedPrice"].max(),
        df_cleaned["awardEstimatedPrice"].max() / 5000,
        log,
    )


def draw_award_price(connexion, log):
    draw_awardPrice_2(connexion, log)
    df = create_df_from_query(
        connexion,
        f"SELECT awardPrice From Lots WHERE awardPrice IS NOT null",
    )
    df2 = create_df_from_query(
        connexion,
        f"SELECT typeOfContract, awardPrice From Lots WHERE awardPrice IS NOT null and typeOfContract IS NOT null",
    )
    draw_box_plot_special(
        df,
        "awardPrice",
        "awardPrice",
        f"Boxplot des awardPrice",
        "Lots",
        log,
        True,
    )
    draw_box_plot_multiple_dense(
        df2,
        "typeOfContract",
        "awardPrice",
        "Boxplot des typeOfContract en fonction des awardPrice",
        "Lots",
        log,
    )


def draw_awardPrice_2(conn, log):
    df = create_df_from_query(
        conn,
        "SELECT awardPrice, COUNT(awardPrice) AS 'NbAwardPrice' FROM Lots GROUP BY awardPrice UNION ALL SELECT 'NaN' AS awardPrice, COUNT(*) AS 'NbAwardPrice' FROM Lots WHERE awardPrice IS NULL ORDER BY NbAwardPrice DESC",
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
        log,
    )


def draw_fraEstimated(conn):
    df = create_df_from_query(
        conn,
        "SELECT fraEstimated, count(fraEstimated) AS 'NbFraEstimated' FROM Lots GROUP BY fraEstimated UNION ALL SELECT 'NaN' AS fraEstimated, COUNT(*) AS 'NbFraEstimated' FROM Lots WHERE fraEstimated IS NULL ORDER BY NbFraEstimated DESC",
    )
    draw_hist(df, "fraEstimated", "NbFraEstimated", "fraEstimated", "Lots", True)


def draw_contract_duration(connexion):
    df = create_df_from_query(
        connexion,
        f"SELECT contractDuration, COUNT(contractDuration) AS 'NbcontractDuration' FROM Lots GROUP BY contractDuration UNION ALL SELECT 'NaN' AS contractDuration, COUNT(*) AS 'NbcontractDuration' FROM Lots WHERE contractDuration IS NULL ORDER BY NbcontractDuration DESC",
    )
    draw_hist_with_errors(
        df,
        "contractDuration",
        "NbcontractDuration",
        "Distribution des contractDuration",
        "Lots",
    )
    # Ajouter le catégorie en terme type contrat
    df2 = create_df_from_query(
        connexion,
        f"SELECT typeOfContract, contractDuration From Lots WHERE contractDuration IS NOT null and typeOfContract IS NOT null ORDER BY contractDuration ASC",
    )
    draw_box_plot_special(
        df2,
        "contractDuration",
        "contractDuration",
        f"Boxplot des contractDuration avec échelle logarithmique",
        "Lots",
        True,
        True,
    )
    draw_box_plot_multiple_dense(
        df2,
        "typeOfContract",
        "contractDuration",
        "Boxplot des typeOfContract en fonction des contractDuration",
        "Lots",
        True,
    )


def draw_totalLots(conn, colonne_1):
    df = create_df_from_query(
        conn,
        f"SELECT {colonne_1} FROM Lots WHERE {colonne_1} IS NOT NULL",
    )

    draw_box_plot(
        df,
        colonne_1,
        colonne_1,
        f"Boxplot des {colonne_1} avec échelle logarithmique",
        "Lots",
        True,
    )

    df2 = create_df_from_query(
        conn,
        f"SELECT {colonne_1}, typeOfContract FROM Lots WHERE {colonne_1} IS NOT NULL",
    )

    draw_box_plot_multiple_dense(
        df2,
        "typeOfContract",
        colonne_1,
        f"Boxplot des {colonne_1} en fonction du type de contrat",
        "Lots",
        True,
    )
