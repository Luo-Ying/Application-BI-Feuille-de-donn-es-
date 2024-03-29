from scriptGraphics.db import connect_db, close_db
from scripts_individuel import scripts_individuel
from scripts_paires import scripts_paires

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

DTYPE_DICT_NAMES = {
    "agentId": "Int64",
    "name": "object",
}

DTYPE_DICT_CRITERIA = {
    "criterionId": "Int64",
    "lotId": "Int64",
    "name": "object",
    "weight": "Float64",
    "type": "object",
}

all_columns = []
diagrams = ["camembert", "top 5", "worst 5", "nuage de points", "gauge", "radar", "tree map", "box plot", "violin plot",
            "histogram", "tab"]


def getType(df, column):
    print(f'{df[column].name} est de type {df[column].dtype}')


if __name__ == "__main__":
    db_path = 'Input\\Foppa.db'
    connexion = connect_db(db_path)
    scripts_individuel(connexion)
    # scripts_paires(connexion)
    close_db(connexion)
