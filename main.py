from scriptReadSql import *
from scriptGraphics.drawHist import *
from scriptGraphics.drawBoxPlot import *
from script_single import *
from script_single import script_single
from script_pair import script_pair


def main():
    # database = "Input\\Foppa.db"
    database = r"D:\Yingqi\etude\m2-yingqi\Application BI\Foppa.db"
    # database = r"C:\Users\devef\Documents\Application BI\FOPPA\sqlite-tools-win-x64-3450100\Foppa.db"

    conn = create_connection(database)
    with conn:
        # draw_numberTenders_numberTenderSme(conn)

        ##################################################
        ############# Attribut Individuel ################
        ##################################################
        # script_single(conn)

        ##################################################
        # ############ Attribut En Paire #################
        ##################################################
        script_pair(conn)

    close_db(conn)


if __name__ == "__main__":
    main()
