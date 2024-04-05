import re
from scriptReadSql import create_df_from_query
from scriptReadSql import *
from tabulate import tabulate
import numpy as np

def script_clean_variables_manually(connexion):
    ##############################################
    ################ Lot ###################
    ##############################################
    """awardDate"""
    # convert_abnormal_awardDate(connexion)
    # """accelerated"""
    # convert_null_accelerated(connexion)
    # """contractorSme"""
    # # convert_string_contractorSme(connexion)
    # """contractDuration"""
    # replace_abnormal_contractDuration(connexion)
    # """lotsNumber"""
    # replace_total_lotsNumber(connexion)
    # """publicityDuration"""
    # replace_values_publicityDuration(connexion)
    # """awardPrice""" 
    # replace_values_awardPrice(connexion)
    # """awardEstimatedPrice""" 
    # replace_values_awardEstimatedPrice(connexion)
    # """Difference_awardPrice_awardEstimatedPrice""" 
    # replace_difference_values_awardPrice_awardEstimatedPrice(connexion)
    # """numberTendersSme"""
    # replace_abnormal_numberTendersSme(connexion)


def convert_abnormal_awardDate(conn):
    df = create_df_from_query(
        conn,
        "SELECT lotId, tedCanId, awardDate FROM Lots WHERE CAST(strftime('%Y', awardDate) AS INTEGER) > 2020 OR CAST(strftime('%Y', awardDate) AS INTEGER) < 2010 GROUP BY strftime('%Y', awardDate)",
    )
    df["awardDate"] = pd.to_datetime(df["awardDate"])

    # Extraire les 4 premiers chiffres de tedCanId car c'est l'année de parution de l'offre
    df["yearFromId"] = (df["tedCanId"].astype(str).str[:4]).astype(int)

    # Remplacer dans awardDate
    df["awardDate"] = df.apply(
        lambda x: x["awardDate"].replace(year=int(x["yearFromId"])), axis=1
    )
    df = df.drop(columns=["yearFromId"])

    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute(
            "UPDATE Lots SET awardDate = ? WHERE lotId = ?",
            (str(row["awardDate"]), row["lotId"]),
        )
    conn.commit()
    print("Mise à jour effectuée avec succès.")


def convert_null_accelerated(conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE Lots SET accelerated = 0 WHERE accelerated IS NULL")
    conn.commit()
    print("Les valeurs NULL ont été remplacées par 0 dans la colonne 'accelerated'.")


def convert_string_contractorSme(conn):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Lots SET contractorSme = NULL WHERE contractorSme NOT IN ('0', '1')"
    )
    conn.commit()
    print("Mise à jour effectuée pour tous les contractorSme spécifiés.")

