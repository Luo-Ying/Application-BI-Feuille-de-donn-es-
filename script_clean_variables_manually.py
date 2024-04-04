import re
from scriptReadSql import create_df_from_query
from scriptReadSql import *
from tabulate import tabulate

def script_clean_variables_manually(connexion):
    ##############################################
    ################ Lot ###################
    ##############################################
    """awardDate"""
    # convert_abnormal_awardDate(connexion)
    """accelerated"""
    # convert_null_accelerated(connexion)
    """contractorSme"""
    # convert_string_contractorSme(connexion)
    """numberTendersSme"""
    # replace_abnormal_numberTendersSme(connexion)
    """contractDuration"""
    # replace_abnormal_contractDuration(connexion)
    """awardPrice"""
    clean_awardPrice(connexion)

def clean_awardPrice(conn):
    # Fetching top contract for type 'S'
    df_top1_contractS = create_df_from_query(
        conn,
        "SELECT lotId, awardPrice, awardEstimatedPrice, typeOfContract FROM Lots WHERE typeOfContract = 'S' ORDER BY awardPrice DESC LIMIT 1;"
    )

    # Fetching top contract for type 'U'
    df_top1_contractU = create_df_from_query(
        conn,
        "SELECT lotId, awardPrice, awardEstimatedPrice, typeOfContract FROM Lots WHERE typeOfContract = 'U' ORDER BY awardPrice DESC LIMIT 1;"
    )

    # Modifying awardPrice based on awardEstimatedPrice for contractS
    df_top1_contractS['awardPrice'] = df_top1_contractS['awardEstimatedPrice'] if df_top1_contractS['awardEstimatedPrice'] is not None else None

    # Modifying awardPrice based on awardEstimatedPrice for contractU
    df_top1_contractU['awardPrice'] = df_top1_contractU['awardEstimatedPrice'] if df_top1_contractU['awardEstimatedPrice'] is not None else None

    cursor = conn.cursor()
    for _, row in df_top1_contractS.iterrows():
        cursor.execute("UPDATE Lots SET awardPrice = ? WHERE lotId = ?", (str(row['awardPrice']), row['lotId']))
    conn.commit()

    cursor = conn.cursor()
    for _, row in df_top1_contractU.iterrows():
        cursor.execute("UPDATE Lots SET awardPrice = ? WHERE lotId = ?", (str(row['awardPrice']), row['lotId']))
    conn.commit()

    print("Mise à jour effectuée avec succès.")


def convert_abnormal_awardDate(conn):
    df = create_df_from_query(
        conn,
        "SELECT lotId, tedCanId, awardDate FROM Lots WHERE CAST(strftime('%Y', awardDate) AS INTEGER) > 2020 GROUP BY strftime('%Y', awardDate)"
    )
    df['awardDate'] = pd.to_datetime(df['awardDate'])

    # Extraire les 4 premiers chiffres de tedCanId car c'est l'année de parution de l'offre
    df['yearFromId'] = (df['tedCanId'].astype(str).str[:4]).astype(int)

    # Remplacer dans awardDate
    df['awardDate'] = df.apply(lambda x: x['awardDate'].replace(year=int(x['yearFromId'])), axis=1)
    df = df.drop(columns=['yearFromId'])

    cursor = conn.cursor()
    for _, row in df.iterrows():
        cursor.execute("UPDATE Lots SET awardDate = ? WHERE lotId = ?", (str(row['awardDate']), row['lotId']))
    conn.commit()

    print("Mise à jour effectuée avec succès.")

def convert_null_accelerated(conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE Lots SET accelerated = 0 WHERE accelerated IS NULL")
    conn.commit()
    print("Les valeurs NULL ont été remplacées par 0 dans la colonne 'accelerated'.")

def convert_string_contractorSme(conn):
    cursor = conn.cursor()
    cursor.execute("UPDATE Lots SET contractorSme = NULL WHERE contractorSme NOT IN ('0', '1')")
    conn.commit()
    print("Mise à jour effectuée pour tous les contractorSme spécifiés.")

def replace_abnormal_numberTendersSme(conn):
    cursor = conn.cursor()
    cursor.execute("""UPDATE Lots SET numberTendersSme = numberTenders WHERE numberTendersSme > numberTenders""")
    conn.commit()
    print("Mise à jour effectuée pour tous les lotId spécifiés.")

def replace_abnormal_contractDuration(conn):
    cursor = conn.cursor()
    cursor.execute("""UPDATE Lots SET contractDuration = ROUND(contractDuration / 30.0, 2) WHERE contractDuration > 145 """)
    conn.commit()
    print("Mise à jour effectuée pour les contractDuration spécifiés.")