import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import os
import math
import pygal
import lxml

DTYPE_DICT_LOTS = {
    "lotId": "Int64",
    "tedCanId": "Int64",
    "correctionsNb": "Int64",
    "cancelled": "Int64",
    "awardDate": "object",
    "awardEstimatedPrice": "Float64",
    "awardPrice": "Float64",
    "cpv": "Int64",
    "numberTenders": "Int64",
    "onBehalf": "object",
    "jointProcurement": "object",
    "fraAgreement": "object",
    "fraEstimated": "object",
    "lotsNumber": "object",
    "accelerated": "object",
    "outOfDirectives": "Int64",
    "contractorSme": "object",
    "numberTendersSme": "Float64",
    "subContracted": "object",
    "gpa": "object",
    "multipleCae": "object",
    "typeOfContract": "object",
    "topType": "object",
    "renewal": "object",
    "contractDuration": "Float64",
    "publicityDuration": "Float64",
}

def read_csv(input_csv_path):
    pathLots = input_csv_path + "\\Lots.csv"
    pathNames = input_csv_path + "\\Names.csv"
    pathriteria = input_csv_path + "\\Criteria.csv"
    pathAgents = input_csv_path + "\\Agents.csv"
    pathLotBuyers = input_csv_path + "\\LotBuyers.csv"
    pathLotSuppliers = input_csv_path + "\\LotSuppliers.csv"

    if not os.path.exists(pathLots):
            raise FileNotFoundError(f"Le fichier spécifié n'a pas été trouvé : {pathLots}")
    else:
        csv = "lots"
        if not os.path.exists(sys.path[0] + f'\\fig\\Lots_Pair_Variable'):
            os.makedirs(sys.path[0] + f'\\fig\\Lots_Pair_Variable')
        df_lots = pd.read_csv(pathLots, dtype=DTYPE_DICT_LOTS, sep=",")
        draw_Diagram(df_lots, DTYPE_DICT_LOTS,csv)


def draw_Diagram(df, dtype,csv):
    match csv:
        case "lots":
            # draw_Award_date_Award_price(df, dtype)
            # draw_Award_price_Award_estimated_Price(df, dtype)
            draw_Cpv_Type_of_contract(df, dtype)
        case _:
            print("Action par défaut")

def draw_Award_date_Award_price(df, dtype):
    df['awardDate'] = pd.to_datetime(df['awardDate'])

    # Extraire l'année de chaque date d'attribution pour regrouper les données par année
    df['Year'] = df['awardDate'].dt.year

    # Pour chaque année afficher le boxplot des awardPrice sans log
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Year', y='awardPrice', data=df)
    plt.xticks(rotation=45)
    plt.title('Distribution des prix d\'attribution par année')
    plt.xlabel('Année')
    plt.ylabel('Prix d\'attribution')  
    plt.grid(True)
    plt.tight_layout() 
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/boxplot_awardPrice_AwardDate_PerYear_without_log.png")
    # plt.show()
    plt.close()

    # Pour chaque année afficher le boxplot des awardPrice avec log
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Year', y='awardPrice', data=df)
    plt.xticks(rotation=45)
    plt.title('Distribution des prix d\'attribution par année')
    plt.xlabel('Année')
    plt.ylabel('Prix d\'attribution')  
    plt.grid(True)
    plt.yscale('log')
    plt.tight_layout() 
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/boxplot_awardPrice_AwardDate_PerYear_wit_log.png")
    # plt.show()
    plt.close()

    data_clean = df.copy()
    data_clean['awardPrice'] = pd.to_numeric(data_clean['awardPrice'], errors='coerce')
    data_clean = data_clean.dropna(subset=['awardPrice'])

    # Calculer la moyenne des prix d'attribution par année sans log
    average_price_per_year = data_clean.groupby('Year')['awardPrice'].mean().reset_index()
    average_price_per_year = average_price_per_year.dropna()
    sorted_years = sorted(average_price_per_year['Year'])

    plt.figure(figsize=(12, 8))
    plt.bar(range(len(sorted_years)), average_price_per_year['awardPrice'], color='skyblue')
    plt.xticks(range(len(sorted_years)), sorted_years, rotation=45)
    plt.title('Moyenne des Prix d\'Attribution par Année')
    plt.xlabel('Année')
    plt.ylabel('Prix d\'Attribution Moyen')
    plt.tight_layout()
    plt.grid(axis='y')
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_mean_awardPrice_AwardDate_PerYear_without_log.png")
    # plt.show()
    plt.close()


    # Calculer la moyenne des prix d'attribution par année avec log
    plt.figure(figsize=(12, 8))
    plt.bar(range(len(sorted_years)), average_price_per_year['awardPrice'], color='skyblue')
    plt.xticks(range(len(sorted_years)), sorted_years, rotation=45)
    plt.title('Moyenne des Prix d\'Attribution par Année')
    plt.xlabel('Année')
    plt.ylabel('Prix d\'Attribution Moyen')
    plt.tight_layout()
    plt.yscale('log')
    plt.grid(axis='y')
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_mean_awardPrice_AwardDate_PerYear_with_log.png")
    # plt.show()
    plt.close()

