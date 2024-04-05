import requests
import varsEnv as env
from scriptReadSql import create_df_from_query

BEARER_TOKEN = env.BEARER_TOKEN

endpoint = "https://api.insee.fr/entreprises/sirene/V3.11/siret/"


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def check_agents_with_siret(conn):
    df = create_df_from_query(
        conn,
        "SELECT * FROM Agents",
    )
    print(df)
    for index, row in df.iterrows():
        if row["siret"] is not None:
            try:
                res = requests.get(
                    endpoint + row["siret"], auth=BearerAuth(BEARER_TOKEN)
                )
                res = res.json()
                # print(res["etablissement"]["siren"])
                df.at[index, "siren"] = res["etablissement"]["siren"]
                # print(df)
                df.at[index, "categorieEntreprise"] = res["etablissement"][
                    "uniteLegale"
                ]["categorieEntreprise"]
                # print(type(res["etablissement"]["adresseEtablissement"]["codePostalEtablissement"]))
                # print(type(df["zipcode"][0]))
                # print(type(df["department"][0]))
                # print(res["etablissement"]["adresseEtablissement"]["codePostalEtablissement"][:2])
                if (
                    row["zipcode"]
                    != res["etablissement"]["adresseEtablissement"][
                        "codePostalEtablissement"
                    ]
                ):
                    df.at[index, "zipcode"] = res["etablissement"][
                        "adresseEtablissement"
                    ]["codePostalEtablissement"]
                if (
                    row["department"]
                    != res["etablissement"]["adresseEtablissement"][
                        "codePostalEtablissement"
                    ][:2]
                ):
                    df.at[index, "department"] = res["etablissement"][
                        "adresseEtablissement"
                    ]["codePostalEtablissement"][:2]
            except Exception as e:
                print(f"Error processing row {index}: {e}")
    print(df)


def testapi():
    res = requests.get(endpoint, auth=BearerAuth(BEARER_TOKEN))
    print(res.json())
