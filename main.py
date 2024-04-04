from scriptReadSql import *
from scriptGraphics.drawHist import *
from scriptGraphics.drawBoxPlot import *
from script_single import *
from script_calcule_correlation_paires import *
from script_single import script_single
from script_pair import script_pair
from script_clean_variables_manually import *


def main():
    # database = "Input\\Foppa.db"
    # # database = r"D:\Yingqi\etude\m2-yingqi\Application BI\Foppa.db"
    database = r"E:\Yingqi\etudes\m2\Application BI\Foppa.db"
    database = r"C:\Users\devef\Documents\Application BI\FOPPA\sqlite-tools-win-x64-3450100\Foppa.db"

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
        # create_csv_from_database()
        # calcule_correlation_Lots(conn)
        # script_pair(conn)
        script_clean_variables_manually(conn)

    close_db(conn)


if __name__ == "__main__":
    main()