def draw_Award_price_Award_estimated_Price(df, dtype):
    data_clean = df
    data_clean['awardPrice'] = pd.to_numeric(data_clean['awardPrice'], errors='coerce')
    data_clean['awardEstimatedPrice'] = pd.to_numeric(data_clean['awardEstimatedPrice'], errors='coerce')
    data_clean = data_clean.dropna(subset=['awardPrice'])
    data_clean = data_clean.dropna(subset=['awardEstimatedPrice'])


    # Identifier le top 25 et bottom 25 basé sur 'awardPrice'
    top_25_awardPrice = data_clean.nlargest(30, 'awardPrice')
    bottom_25_awardPrice = data_clean.nsmallest(30, 'awardPrice')
    top_25_awardPrice['ID'] = top_25_awardPrice.index
    bottom_25_awardPrice['ID'] = bottom_25_awardPrice.index

    top_25_melted = pd.melt(top_25_awardPrice, id_vars=['ID'], value_vars=['awardPrice', 'awardEstimatedPrice'],
                            var_name='Type', value_name='Montant')

    bottom_25_melted = pd.melt(bottom_25_awardPrice, id_vars=['ID'], value_vars=['awardPrice', 'awardEstimatedPrice'],
                            var_name='Type', value_name='Montant')
                            
    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=top_25_melted, dodge=True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.title('Comparaison du top 25 Award Price et Estimated Award Price')
    plt.xlabel('Enregistrements')
    plt.ylabel('Montant')
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_top25_awardPrice_awardEstimatedPrice_without_log.png")
    # plt.show()
    plt.close()

    # Avec log
    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=top_25_melted, dodge=True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.yscale('log')
    plt.title('Comparaison du top 25 Award Price et Estimated Award Price')
    plt.xlabel('Enregistrements')
    plt.ylabel('Montant')
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_top25_awardPrice_awardEstimatedPrice_with_log.png")
    # plt.show()
    plt.close()

    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=bottom_25_melted, dodge=True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.title('Comparaison du bottom 25 Award Price et Estimated Award Price')
    plt.xlabel('Enregistrements')
    plt.ylabel('Montant')
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_bottom25_awardPrice_awardEstimatedPrice_without_log.png")
    # plt.show()
    plt.close()

    # Avec log
    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=bottom_25_melted, dodge=True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.yscale('log')
    plt.title('Comparaison du bottom 25 Award Price et Estimated Award Price')
    plt.xlabel('Enregistrements')
    plt.ylabel('Montant')
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_bottom25_awardPrice_awardEstimatedPrice_with_log.png")
    # plt.show()
    plt.close()

    # Identifier le top 25 basé sur 'awardEstimatedPrice'
    top_25_awardEstimatedPrice = data_clean.nlargest(30, 'awardEstimatedPrice')
    bottom_25_awardEstimatedPrice = data_clean.nsmallest(30, 'awardEstimatedPrice')
    top_25_awardEstimatedPrice['ID'] = top_25_awardEstimatedPrice.index
    bottom_25_awardEstimatedPrice['ID'] = bottom_25_awardEstimatedPrice.index

    top_25_melted = pd.melt(top_25_awardEstimatedPrice, id_vars=['ID'], value_vars=['awardPrice', 'awardEstimatedPrice'],
                            var_name='Type', value_name='Montant')

    bottom_25_melted = pd.melt(bottom_25_awardEstimatedPrice, id_vars=['ID'], value_vars=['awardPrice', 'awardEstimatedPrice'],
                            var_name='Type', value_name='Montant')

    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=top_25_melted, dodge=True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.title('Comparaison du top 25 Estimated Award Price et Award Price')
    plt.xlabel('Enregistrements')
    plt.ylabel('Montant')
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_top25_awardEstimatedPrice_awardPrice_without_log.png")
    # plt.show()
    plt.close()

    # Avec log
    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=top_25_melted, dodge=True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.yscale('log')
    plt.title('Comparaison du top 25 Estimated Award Price et Award Price')
    plt.xlabel('Enregistrements')
    plt.ylabel('Montant')
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_top25_awardEstimatedPrice_awardPrice_with_log.png")
    # plt.show()
    plt.close()

    # Identifier bottom 25 basé sur 'awardEstimatedPrice'
    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=bottom_25_melted, dodge=True)
    plt.legend()
    plt.xticks(rotation=45)
    plt.title('Comparaison du bottom 25 Estimated Award Price et Award Price')
    plt.xlabel('Enregistrements')
    plt.ylabel('Montant')
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_bottom25_awardEstimatedPrice_awardPrice_without_log.png")
    # plt.show()
    plt.close()

    # Avec log
    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=bottom_25_melted, dodge=True)
    plt.xticks(rotation=45)
    plt.yscale('log')
    plt.title('Comparaison du bottom 25 Estimated Award Price et Award Price')
    plt.xlabel('Enregistrements')
    plt.ylabel('Montant')
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_bottom25_awardEstimatedPrice_awardPrice_with_log.png")
    # plt.show()
    plt.close()

    # Identifier le top 25 basé sur la différence entre AwardPrice et AwardEstimatedPrice
    data_clean['Difference'] = (data_clean['awardPrice'] - data_clean['awardEstimatedPrice']).abs()
    top_25_smallest_difference = data_clean.nsmallest(25, 'Difference')
    top_25_biggest_difference = data_clean.nlargest(25, 'Difference')

    top_25_biggest_difference['ID'] = top_25_biggest_difference.index
    top_25_smallest_difference['ID'] = top_25_smallest_difference.index

   
    top_25_melted = pd.melt(top_25_smallest_difference, id_vars=['ID'], value_vars=['awardPrice', 'awardEstimatedPrice'],
                            var_name='Type', value_name='Montant')
                        
    bottom_25_melted = pd.melt(top_25_biggest_difference, id_vars=['ID'], value_vars=['awardPrice', 'awardEstimatedPrice'],
                            var_name='Type', value_name='Montant')

    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=top_25_melted, dodge=True)
    plt.xticks(rotation=90)
    plt.legend()
    plt.title('Top 25 des plus petites différences entre Award Price et Estimated Award Price')
    plt.xlabel('ID des Enregistrements')
    plt.ylabel('Montant')
    plt.tight_layout()
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_top25_difference_awardEstimatedPrice_awardPrice.png")
    # plt.show()
    plt.close()

    # Identifier le bottom 25 basé sur la différence entre AwardPrice et AwardEstimatedPrice
    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=bottom_25_melted, dodge=True)
    plt.xticks(rotation=90)  # Rotation pour une meilleure lisibilité des étiquettes de l'axe x
    plt.legend()
    plt.title('Top 25 des plus grandes différences entre Award Price et Estimated Award Price')
    plt.xlabel('ID des Enregistrements')
    plt.ylabel('Montant')
    plt.tight_layout()
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_bottom25_difference_awardEstimatedPrice_awardPrice_without_log.png")
    # plt.show()
    plt.close()

    # Avec log
    plt.figure(figsize=(14, 8))
    sns.barplot(x='ID', y='Montant', hue='Type', data=bottom_25_melted, dodge=True)
    plt.xticks(rotation=90)  # Rotation pour une meilleure lisibilité des étiquettes de l'axe x
    plt.legend()
    plt.yscale('log')
    plt.title('Top 25 des plus grandes différences entre Award Price et Estimated Award Price')
    plt.xlabel('ID des Enregistrements')
    plt.ylabel('Montant')
    plt.tight_layout()  
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_bottom25_difference_awardEstimatedPrice_awardPrice_with_log.png")
    # plt.show()
    plt.close()

    # Histogram bins de même tailles pour les différences
    smallest_difference = data_clean['Difference'].min()
    largest_difference = data_clean['Difference'].max()
    plt.figure(figsize=(14, 8))
    num_bins = 100
    plt.hist(data_clean['Difference'], bins=num_bins, color='skyblue', edgecolor='black')
    plt.title('Histogramme des différences entre Award Price et Estimated Award Price')
    plt.xlabel('Différence absolue')
    plt.ylabel('Nombre d\'enregistrements')
    plt.legend()
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_differences_awardEstimatedPrice_awardPrice_without_log.png")
    # plt.show()
    plt.close()

    # Avec log
    plt.figure(figsize=(14, 8))
    num_bins = 100
    plt.yscale('log')
    plt.hist(data_clean['Difference'], bins=num_bins, color='skyblue', edgecolor='black')
    plt.title('Histogramme des différences entre Award Price et Estimated Award Price')
    plt.xlabel('Différence absolue')
    plt.ylabel('Nombre d\'enregistrements')
    plt.legend()
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_differences_awardEstimatedPrice_awardPrice_with_log.png")
    # plt.show()
    plt.close()

