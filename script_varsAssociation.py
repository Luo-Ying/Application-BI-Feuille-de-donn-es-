from scriptReadSql import *
from scriptGraphics.drawHist import draw_hist


def communication_beteewn_Agents(conn):
    df_Buyers = create_df_from_query(
        conn,
        "SELECT lotId, agentId as idBuyer FROM LotBuyers",
    )
    df_Suppliers = create_df_from_query(
        conn,
        "SELECT lotId, agentId as idSupplier FROM LotSuppliers",
    )
    df_Agents = create_df_from_query(
        conn,
        "SELECT * FROM Agents",
    )

    df_Lots = create_df_from_query(
        conn,
        "SELECT * FROM Lots",
    )

    merged_df = pd.merge(df_Buyers, df_Suppliers, on="lotId")

    merged_df_buyer_lot = pd.merge(
        df_Buyers, df_Lots[["lotId", "awardPrice"]], on="lotId"
    )
    merged_df_buyer_dep = pd.merge(
        merged_df_buyer_lot,
        df_Agents[["agentId", "department"]],
        left_on="idBuyer",
        right_on="agentId",
    )
    merged_df_supplier_dep = pd.merge(
        df_Suppliers, df_Lots[["lotId", "awardPrice"]], on="lotId"
    )
    merged_df_supplier_dep = pd.merge(
        merged_df_supplier_dep,
        df_Agents[["agentId", "department"]],
        left_on="idSupplier",
        right_on="agentId",
    )

    merged_df_buyer_dep.drop(
        columns=["agentId"],
        inplace=True,
    )
    merged_df_supplier_dep.drop(
        columns=["agentId"],
        inplace=True,
    )

    merged_df_buyer_dep = (
        merged_df_buyer_dep.groupby("department")["awardPrice"].sum().reset_index()
    )
    merged_df_buyer_dep = merged_df_buyer_dep.rename(
        columns={"awardPrice": "totalAwardPriceBuyer"}
    )

    merged_df_supplier_dep = (
        merged_df_supplier_dep.groupby("department")["awardPrice"].sum().reset_index()
    )
    merged_df_supplier_dep = merged_df_supplier_dep.rename(
        columns={"awardPrice": "totalAwardPriceSupplier"}
    )

    merged_df_buyer_dep = merged_df_buyer_dep.sort_values(
        by="totalAwardPriceBuyer", ascending=False
    ).reset_index(drop=True)
    merged_df_supplier_dep = merged_df_supplier_dep.sort_values(
        by="totalAwardPriceSupplier", ascending=False
    ).reset_index(drop=True)

    # Merge the first dataframe with the second dataframe on 'idBuyer' to get corresponding 'siret' for 'idBuyer'
    merged_df_buyer = pd.merge(
        merged_df,
        df_Agents[["agentId", "siret"]],
        left_on="idBuyer",
        right_on="agentId",
    )

    # Merge the first dataframe with the second dataframe on 'idSupplier' to get corresponding 'siret' for 'idSupplier'
    merged_df_supplier_buyer = pd.merge(
        merged_df_buyer,
        df_Agents[
            [
                "agentId",
                "siret",
            ]
        ],
        left_on="idSupplier",
        right_on="agentId",
        suffixes=("_buyer", "_supplier"),
    )

    # Extract the first 9 digits of 'siret' columns and replace 'idBuyer' and 'idSupplier'
    merged_df_supplier_buyer["idBuyer"] = merged_df_supplier_buyer["siret_buyer"].str[
        :9
    ]
    merged_df_supplier_buyer["idSupplier"] = merged_df_supplier_buyer[
        "siret_supplier"
    ].str[:9]

    merged_df_Lot_comm = pd.merge(
        merged_df_supplier_buyer, df_Lots[["lotId", "awardPrice"]], on="lotId"
    )

    # Drop unnecessary columns
    merged_df_Lot_comm.drop(
        columns=["agentId_buyer", "siret_buyer", "agentId_supplier", "siret_supplier"],
        inplace=True,
    )

    # Count occurrences of idBuyer
    buyer_counts = merged_df_Lot_comm["idBuyer"].value_counts().reset_index()
    buyer_counts.columns = ["idBuyer", "Buyer_Count"]

    # Count occurrences of idSupplier
    supplier_counts = merged_df_Lot_comm["idSupplier"].value_counts().reset_index()
    supplier_counts.columns = ["idSupplier", "Supplier_Count"]

    # Count occurrences of pairs of idBuyer and idSupplier
    pair_counts = (
        merged_df_Lot_comm.groupby(["idBuyer", "idSupplier"])
        .size()
        .reset_index(name="Pair_Count")
    )
    pair_counts = pair_counts.sort_values(by="Pair_Count", ascending=False)

    pair_counts["id_BuyerAndSupplier"] = (
        pair_counts["idBuyer"].astype(str) + "_" + pair_counts["idSupplier"].astype(str)
    )

    buyer_total = (
        merged_df_Lot_comm.groupby("idBuyer")["awardPrice"].sum().reset_index()
    )
    buyer_total = buyer_total.rename(columns={"awardPrice": "totalAwardPriceBuyer"})

    supplier_total = (
        merged_df_Lot_comm.groupby("idSupplier")["awardPrice"].sum().reset_index()
    )
    supplier_total = supplier_total.rename(
        columns={"awardPrice": "totalAwardPriceSupplier"}
    )

    buyer_total = buyer_total.sort_values(
        by="totalAwardPriceBuyer", ascending=False
    ).reset_index(drop=True)
    supplier_total = supplier_total.sort_values(
        by="totalAwardPriceSupplier", ascending=False
    ).reset_index(drop=True)

    # print("Buyer Total Paid Price:")
    # print(buyer_total)

    # print("\nSupplier Total Award Price:")
    # print(supplier_total)

    draw_hist_top_50_Buyers_communication(buyer_counts.head(50))
    draw_hist_top_50_Suppliers_communication(supplier_counts.head(50))
    draw_hist_top_50_Buyers_and_Suppliers_communication_paire(pair_counts.head(50))
    draw_hist_top_50_Buyers_paid(buyer_total.head(50))
    draw_hist_top_50_Sppliers_awrd(supplier_total.head(50))
    draw_hist_top_50_Buyers_departement(merged_df_buyer_dep.head(50))
    draw_hist_top_50_Suppliers_departement(merged_df_supplier_dep.head(50))


