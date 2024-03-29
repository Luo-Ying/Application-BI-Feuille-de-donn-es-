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
