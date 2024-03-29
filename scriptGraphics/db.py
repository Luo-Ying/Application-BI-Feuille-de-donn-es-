import sqlite3
import pandas as pd


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
