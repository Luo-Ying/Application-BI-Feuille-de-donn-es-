from scriptReadSql import *
from scriptGraphics.drawHist import *
from scriptGraphics.drawBoxPlot import *


def draw_correctionsNb(conn):

    rows = select_column_from_table(conn, "Lots", ["correctionsNb"])
    data = []

    for row in rows:
        data.append(row[0])

    draw_box_plot(data, "", "valeurs", "correctionsNb")


def draw_cancelled(conn):

    rows = select_cancelled_count_diff_elements(conn)
    data_count_elements = {}

    for row in rows:
        data_count_elements[str(row[0])] = row[1]

    draw_hist(
        data_count_elements, "Les éléments", "nombre d'appaîtion", "cancelled", True
    )


def draw_awardDate(conn):
    rows = select_awardDate_get_date_appearances(conn)

    data_date_appearances_by_each_year = {}
    data_date_appearances_by_each_decade = {}

    for row in rows:
        data_date_appearances_by_each_year[row[0]] = (
            row[2]
            if str(row[0]) not in data_date_appearances_by_each_year
            else data_date_appearances_by_each_year[row[0]] + row[2]
        )

    print(data_date_appearances_by_each_year)

    year_start = 0
    year_end = 0
    appearances = 0
    keys = list(data_date_appearances_by_each_year.keys())
    length = len(keys)
    for index, key in enumerate(keys):
        value = data_date_appearances_by_each_year[key]
        year_end = int(key)
        if year_start == 0:
            year_start = int(key)
        appearances += value
        if year_end - year_start >= 19 or index == length - 1:
            data_date_appearances_by_each_decade[f"{year_start}-{year_end}"] = (
                appearances
            )
            appearances = 0
            year_start = year_end
            year_end = 0

    print(data_date_appearances_by_each_decade)
    draw_hist(
        data_date_appearances_by_each_decade,
        "Chaque 20 ans",
        "Nombre d'appaîtion",
        "awardDate",
        False,
    )
