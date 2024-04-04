import requests

from extractor import *


def createXML(filename):
    url = f"https://ted.europa.eu/fr/notice/{filename}/xml"
    response = requests.get(url)
    data = response.text
    file_path = f'./tedId/{filename}.xml'
    with open(file_path, 'w', encoding="utf-8") as file:
        file.write(data)


def transform(tedCanId):
    ted = str(tedCanId)
    year = ted[:4]
    remaining = ted[4:]
    return f"{remaining}-{year}"


def openXML(filename):
    file_path = f'./tedId/{filename}.xml'
    raw = extract(file_path)
    print(raw)
