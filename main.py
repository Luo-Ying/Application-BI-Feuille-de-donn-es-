from scriptReadSql import *
from scriptGraphics.drawHist import *
from scriptGraphics.drawBoxPlot import *
from scriptIndividual import *
from scripts_individuel import scripts_individuel
from scripts_paires import scripts_paires


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

    draw_box_plot(lstdata_outOfDirectives_0, "0", "", "outOfDirectives est à 0")
    draw_box_plot(lstdata_outOfDirectives_1, "1", "", "outOfDirectives est à 1")


def draw_numberTenders_numberTenderSme(conn):
    data_for_hist = {}

    rows = ["numberTenders", "numberTendersSme"]

    data_numberTenders = count_null_and_notNull_values_in_column(
        conn, "Lots", "numberTenders", "v1"
    )

    data_numberTendersSme = count_null_and_notNull_values_in_column(
        conn, "Lots", "numberTendersSme", "v2"
    )

    data_numberTenders_compare_numberTendersSme_null = (
        count_two_columns_NULL_vs_NOTNULL(conn, "Lots", rows)
    )

    data_numberTenders_compare_numberTendersSme_0 = count_two_columns_0_vs_Positives(
        conn, "Lots", rows
    )
    data_numberTenders_compare_numberTendersSme_sup = (
        count_compare_two_columns_not_null(conn, "Lots", rows)
    )

    data_for_hist = dict(data_numberTenders)
    data_for_hist.update(data_numberTendersSme)
    data_for_hist.update(data_numberTenders_compare_numberTendersSme_null)
    data_for_hist.update(data_numberTenders_compare_numberTendersSme_0)
    data_for_hist.update(data_numberTenders_compare_numberTendersSme_sup)
    annotation_text = (
        f"v1: {rows[0]}\n v2: {rows[1]}\n Ø: NULL\n +: Positive (supérieur à 0)"
    )

    print(data_for_hist)
    draw_hist(
        data_for_hist,
        "",
        "nombre d'appaîtion",
        "numberTenders et numberTendedrSme",
        False,
        45,
        None,
        annotation_text,
    )

    rows_groupBy = count_and_groupBY_2_columns_whitch_notNull(conn, "Lots", rows)

    data_for_boxplot = {}

    for row in rows_groupBy:
        if str(row[0]) not in data_for_boxplot:
            data_for_boxplot[str(row[0])] = []
        data_for_boxplot[str(row[0])].append(row[1])

    # print(data_for_boxplot)
    draw_multiple_box_plot(
        data_for_boxplot,
        "Distribution de Tenders (Sme dans totale)",
        "Categories (numberTenders)",
        "numberTendersSme",
    )


def main():
    database = r"D:\Yingqi\etude\m2-yingqi\Application BI\Foppa.db"

    conn = create_connection(database)
    with conn:
        # draw_outOfDirectives_publicityDuration(conn)
        # draw_numberTenders_numberTenderSme(conn)

        ##################################################
        # AttributIndividuel
        ##################################################
        """correctionsNb"""
        # draw_correctionsNb(conn)
        """cancelled"""
        # draw_cancelled(conn)
        """awardDate"""
        draw_awardDate(conn)
        """awardEstimatedPrice"""
        # draw_awardEstimatedPrice(conn)
        scripts_individuel(conn)
        scripts_paires(conn)
        close_db(conn)


if __name__ == "__main__":
    main()
