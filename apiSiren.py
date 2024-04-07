import requests
import varsEnv as env
from scriptReadSql import create_df_from_query
import csv
import pandas as pd

from scriptGraphics.generateFileChart import generateFileTab

BEARER_TOKEN = env.BEARER_TOKEN

endpoint = "https://api.insee.fr/entreprises/sirene/V3.11/siren/"


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


keys = [
    "siren",
    "statutDiffusionUniteLegale",
    "dateCreationUniteLegale",
    "denominationUniteLegale",
    "categorieEntreprise",
    "trancheEffectifsUniteLegale",
    "activitePrincipaleUniteLegale",
    "economieSocialeSolidaireUniteLegale",
]

statutDiffusionUniteLegale = {
    "O": "Unité diffusible",
    "P": "Unité en diffusion partielle",
}

trancheEffectifsUniteLegale = {
    "NN": "Unité non-employeuse ou présumée non-employeuse (faute de déclaration reçue)",
    "00": "0 salarié (n'ayant pas d'effectif au 31/12 mais ayant employé des salariés au cours de l'année de référence)",
    "01": "1 ou 2 salariés",
    "02": "3 à 5 salariés",
    "03": "6 à 9 salariés",
    "11": "10 à 19 salariés",
    "12": "20 à 49 salariés",
    "21": "50 à 99 salariés",
    "22": "100 à 199 salariés",
    "31": "200 à 249 salariés",
    "32": "250 à 499 salariés",
    "41": "500 à 999 salariés",
    "42": "1 000 à 1 999 salariés",
    "51": "2 000 à 4 999 salariés",
    "52": "5 000 à 9 999 salariés",
    "53": "10 000 salariés et plus",
    "null": 'donnée manquante ou "sans objet"',
}

activitePrincipaleUniteLegale = pd.read_excel("References/int_courts_naf_rev_2.xls")
# print(activitePrincipaleUniteLegale)
activite_dict = dict(
    zip(
        activitePrincipaleUniteLegale["Code"],
        activitePrincipaleUniteLegale["Intitulés_NAF_rev_2_version_finale"],
    )
)


economieSocialeSolidaireUniteLegale = {
    "O": "l'entreprise appartient au champ de l'économie sociale et solidaire",
    "N": "l'entreprise n'appartient pas au champ de l'économie sociale et solidaire",
}


def get_info_detail_Agents(df, filename):
    # print(activitePrincipaleUniteLegale)
    data = []
    for index, row in df.iterrows():
        for column_name in df.columns:
            if "siren" in column_name and row[column_name] is not None:
                try:
                    res = requests.get(
                        endpoint + str(row[column_name]), auth=BearerAuth(BEARER_TOKEN)
                    )
                    res = res.json()
                    # print(res)
                    values = {}
                    for key in keys:
                        value = None
                        # Check if the key exists in the data
                        if key in res["uniteLegale"]:
                            value = res["uniteLegale"][key]
                        else:
                            value = []
                            for item in res["uniteLegale"]["periodesUniteLegale"]:
                                if key in item:
                                    value.append(value.append(item[key]))
                        values[key] = value
                        # break
                    values = clean_data(values)
                    values = replace_details_infos(values)
                    # print(values)
                    data.append(values)
                except Exception as e:
                    print(f"Error processing row {index} and column {column_name}: {e}")
    df = pd.DataFrame(data)
    generateFileTab("Top50", filename, df)


def replace_details_infos(data):
    data["statutDiffusionUniteLegale"] = statutDiffusionUniteLegale.get(
        data["statutDiffusionUniteLegale"], None
    )
    data["trancheEffectifsUniteLegale"] = trancheEffectifsUniteLegale.get(
        data["trancheEffectifsUniteLegale"], None
    )
    data["activitePrincipaleUniteLegale"] = [
        activite_dict.get(code, None) for code in data["activitePrincipaleUniteLegale"]
    ]
    data["economieSocialeSolidaireUniteLegale"] = [
        economieSocialeSolidaireUniteLegale.get(code, None)
        for code in data["economieSocialeSolidaireUniteLegale"]
    ]
    data = clean_data(data)
    return data


def clean_data(data):
    for key, value in data.items():
        # If the value is a list, filter out the None values
        if isinstance(value, list):
            # Use a set to keep track of unique values
            unique_values = set()
            # Iterate through the list and keep only unique values
            data[key] = [
                item
                for item in value
                if item is not None
                and item not in unique_values
                and not unique_values.add(item)
            ]
    return data
