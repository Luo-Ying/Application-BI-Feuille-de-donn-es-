import matplotlib.pyplot as plt

from scriptGraphics.generateFileChart import generateFileChart


def get_top_multiple(data, column1, column2, N, nom_fichier):
    agents_count_per_city = data.groupby(column1)[column2].nunique()

    top_10_cities = agents_count_per_city.sort_values(ascending=True).head(N)
    top_10_cities = top_10_cities.sort_values(ascending=False)
    bars = plt.bar(top_10_cities.index, top_10_cities.values, color='skyblue', edgecolor='black')

    plt.title(f'Top {N} des {column1} par {column2}')
    plt.xlabel(column1)
    plt.ylabel(column2)
    plt.xticks(rotation=45)  # Rotation des étiquettes pour une meilleure lisibilité

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, yval + 0.5, yval, ha='center', va='bottom')

    plt.tight_layout()  # Ajuste automatiquement les sous-plots pour qu'ils tiennent dans la figure

    # generateFileChart(nom_fichier, columns, f"top {N}")
    generateFileChart(nom_fichier, f'{column1}_{column2}', f"worst {N}")
    plt.show()


def get_top(data, column, N, nom_fichier, reversed=True):
    # data[column] = pd.to_numeric(data[column], errors='coerce')

    if data[column].dtype in ['object', 'Int64']:
        # Count occurrences of each term
        counts = data[column].value_counts().nlargest(N)
        x = counts.index.astype(str).tolist()  # Term names
        y = counts.values.tolist()  # Occurrences
    else:
        table = data.nlargest(n=N, columns=[column])
        x = ["Candidat " + str(n) for n in range(N, 0, -1)]
        # getting values against each value of y
        y = table[column].to_list()

    if reversed:
        x.reverse()
        y.reverse()
    print(x)

    # plt.xscale("log")
    plt.barh(x, y)

    for index, value in enumerate(y):
        plt.text(value, index, str(value))

    if data[column].dtype == 'object':
        print('')
    else:
        index_labels = ["Candidat " + str(n) for n in range(1, N + 1)]
        table = pd.DataFrame(data=table.values, index=index_labels, columns=data.head)
        print(table)

    generateFileChart(nom_fichier, column, "top")
    plt.show()