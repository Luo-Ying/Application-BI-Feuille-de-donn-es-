# Chemin du sqlite => "D:\Program Files\sqlite-tools-win-x64-3450100\sqlite3.exe"

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

    return rows


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


def get_all_data_not_null_of_columns(conn, tableName, lstColumnName):

    cur = conn.cursor()
    columns = ""
    for i in range(len(lstColumnName)):
        columns += f"{lstColumnName[i]}"
        if i < len(lstColumnName) - 1:
            columns += ","
    context_conditions = ""
    for i in range(len(lstColumnName)):
        context_conditions += f"{lstColumnName[i]} IS NOT null"
        if i < len(lstColumnName) - 1:
            context_conditions += " AND "
    cur.execute(
        f"SELECT {columns} FROM {tableName} WHERE {context_conditions} limit 100"
    )

    rows = cur.fetchall()

    return rows


def count_null_and_notNull_values_in_column(conn, tableName, columnName, varName):
    result = {}

    cur = conn.cursor()
    cur.execute(
        f"SELECT count({columnName}) as {columnName}_notNull, SUM(CASE WHEN {columnName} IS NULL then 1 else 0 end) as {columnName}_NullCount FROM {tableName}"
    )

    rows = cur.fetchall()

    result[f"{varName}_NotØ"] = rows[0][0]
    result[f"{varName}_Ø"] = rows[0][1]

    return result


def count_two_columns_NULL_vs_NOTNULL(conn, tableName, columns):
    result = {}

    cur = conn.cursor()

    cur.execute(
        f"SELECT count(*) FROM ( SELECT {columns[0]}, {columns[1]} FROM {tableName} WHERE {columns[0]} IS null and {columns[1]} IS NOT null ) as result"
    )
    # result[f"{columns[0]}_NULL {columns[1]}_NotNULL"] = cur.fetchall()[0][0]
    result[f"v1_Ø v2_NotØ"] = cur.fetchall()[0][0]

    cur.execute(
        f"SELECT count(*) FROM ( SELECT {columns[0]}, {columns[1]} FROM {tableName} WHERE {columns[0]} IS NOT null and {columns[1]} IS null ) as result"
    )
    # result[f"{columns[0]}_NotNULL {columns[1]}_NULL"] = cur.fetchall()[0][0]
    result[f"v1_NotØ v2_Ø"] = cur.fetchall()[0][0]

    cur.execute(
        f"SELECT count(*) FROM ( SELECT {columns[0]}, {columns[1]} FROM {tableName} WHERE {columns[0]} IS NOT null and {columns[1]} IS NOT null ) as result"
    )
    # result[f"{columns[0]}_NotNULL {columns[1]}_NotNULL"] = cur.fetchall()[0][0]
    result[f"v1_NotØ v2_NotØ"] = cur.fetchall()[0][0]

    return result


def count_two_columns_0_vs_Positives(conn, tableName, columns):
    result = {}

    cur = conn.cursor()

    cur.execute(
        f"SELECT count(*) FROM ( SELECT {columns[0]}, {columns[1]} FROM {tableName} WHERE {columns[0]} = 0 and {columns[1]} > 0 ) as result"
    )
    # result[f"{columns[0]}_NULL {columns[1]}_NotNULL"] = cur.fetchall()[0][0]
    result[f"v1_0 v2_+"] = cur.fetchall()[0][0]

    cur.execute(
        f"SELECT count(*) FROM ( SELECT {columns[0]}, {columns[1]} FROM {tableName} WHERE {columns[0]} > 0 and {columns[1]} = 0 ) as result"
    )
    # result[f"{columns[0]}_NotNULL {columns[1]}_NULL"] = cur.fetchall()[0][0]
    result[f"v1_+ v2_0"] = cur.fetchall()[0][0]

    cur.execute(
        f"SELECT count(*) FROM ( SELECT {columns[0]}, {columns[1]} FROM {tableName} WHERE {columns[0]} > 0 and {columns[1]} > 0 ) as result"
    )
    # result[f"{columns[0]}_NotNULL {columns[1]}_NotNULL"] = cur.fetchall()[0][0]
    result[f"v1_+ v2_+"] = cur.fetchall()[0][0]

    return result


def count_compare_two_columns_not_null(conn, tableName, columns):
    result = {}

    cur = conn.cursor()

    cur.execute(
        f"SELECT count(*) FROM ( SELECT {columns[0]}, {columns[1]} FROM {tableName} WHERE {columns[0]} > 0 AND {columns[1]} > 0 AND {columns[0]} > {columns[1]} ) as result"
    )
    # result[f"{columns[0]}_NULL {columns[1]}_NotNULL"] = cur.fetchall()[0][0]
    result[f"v1 sup. v2"] = cur.fetchall()[0][0]

    cur.execute(
        f"SELECT count(*) FROM ( SELECT {columns[0]}, {columns[1]} FROM {tableName} WHERE {columns[0]} > 0 AND {columns[1]} > 0 AND {columns[1]} > {columns[0]} ) as result"
    )
    # result[f"{columns[0]}_NULL {columns[1]}_NotNULL"] = cur.fetchall()[0][0]
    result[f"v2 sup. v1"] = cur.fetchall()[0][0]

    return result


def count_and_groupBY_2_columns(conn, tableName, columns):
    cur = conn.cursor()
    cur.execute(
        f"SELECT {columns[0]}, {columns[1]}, COUNT(*) as count From {tableName} GROUP BY {columns[0]}, {columns[1]} ORDER BY {columns[0]} ASC, {columns[1]} ASC;"
    )

    rows = cur.fetchall()

    return rows


def count_and_groupBY_2_columns_whitch_notNull(conn, tableName, columns):
    cur = conn.cursor()
    cur.execute(
        f"SELECT {columns[0]}, {columns[1]} From {tableName} WHERE {columns[0]} IS NOT null and {columns[1]} IS NOT null ORDER BY {columns[0]} ASC;"
    )

    rows = cur.fetchall()

    return rows
