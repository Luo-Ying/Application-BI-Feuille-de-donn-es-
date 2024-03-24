from scriptReadSql import *


def main():
    database = r"D:\Yingqi\etude\m2-yingqi\Application BI\Foppa.db"

    # create a database connection
    conn = create_connection(database)
    with conn:

        # print("1. Query all Agents Names")
        # select_all_from_table(conn, "Names")

        print("2. Query columns from table")
        select_column_from_table(conn, "Lots", ["contractorSme", "numberTendersSme"])


if __name__ == "__main__":
    main()
