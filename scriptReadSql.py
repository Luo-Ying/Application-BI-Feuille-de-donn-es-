import sqlite3
from sqlite3 import Error


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


def select_all_from_table(conn, tableName):
    """
    Query all rows in the tableName table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {tableName}")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_column_from_table(conn, tableName, lstColumnName):
    """
    Query all rows in the tableName table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    columns = ""
    for i in range(len(lstColumnName)):
        columns += f"{lstColumnName[i]}"
        if i < len(lstColumnName) - 1:
            columns += ","
    cur.execute(f"SELECT {columns} FROM {tableName}")

    rows = cur.fetchall()

    for row in rows:
        print(row)
