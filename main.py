from scriptReadSql import *
from scriptGraphics.drawHist import *
from scriptGraphics.drawBoxPlot import *
from script_single import *
from scripts_paires import scripts_paires
from script_single import script_single


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
        # draw_numberTenders_numberTenderSme(conn)

        ##################################################
        # AttributIndividuel
        ##################################################
        script_single(conn)
        # draw_awardDate(conn)

    close_db(conn)


if __name__ == "__main__":
    main()
