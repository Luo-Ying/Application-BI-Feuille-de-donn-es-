# Chemin du sqlite => D:\Program Files\sqlite-tools-win-x64-3450100\sqlite3.exe

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


def count_null_and_notNull_values_in_column(conn, tableName, columnName):
    cur = conn.cursor()
    cur.execute(
        f"SELECT count({columnName}) as {columnName}_notNull, SUM(CASE WHEN {columnName} IS NULL then 1 else 0 end) as {columnName}_NullCount FROM {tableName}"
    )

    rows = cur.fetchall()

    # print(rows)

    for row in rows:
        print(row)


def count_and_groupBY_2_columns(conn, tableName, columns):
    cur = conn.cursor()
    cur.execute(
        f"SELECT {columns[0]}, {columns[1]}, COUNT(*) as count From {tableName} GROUP BY {columns[0]}, {columns[1]} ORDER BY {columns[0]} ASC, {columns[1]} ASC;"
    )

    rows = cur.fetchall()

    return rows