def draw_Cpv_Type_of_contract(df, dtype):
    data_clean = df
    data_clean = data_clean.dropna(subset=['cpv', 'typeOfContract'])
    data_clean['cpv'] = df['cpv'].astype(str).str[:2]

    cpv_counts = data_clean.groupby(['typeOfContract', 'cpv']).size().reset_index(name='counts')
    top_cpv = cpv_counts.sort_values(['typeOfContract', 'counts'], ascending=[True, False]).groupby('typeOfContract').head(10)
    bottom_cpv = cpv_counts.sort_values(['typeOfContract', 'counts'], ascending=[True, True]).groupby('typeOfContract').head(10)

    # Top 10 occurences cpv pour chaque type de contrat
    plt.figure(figsize=(14, 8))
    sns.catplot(x='cpv', y='counts', hue='typeOfContract', data=top_cpv, kind='bar', height=5, aspect=2)
    plt.xticks(rotation=90)
    plt.xlabel("CPV")
    plt.ylabel("Occurences")
    plt.title("Top 10 occurences CPV pour chaque type de contrat")
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_top10_occurences_cpv_type_of_contract_without_log.png")
    # plt.show()
    plt.close()

    # Avec log
    plt.figure(figsize=(14, 8))
    sns.catplot(x='cpv', y='counts', hue='typeOfContract', data=top_cpv, kind='bar', height=5, aspect=2)
    plt.xticks(rotation=90)
    plt.xlabel("CPV")
    plt.ylabel("Occurences")
    plt.yscale('log')
    plt.title("Top 10 occurences CPV pour chaque type de contrat")
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_top10_occurences_cpv_type_of_contract_with_log.png")
    # plt.show()
    plt.close()

    # Bottom 10 occurences cpv pour chaque type de contrat
    plt.figure(figsize=(14, 8))
    sns.catplot(x='cpv', y='counts', hue='typeOfContract', data=bottom_cpv, kind='bar', height=5, aspect=2)
    plt.xticks(rotation=90)
    plt.xlabel("CPV")
    plt.ylabel("Occurences")
    plt.title("Bottom 10 occurences CPV pour chaque type de contrat")
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_bottom10_occurences_cpv_type_of_contract_without_log.png")
    # plt.show()
    plt.close()

    # Avec log
    plt.figure(figsize=(14, 8))
    sns.catplot(x='cpv', y='counts', hue='typeOfContract', data=bottom_cpv, kind='bar', height=5, aspect=2)
    plt.xticks(rotation=90)
    plt.xlabel("CPV")
    plt.ylabel("Occurences")
    plt.yscale('log')
    plt.title("Bottom 10 occurences CPV pour chaque type de contrat")
    plt.savefig(sys.path[0] + f'\\fig\\Lots_Pair_Variable'+ "/histogram_bottom10_occurences_cpv_type_of_contract_with_log.png")
    # plt.show()
    plt.close()


if __name__ == "__main__":
    input_csv_path = sys.argv[1]
    read_csv(input_csv_path)