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
    # n = 0
    for index, row in df.iterrows():
        # n += 1
        if row["siret"] is not None:
            try:
                res = requests.get(
                    endpoint + row["siret"], auth=BearerAuth(BEARER_TOKEN)
                )
                res = res.json()
                df.at[index, "siren"] = res["etablissement"]["siren"]
                df.at[index, "categorieEntreprise"] = res["etablissement"][
                    "uniteLegale"
                ]["categorieEntreprise"]
                if (
                    row["zipcode"]
                    != res["etablissement"]["adresseEtablissement"][
                        "codePostalEtablissement"
                    ]
                ):
                    df.at[index, "zipcode"] = res["etablissement"][
                        "adresseEtablissement"
                    ]["codePostalEtablissement"]
                    print()
                if (
                    res["etablissement"]["adresseEtablissement"][
                        "codeCommuneEtablissement"
                    ][:2]
                    == "97"
                ):
                    if (
                        row["department"]
                        != res["etablissement"]["adresseEtablissement"][
                            "codeCommuneEtablissement"
                        ][:3]
                    ):
                        df.at[index, "department"] = res["etablissement"][
                            "adresseEtablissement"
                        ]["codeCommuneEtablissement"][:3]
                else:
                    if (
                        row["department"]
                        != res["etablissement"]["adresseEtablissement"][
                            "codeCommuneEtablissement"
                        ][:2]
                    ):
                        df.at[index, "department"] = res["etablissement"][
                            "adresseEtablissement"
                        ]["codeCommuneEtablissement"][:2]
            except Exception as e:
                print(f"Error processing row {index}: {e}. ")
        # if n == 10:
        #     break
    df.to_sql(name="Agents", if_exists="replace", con=conn, index=False)
    print("Mise à jour effectuée pour les lotsNumber spécifiés.")


def testapi():
    res = requests.get(endpoint, auth=BearerAuth(BEARER_TOKEN))
    print(res.json())