def draw_hist_top_50_Buyers_departement(data):
    draw_hist(
        data,
        "department",
        "totalAwardPriceBuyer",
        "Top 50 des département avec le plus de flux d'agent sortant",
        "Flux",
        True,
    )


def draw_hist_top_50_Suppliers_departement(data):
    draw_hist(
        data,
        "department",
        "totalAwardPriceSupplier",
        "Top 50 des département avec le plus de flux d'agent entrant",
        "Flux",
        True,
    )


def draw_hist_top_50_Buyers_communication(data):
    draw_hist(
        data,
        "idBuyer",
        "Buyer_Count",
        "Top 50 des acheteurs qui communiquent le plus",
        "Flux",
    )


def draw_hist_top_50_Suppliers_communication(data):
    draw_hist(
        data,
        "idSupplier",
        "Supplier_Count",
        "Top 50 des fournisseurs qui communiquent le plus",
        "Flux",
    )


def draw_hist_top_50_Buyers_and_Suppliers_communication_paire(data):
    draw_hist(
        data,
        "id_BuyerAndSupplier",
        "Pair_Count",
        "Top 50 des acheteurs et des fournisseurs qui communiquent entre eux le plus",
        "Flux",
    )


def draw_hist_top_50_Buyers_paid(data):
    draw_hist(
        data,
        "idBuyer",
        "totalAwardPriceBuyer",
        "Top 50 des acheteurs avec le plus de flux d'agent sortant",
        "Flux",
        True,
    )


def draw_hist_top_50_Sppliers_awrd(data):
    draw_hist(
        data,
        "idSupplier",
        "totalAwardPriceSupplier",
        "Top 50 des fournisseurs avec le plus de flux d'agent entrant",
        "Flux",
        True,
    )