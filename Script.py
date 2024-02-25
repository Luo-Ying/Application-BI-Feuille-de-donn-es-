import pandas as pd
import numpy as np
import sys
import os

DTYPE_DICT_LOTS = {'lotId': 'Int64', 'tedCanId': 'Int64', 'correctionsNb': 'Int64', 'cancelled': 'Int64', 'awardDate': 'object', 'awardEstimatedPrice': 'Float64',
'awardPrice': 'Float64', "cpv" : 'Int64', 'numberTenders' : 'Int64', 'onBehalf': 'object' , 'jointProcurement' : 'object' , 'fraAgreement' : 'object',
'fraEstimated' : 'object', 'lotsNumber' : 'object', 'accelerated' : 'object', 'outOfDirectives': 'Int64', 'contractorSme' : 'object', 'numberTendersSme' : 'Float64' ,
'subContracted' : 'object', 'gpa' : 'object', 'multipleCae': 'object', 'typeOfContract': 'object', 'topType' : 'object', 'renewal': 'object', 'contractDuration': 'Float64',
'publicityDuration' : 'Float64'}

def read_csv(input_csv_path):
    match os.path.basename(input_csv_path):
        case 'Lots.csv':
            df = pd.read_csv(input_csv_path, dtype=DTYPE_DICT_LOTS, sep=',')
            column = read_user_column(df)
            choose_Diagram(DTYPE_DICT_LOTS[column])
        case _:
            print("Action par defaut")

def read_user_column(df):
    print("Voici les colonnes disponibles : ")
    for col in df.columns:
        print(col)
    print("Veuillez selectionner une colonne : ")
    return input()

def choose_Diagram(column_type):
    match column_type:
        case 'Int64':
        case 'object':
        case 'Float64':
        case _:
            print("Action par defaut")

if __name__ == '__main__':
    input_csv_path = sys.argv[1]
    read_csv(input_csv_path)