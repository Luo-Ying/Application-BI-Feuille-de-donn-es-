import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib import colors
from scriptGraphics.generateFileChart import generateFileChart


def load_map_france_departement(data, dataColName, color, title):
    data = data.rename(columns={"department": "code_insee", f"{dataColName}": "data"})

    # Load the world shapefile
    france = gpd.read_file("./References/departements-20180101.shp")

    # Merge the France shapefile with the data
    france["data"] = 0
    france = france.merge(
        data, on="code_insee", how="left", suffixes=("_original", "_new")
    )
    france["data"] = france["data_new"].fillna(france["data_original"])

    # List of DOM-TOM department codes
    dom_tom_codes = ["971", "972", "973", "974", "976"]  # Adjust as needed

    # Filter out DOM-TOM departments
    france_mainland = france[~france["code_insee"].isin(dom_tom_codes)]

    # Plot the map
    fig, ax = plt.subplots(1, 1)
    min_non_zero = france_mainland[france_mainland["data"] != 0]["data"].min()
    france_mainland.plot(
        column="data",
        cmap=color,
        linewidth=0.8,
        ax=ax,
        edgecolor="0.8",
        legend=True,
        norm=LogNorm(vmin=min_non_zero, vmax=france_mainland["data"].max()),
    )

    for idx, row in france_mainland.iterrows():
        ax.text(
            row.geometry.centroid.x,
            row.geometry.centroid.y,
            row["code_insee"],
            fontsize=8,
            ha="center",
        )

    # Add title and show
    plt.title(title)
    # plt.show()

    generateFileChart("Flux", title, "hist_pivot")
