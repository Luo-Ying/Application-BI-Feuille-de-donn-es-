from bs4 import BeautifulSoup
from getTedXML import *
from scriptReadSql import *

"""
"""
def correctedData(conn):
    tedCanId = "2012208072"
    df = create_df_from_query(
        conn,
        f"SELECT * FROM Lots WHERE tedCanId IN ({tedCanId})",
    )
    print(df)
    ted = transform(tedCanId)
    # createXML(ted)
    fileXML = openXML(ted)
    # test(fileXML)