import matplotlib.pyplot as plt
import pandas as pd

from scriptGraphics.generateFileChart import *
from scriptReadSql import *


def script_cpv(conn):
    script_cpv_flux(conn, 2, 10)
    script_cpv_flux(conn, 3, 50)
    script_cpv_maxAwardPrice_Buyers(conn, 2, 10)
    script_cpv_maxAwardPrice_Buyers(conn, 3, 50)
    script_cpv_maxAwardPrice_Suppliers(conn, 2, 10)
    script_cpv_maxAwardPrice_Suppliers(conn, 3, 50)
    script_cpv_par_domain(conn)


def script_cpv_maxAwardPrice_Buyers(conn, cpv_max_nb, top_max_nb):
    df = create_df_from_query(
        conn,
        f"""
            SELECT SUBSTR(L.cpv, 1, {cpv_max_nb}) as cpv_group, SUM(L.awardPrice) as somme
            FROM Lots L
            JOIN LotBuyers LB ON L.lotId = LB.lotId
            GROUP BY cpv_group
            ORDER BY somme DESC
            LIMIT {top_max_nb}
        """,
    )

    top_cpvs_df = df.sort_values(by="somme", ascending=False).head(top_max_nb)

    plt.figure(figsize=(12, 7))
    bars = plt.bar(top_cpvs_df["cpv_group"], top_cpvs_df["somme"], color="skyblue")

    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            int(yval),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.xlabel("CPVs")
    plt.ylabel("Total des ventes")
    plt.yscale("log")
    plt.title(f"Top {top_max_nb} CPV pour les acheteurs qui génèrent le plus d'argent")
    plt.xticks(rotation=45)

    plt.tight_layout()
    generateFileChart(
        "Fusion",
        f"Top {top_max_nb} CPV pour les acheteurs qui génèrent le plus d'argent",
        "hist_with_log",
    )


def script_cpv_maxAwardPrice_Suppliers(conn, cpv_max_nb, top_max_nb):
    df = create_df_from_query(
        conn,
        f"""
            SELECT SUBSTR(L.cpv, 1, {cpv_max_nb}) as cpv_group, SUM(L.awardPrice) as somme
            FROM Lots L
            JOIN LotSuppliers LS ON L.lotId = LS.lotId
            GROUP BY cpv_group
            ORDER BY somme DESC
            LIMIT {top_max_nb}
        """,
    )

    top_cpvs_df = df.sort_values(by="somme", ascending=False).head(top_max_nb)

    plt.figure(figsize=(12, 7))
    bars = plt.bar(top_cpvs_df["cpv_group"], top_cpvs_df["somme"], color="skyblue")

    for bar in bars:
        yval = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            yval,
            int(yval),
            ha="center",
            va="bottom",
            fontsize=8,
        )

    plt.xlabel("CPVs")
    plt.ylabel("Total des gains")
    plt.yscale("log")
    plt.title(
        f"Top {top_max_nb} CPV pour les fournisseurs qui gagnent le plus d'argent"
    )
    plt.xticks(rotation=45)

    plt.tight_layout()  # Adjust the layout to prevent clipping of tick-labels
    generateFileChart(
        "Fusion",
        f"Top {top_max_nb} CPV pour les acheteurs qui génèrent le plus d'argent",
        "hist_with_log",
    )


def script_cpv_flux(conn, cpv_max_nb, top_max_nb):
    buyers_df = create_df_from_query(
        conn,
        f"""
                SELECT SUBSTR(L.cpv, 1, {cpv_max_nb}) as cpv_group, COUNT(*) as buyers_count
                FROM Lots L
                JOIN LotBuyers LB ON L.lotId = LB.lotId
                GROUP BY cpv_group
                """,
    )

    suppliers_df = create_df_from_query(
        conn,
        f"""
            SELECT SUBSTR(L.cpv, 1, {cpv_max_nb}) as cpv_group, COUNT(*) as suppliers_count
            FROM Lots L
            JOIN LotSuppliers LS ON L.lotId = LS.lotId
            GROUP BY cpv_group
        """,
    )

    merged_df = pd.merge(buyers_df, suppliers_df, on="cpv_group")
    merged_df["combined_count"] = (
        merged_df["buyers_count"] + merged_df["suppliers_count"]
    )
    top_cpvs_df = merged_df.nlargest(top_max_nb, "combined_count")

    plt.figure(figsize=(10, 6))
    plt.bar(top_cpvs_df["cpv_group"], top_cpvs_df["combined_count"], color="skyblue")

    for idx, value in enumerate(top_cpvs_df["combined_count"]):
        plt.text(idx, value, str(value), ha="center", va="bottom", fontsize=8)

    plt.xlabel("CPV")
    plt.ylabel("Nombre d'apparition")
    plt.title(f"Top {top_max_nb} des CPVs ayant le plus de flux")
    plt.xticks(range(len(top_cpvs_df)), top_cpvs_df["cpv_group"])

    # Show the plot
    plt.tight_layout()
    generateFileChart("Fusion", f"Top {top_max_nb} CPV flux", "hist")


def script_cpv_par_domain(conn):
    script_cpv_domain(conn, "S")
    script_cpv_domain(conn, "U")
    script_cpv_domain(conn, "W")


def script_cpv_domain(conn, typeContract):
    df_top_departments = create_df_from_query(
        conn,
        "SELECT distinct department, count(department) as nombre_agents FROM Agents WHERE department IS NOT null GROUP BY department ORDER BY nombre_agents DESC LIMIT 5",
    )
    top_cpvs_query = create_df_from_query(
        conn,
        "SELECT SUBSTR(L.cpv, 1, 2) as cpv_group, SUM(L.awardPrice) as total_award_price, department FROM Lots L JOIN LotSuppliers LS ON L.lotId = LS.lotId JOIN Agents A ON LS.agentId = A.agentId WHERE typeOfContract='"
        + typeContract
        + "' AND A.department IN ({}) GROUP BY cpv_group ORDER BY total_award_price DESC LIMIT 10".format(
            ",".join(f"'{d}'" for d in df_top_departments["department"])
        ),
    )
    pivot_df = top_cpvs_query.pivot(
        index="department", columns="cpv_group", values="total_award_price"
    )

    # Plotting the histogram
    # pivot_df.plot(kind='bar', stacked=False, figsize=(10, 7))
    ax = pivot_df.plot(kind="bar", stacked=False, figsize=(10, 7), logy=True)
    plt.title(
        "Top 10 des CPV qui génèrent le plus d'argent pour les 10 département ayant le plus d'agents pour le type de contrat 'S'"
    )
    # plt.yscale("log")
    plt.xticks(rotation=45)

    plt.xlabel("Department")
    plt.ylabel("Total Award Price")
    plt.legend(title="CPV Group")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f", label_type="edge", padding=3)
    plt.tight_layout()
    generateFileChart(
        "Fusion",
        f"Top 10 des CPV TOP 10 les département pour le contrat {typeContract}",
        "hist",
    )
