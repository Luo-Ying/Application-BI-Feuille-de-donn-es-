import requests
from bs4 import BeautifulSoup

from extractor import get_total, extract


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
    with open(file_path, 'r', encoding="utf-8") as file:
        return BeautifulSoup(file.read(), 'xml')


def openJSON(filename):
    file_path = f'./tedId/{filename}.xml'
    raw = extract(file_path)
    print(raw)


def search_tag(xml, tagName):
    return xml.find_all(tagName)[0]


def get_content_tag(xml, tagName):
    return xml.find_all(tagName)


def get_value_tag(xml, tagName):
    return xml[tagName]


def count_tag(xml, parentTagName, tagName):
    tags = search_tag(xml, parentTagName)
    return len(tags.find_all(tagName))