def replace_abnormal_contractDuration(conn):
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE Lots SET contractDuration = ROUND(contractDuration / 30.0, 2) WHERE contractDuration > 145 """
    )
    cursor.execute(
        """UPDATE Lots SET contractDuration = NULL WHERE SUBSTR(CAST(cpv AS TEXT), 1, 2) LIKE '45' AND contractDuration < 1"""
    )
    conn.commit()
    print("Mise à jour effectuée pour les contractDuration spécifiés.")

def replace_total_lotsNumber(conn):
    cursor = conn.cursor()
    df = create_df_from_query(conn, "SELECT * FROM Lots")
    df2 = create_df_from_query(
        conn,
        "WITH Counts AS ( SELECT tedCanId, COUNT(*) AS totalLots  FROM Lots  GROUP BY tedCanId ) SELECT Counts.totalLots FROM Lots JOIN Counts ON Lots.tedCanId = Counts.tedCanId"
    )
    df["totalLots"] = df2["totalLots"]

    df.to_sql(name='Lots', if_exists='replace', con=conn, index=False)
    print("Mise à jour effectuée pour les lotsNumber spécifiés.")


def replace_values_publicityDuration(conn):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Lots SET publicityDuration = NULL WHERE publicityDuration < 0 "
    )
    cursor.execute("UPDATE Lots SET publicityDuration = 5 WHERE publicityDuration < 6 ")
    cursor.execute(
        "UPDATE Lots SET publicityDuration = NULL WHERE publicityDuration > 144 "
    )
    conn.commit()
    print("Mise à jour effectuée pour tous les publicityDuration spécifiés.")


def replace_values_awardPrice(conn):
    df = create_df_from_query(
        conn,
        f"""SELECT lotId, awardPrice, typeOfContract, SUBSTR(CAST(cpv AS TEXT), 1, 2) AS cpv, subContracted, FLOOR(contractDuration / 12.0) AS contractDuration FROM Lots WHERE awardPrice IS NOT NULL""",
    )
    # Ajoutez la colonne 'group_id' qui concatène les colonnes sur lesquelles vous voulez grouper
    df['group_id'] = (
        df['typeOfContract'].astype(str) + "_" + 
        df['cpv'].astype(str).str[:2] + "_" +
        df['subContracted'].astype(str) + "_" +
        df['contractDuration'].astype(str)
    )
    # draw_boxplot_special_replace_abnormal_value_awardDate_and_awardEstimatedDate(df, "Lots", "Before")
    # # Calculer les whiskers chaque group_id
    q1 = df.groupby('group_id')['awardPrice'].quantile(0.25)
    q3 = df.groupby('group_id')['awardPrice'].quantile(0.75)
    iqr = q3 - q1

    whisker_high = q3 + 1.5 * iqr
    whisker_high_df = whisker_high.reset_index().rename(columns={'awardPrice': 'whisker_high'})
    df = pd.merge(df, whisker_high_df, on='group_id', how='left')
    df.loc[df['awardPrice'] > df['whisker_high'], 'awardPrice'] = np.nan

    whisker_low = q1 - 1.5 * iqr
    whisker_low_df = whisker_low.reset_index().rename(columns={'awardPrice': 'whisker_low'})
    df = pd.merge(df, whisker_low_df, on='group_id', how='left')
    df.loc[df['awardPrice'] < df['whisker_low'], 'awardPrice'] = np.nan

    # Mettre à jour la base de données
    df2 = create_df_from_query(conn, "SELECT * FROM Lots")

    merged_df = pd.merge(df2, df[['lotId', 'awardPrice']], on='lotId', how='left', suffixes=('', '_new'))
    merged_df['awardPrice'] = merged_df['awardPrice_new']
    merged_df.drop(columns=['awardPrice_new'], inplace=True)
    merged_df.to_sql(name='Lots', if_exists='replace', con=conn, index=False)

    print("Mise à jour effectuée pour tous les awardPrice spécifiés.")

    # draw_boxplot_special_replace_abnormal_value_awardDate_and_awardEstimatedDate(df, "Lots", "After")

def replace_values_awardEstimatedPrice(conn):
    df = create_df_from_query(
        conn,
        f"""SELECT lotId, awardEstimatedPrice, typeOfContract, SUBSTR(CAST(cpv AS TEXT), 1, 2) AS cpv, subContracted, FLOOR(contractDuration / 12.0) AS contractDuration FROM Lots WHERE awardEstimatedPrice IS NOT NULL""",
    )
    # Ajoutez la colonne 'group_id' qui concatène les colonnes sur lesquelles vous voulez grouper
    df['group_id'] = (
        df['typeOfContract'].astype(str) + "_" + 
        df['cpv'].astype(str).str[:2] + "_" +
        df['subContracted'].astype(str) + "_" +
        df['contractDuration'].astype(str)
    )
    # draw_boxplot_special_replace_abnormal_value_awardDate_and_awardEstimatedDate(df, "Lots", "Before")
    # # Calculer les whiskers chaque group_id
    q1 = df.groupby('group_id')['awardEstimatedPrice'].quantile(0.25)
    q3 = df.groupby('group_id')['awardEstimatedPrice'].quantile(0.75)
    iqr = q3 - q1

    whisker_high = q3 + 1.5 * iqr
    whisker_high_df = whisker_high.reset_index().rename(columns={'awardEstimatedPrice': 'whisker_high'})
    df = pd.merge(df, whisker_high_df, on='group_id', how='left')
    df.loc[df['awardEstimatedPrice'] > df['whisker_high'], 'awardEstimatedPrice'] = np.nan

    whisker_low = q1 - 1.5 * iqr
    whisker_low_df = whisker_low.reset_index().rename(columns={'awardEstimatedPrice': 'whisker_low'})
    df = pd.merge(df, whisker_low_df, on='group_id', how='left')
    df.loc[df['awardEstimatedPrice'] < df['whisker_low'], 'awardEstimatedPrice'] = np.nan

    # Mettre à jour la base de données
    df2 = create_df_from_query(
        conn,
        "SELECT * FROM Lots"
    )

    merged_df = pd.merge(df2, df[['lotId', 'awardEstimatedPrice']], on='lotId', how='left', suffixes=('', '_new'))
    merged_df['awardEstimatedPrice'] = merged_df['awardEstimatedPrice_new']
    merged_df.drop(columns=['awardEstimatedPrice_new'], inplace=True)
    merged_df.to_sql(name='Lots', if_exists='replace', con=conn, index=False)

    print("Mise à jour effectuée pour tous les awardEstimatedPrice spécifiés.")

    # draw_boxplot_special_replace_abnormal_value_awardDate_and_awardEstimatedDate(df, "Lots", "After")

def replace_difference_values_awardPrice_awardEstimatedPrice(conn):
    df = create_df_from_query(
        conn,
        f"""SELECT lotId, awardPrice, awardEstimatedPrice, (awardPrice - awardEstimatedPrice) AS difference, typeOfContract, SUBSTR(CAST(cpv AS TEXT), 1, 2) AS cpv, subContracted, FLOOR(contractDuration / 12.0) AS contractDuration FROM Lots WHERE awardEstimatedPrice IS NOT NULL AND awardPrice IS NOT NULL AND (awardPrice - awardEstimatedPrice) > 0""",
    )
    # Ajoutez la colonne 'group_id' qui concatène les colonnes sur lesquelles vous voulez grouper
    df['group_id'] = (
        df['typeOfContract'].astype(str) + "_" + 
        df['cpv'].astype(str).str[:2] + "_" +
        df['subContracted'].astype(str) + "_" +
        df['contractDuration'].astype(str)
    )
    # draw_boxplot_special_replace_abnormal_value_awardDate_and_awardEstimatedDate(df, "Lots", "Before")
    # # Calculer les whiskers chaque group_id
    q1 = df.groupby('group_id')['difference'].quantile(0.25)
    q3 = df.groupby('group_id')['difference'].quantile(0.75)
    iqr = q3 - q1

    whisker_high = q3 + 1.5 * iqr
    whisker_high_df = whisker_high.reset_index().rename(columns={'difference': 'whisker_high'})
    df = pd.merge(df, whisker_high_df, on='group_id', how='left')
    df.loc[df['difference'] > df['whisker_high'], 'awardPrice'] = df['awardEstimatedPrice']

    whisker_low = q1 - 1.5 * iqr
    whisker_low_df = whisker_low.reset_index().rename(columns={'difference': 'whisker_low'})
    df = pd.merge(df, whisker_low_df, on='group_id', how='left')
    df.loc[df['difference'] < df['whisker_low'], 'awardPrice'] = df['awardEstimatedPrice']

    # Mettre à jour la base de données
    df2 = create_df_from_query(
        conn,
        "SELECT * FROM Lots"
    )

    merged_df = pd.merge(df2, df[['lotId', 'awardPrice']], on='lotId', how='left', suffixes=('', '_new'))
    merged_df['awardPrice'] = merged_df['awardPrice_new']
    merged_df.drop(columns=['awardPrice_new'], inplace=True)
    merged_df.to_sql(name='Lots', if_exists='replace', con=conn, index=False)

    print("Mise à jour effectuée pour toutes les differences awardPrice spécifiés.")

    # draw_boxplot_special_replace_abnormal_value_awardDate_and_awardEstimatedDate(df, "Lots", "After")
    
def replace_abnormal_numberTendersSme(conn):
    cursor = conn.cursor()

    df = create_df_from_query(
        conn,
        f"""SELECT lotId, numberTenders, typeOfContract, SUBSTR(CAST(cpv AS TEXT), 1, 2) AS cpv, subContracted, FLOOR(contractDuration / 12.0) AS contractDuration FROM Lots WHERE numberTenders IS NOT NULL""",
    )
    # Ajoutez la colonne 'group_id' qui concatène les colonnes sur lesquelles vous voulez grouper
    df['group_id'] = (
        df['typeOfContract'].astype(str) + "_" + 
        df['cpv'].astype(str).str[:2] + "_" +
        df['subContracted'].astype(str) + "_" +
        df['contractDuration'].astype(str)
    )
    # draw_boxplot_special_replace_abnormal_value_awardDate_and_awardEstimatedDate(df, "Lots", "Before")
    # # Calculer les whiskers chaque group_id
    q1 = df.groupby('group_id')['numberTenders'].quantile(0.25)
    q3 = df.groupby('group_id')['numberTenders'].quantile(0.75)
    iqr = q3 - q1

    whisker_high = q3 + 1.5 * iqr
    whisker_high_df = whisker_high.reset_index().rename(columns={'numberTenders': 'whisker_high'})
    df = pd.merge(df, whisker_high_df, on='group_id', how='left')
    df.loc[df['numberTenders'] > df['whisker_high'], 'numberTenders'] = np.nan

    whisker_low = q1 - 1.5 * iqr
    whisker_low_df = whisker_low.reset_index().rename(columns={'numberTenders': 'whisker_low'})
    df = pd.merge(df, whisker_low_df, on='group_id', how='left')
    df.loc[df['numberTenders'] < df['whisker_low'], 'numberTenders'] = np.nan

    # Mettre à jour la base de données
    df2 = create_df_from_query(
        conn,
        "SELECT * FROM Lots"
    )

    merged_df = pd.merge(df2, df[['lotId', 'numberTenders']], on='lotId', how='left', suffixes=('', '_new'))
    merged_df['numberTenders'] = merged_df['numberTenders_new']
    merged_df.drop(columns=['numberTenders_new'], inplace=True)
    merged_df.to_sql(name='Lots', if_exists='replace', con=conn, index=False)

    # draw_boxplot_special_replace_abnormal_value_awardDate_and_awardEstimatedDate(df, "Lots", "After")

    cursor.execute(
        """UPDATE Lots SET numberTendersSme = numberTenders WHERE numberTendersSme > numberTenders"""
    )
    conn.commit()

    print("Mise à jour effectuée pour tous les numberTendersSme spécifiés.")
    
