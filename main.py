from scriptReadSql import *
from scriptGraphics.drawHist import *
from scriptGraphics.drawBoxPlot import *


def draw_outOfDirectives_publicityDuration(conn):
    rows = count_and_groupBY_2_columns(
        conn, "Lots", ["outOfDirectives", "publicityDuration"]
    )
    data_outOfDirectives_0 = {}
    lstdata_outOfDirectives_0 = []
    data_outOfDirectives_1 = {}
    lstdata_outOfDirectives_1 = []
    for row in rows:
        # print(row[0])
        if row[0] == 0:
            # print(row[0])
            data_outOfDirectives_0[str(row[1])] = row[2]
            if row[1] != None:
                lstdata_outOfDirectives_0.append(row[1])
            # lstdata_outOfDirectives_0.append(row[1])
        elif row[0] == 1:
            data_outOfDirectives_1[str(row[1])] = row[2]
            if row[1] != None:
                lstdata_outOfDirectives_1.append(row[1])
            # lstdata_outOfDirectives_1.append(row[1])

    print("Les résultat pour quand outOfDirectives est à 0 : ")
    print(data_outOfDirectives_0)

    print("\nLes résultat pour quand outOfDirectives est à 1 : ")
    print(data_outOfDirectives_1)

    # draw_hist_without_log(
    #     data_outOfDirectives_0,
    #     "publicityDuration",
    #     "nombre d'appaîtion",
    #     "outOfDirectives is 0 without log",
    # )
    # draw_hist_without_log(
    #     data_outOfDirectives_1,
    #     "publicityDuration",
    #     "nombre d'appaîtion",
    #     "outOfDirectives is 1 without log",
    # )

    # draw_hist_with_log(
    #     data_outOfDirectives_0,
    #     "publicityDuration",
    #     "nombre d'appaîtion",
    #     "outOfDirectives is 0 with log",
    # )
    # draw_hist_with_log(
    #     data_outOfDirectives_1,
    #     "publicityDuration",
    #     "nombre d'appaîtion",
    #     "outOfDirectives is 1 with log",
    # )

    draw_box_plot_without_log(lstdata_outOfDirectives_0, "0", "outOfDirectives est à 0")
    draw_box_plot_without_log(lstdata_outOfDirectives_1, "1", "outOfDirectives est à 1")


def main():
    database = r"D:\Yingqi\etude\m2-yingqi\Application BI\Foppa.db"

    # create a database connection
    conn = create_connection(database)
    with conn:

        # print("1. Query all Agents Names")
        # select_all_from_table(conn, "Names")

        # print("2. Query columns from table")
        # select_column_from_table(conn, "Lots", ["contractorSme", "numberTendersSme"])

        draw_outOfDirectives_publicityDuration(conn)


if __name__ == "__main__":
    main()
