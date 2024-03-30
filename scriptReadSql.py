# Chemin du sqlite => "D:\Program Files\sqlite-tools-win-x64-3450100\sqlite3.exe"

import sqlite3
from sqlite3 import Error
import pandas as pd


def create_connection(db_file):
    """create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


"""
les requêtes pour 'cancelled'
"""


def select_cancelled_count_diff_elements(conn):
    cur = conn.cursor()
    cur.execute("SELECT cancelled, COUNT(*) AS count FROM Lots GROUP BY cancelled")

    rows = cur.fetchall()

    return rows


"""
les requêtes pour 'awardDate'
"""


def select_awardDate_get_date_appearances(conn):
    cur = conn.cursor()
    cur.execute(
        "SELECT strftime('%Y', awardDate) AS date, awardDate, COUNT(*) AS count FROM Lots WHERE awardDate IS NOT null GROUP BY date, awardDate ORDER BY date, awardDate;"
    )

    rows = cur.fetchall()

    return rows


def close_db(connexion):
    connexion.close()


def create_df_from_query(connexion, query):
    return pd.read_sql_query(query, connexion)
