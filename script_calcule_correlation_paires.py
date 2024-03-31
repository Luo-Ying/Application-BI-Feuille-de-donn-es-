import pandas as pd
from scriptReadSql import *


def calcule_correlation(data):
    df = pd.DataFrame(data=data)
    print("Data Frame")
    print(df)
    print()

    print("Correlation Matrix")
    print(df.corr())
    print()

    def get_redundant_pairs(df):
        """Get diagonal and lower triangular pairs of correlation matrix"""
        pairs_to_drop = set()
        cols = df.columns
        for i in range(0, df.shape[1]):
            for j in range(0, i + 1):
                pairs_to_drop.add((cols[i], cols[j]))
        return pairs_to_drop

    def get_top_abs_correlations(df, n=5):
        au_corr = df.corr().abs().unstack()
        labels_to_drop = get_redundant_pairs(df)
        au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
        return au_corr[0:n]

    print("Top Absolute Correlations")
    print(get_top_abs_correlations(df, 3))


def calcule_correlation_Lots(conn):
    df = create_df_from_query(
        conn,
        "SELECT * FROM Lots",
    )
    df["awardDate"] = pd.to_datetime(df["awardDate"])
    df["awardDate"] = pd.to_numeric(df["awardDate"])
    df = pd.get_dummies(df, columns=["fraEstimated"], drop_first=True)
    df["lotsNumber"] = pd.to_numeric(df["lotsNumber"], errors="coerce")
    df = pd.get_dummies(df, columns=["contractorSme"], drop_first=True)
    df = pd.get_dummies(df, columns=["typeOfContract"], drop_first=True)
    df = pd.get_dummies(df, columns=["topType"], drop_first=True)
    calcule_correlation(df)
