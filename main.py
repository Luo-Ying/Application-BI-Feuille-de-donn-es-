from script_clean_variables_api_tedeuropa import *
from script_cpv_par_domaine import *
from script_calcule_correlation_paires import *
from script_single import script_single
from script_pair import script_pair
from script_clean_variables_manually import *
from script_varsAssociation import *
import sys


def main(argv, arc):
    database = argv[1]

    conn = create_connection(database)
    with conn:
        """Code main"""
        # calcule_correlation_Lots(conn, "before_clean")

        ##################################################
        ############# Attribut Individuel ################
        ##################################################
        # script_single(conn, False)

        ##################################################
        ############# Attribut En Paire #################
        ##################################################
        # script_pair(conn, False)

        ##################################################
        ########### Correction des données ###############
        ##################################################
        # correctedData(conn)
        # script_clean_variables_manually(conn)

        ##################################################
        ############# Attribut Individuel ################
        ##################################################
        # script_single(conn, True)

        ##################################################
        ############# Attribut En Paire #################
        ##################################################
        # script_pair(conn, True)

        calcule_correlation_Lots(conn, "after_cleaned")

        ##################################################
        ############## Questionnements ##################
        ##################################################
        # top50(conn)
        # script_cpv(conn)
    close_db(conn)


if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
