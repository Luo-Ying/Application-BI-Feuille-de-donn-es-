import numpy as np
from bs4 import BeautifulSoup
from getTedXML import *
from scriptReadSql import *


def correctedData(conn):
    all_db = create_df_from_query(
        conn,
        f"SELECT * FROM Lots",
    )
    # tedCanId = "2012208072"
    # tedCanId = "2017407163"
    # tedCanId = "2010142"
    # tedCanId = "201484598"
    tedCanId = "2020154110"
    df = create_df_from_query(
        conn,
        f"SELECT * FROM Lots WHERE tedCanId IN ({tedCanId})",
    )
    # print(df)
    ted = transform(tedCanId)
    # createXML(ted)
    fileXML = openXML(ted)
    # fileJSON = openJSON(ted)
    display_information(tedCanId, fileXML)


def display_information(tedCanId, fileXML):
    """TedCanId"""
    print(f"TedCanId : {tedCanId}")
    """GPA"""
    print(f"GPA ? {is_gpa(fileXML)}")
    """NumberTenders"""
    print(f"NumberTenders : {get_numberTenders(fileXML)}")
    """NumberTenders"""
    print(f"NumberTendersSme : {get_numberTendersSme(fileXML)}")
    """NumberTenders"""
    print(f"LotsNumber : {get_lotsNumber(fileXML)}")
    """Accelerated"""
    print(f"Accelerated ? {is_accelerated(fileXML)}")
    """CPV"""
    print(f"CPV : {get_CPV(fileXML)}")
    """AwardDate"""
    print(f"AwardDate : {get_awardDate(fileXML)}")
    """TypeOfContract"""
    print(f"TypeOfContract : {which_typeOfContract(fileXML)}")
    """awardEstimatedPrice"""
    print(f"awardEstimatedPrice : {get_awardEstimatedPrice(fileXML)}")
    """awardPrice"""
    print(f"awardPrice : {get_awardPrice(fileXML)}")
    """fraAgreement"""
    print(f"fraAgreement  : {is_fraAgreement(fileXML)}")
    """renewal"""
    print(f"is_renewal  : {is_renewal(fileXML)}")
    """contractDuration"""
    print(f"contractDuration : {get_contractDuration(fileXML)}")
    # """publicityDuration"""
    # print(f"awardPrice : {calculate_publicityDuration(fileXML)}")


def get_contractDuration(fileXML):
    try:
        tags = get_content_tag(fileXML, "DURATION")
        return [int(content.get_text()) for content in tags]
    except Exception as e:
        return 0


def is_renewal(fileXML):
    try:
        tag = get_content_tag(fileXML, "RENEWAL")
        return 1 if tag[0] else 0
    except Exception as e:
        return 0


def is_fraAgreement(fileXML):
    try:
        tag = get_content_tag(fileXML, "NOTICE_INVOLVES_DESC")
        fraAgreement = [get_value_tag(content, "VALUE") for content in tag]
        return 1 if fraAgreement[0] == "CONCLUSION_FRAMEWORK_AGREEMENT" else 0
    except Exception as e:
        return 0


def get_awardEstimatedPrice(fileXML):
    try:
        tags_currencies = get_content_tag(fileXML, "INITIAL_ESTIMATED_TOTAL_VALUE_CONTRACT")
        currencies = [get_value_tag(content, "CURRENCY") for content in tags_currencies]
        tags = get_content_tag(fileXML, "VALUE_COST")
        results = [float(content.get_text().replace(' ', '').replace(',', '.')) for content in tags]
        for i in range(0, len(tags)):
            if str(currencies[i]) != "EUR":
                results[i] = np.nan
        if not results:
            tags2 = get_content_tag(fileXML, "VALUE")
            estimated = [get_value_tag(content, "TYPE") for content in tags2]
            currencies2 = [get_value_tag(content, "CURRENCY") for content in tags2]
            if str(estimated[0]) == "ESTIMATED_TOTAL":
                results2 = [float(content.get_text().replace(' ', '').replace(',', '.')) for content in tags2]
                for i in range(0, len(tags2)):
                    if str(currencies2[i]) != "EUR":
                        results2[i] = np.nan
                return results2 if results2 else results
            else:
                return results if results else None
        return results
    except Exception as e:
        return None


def get_awardPrice(fileXML):
    try:
        tags = get_content_tag(fileXML, "VALUE")
        currencies = [get_value_tag(content, "CURRENCY") for content in tags]
        try:
            estimated = [get_value_tag(content, "TYPE") for content in tags]
            tags2 = get_content_tag(fileXML, "VAL_OBJECT")
            currencies2 = [get_value_tag(content, "CURRENCY") for content in tags2]
            results2 = [float(content.get_text().replace(' ', '').replace(',', '.')) for content in tags2]
            for i in range(0, len(tags2)):
                if str(currencies2[i]) != "EUR":
                    results2[i] = np.nan
            return results2
        except Exception as e2:
            results = [float(content.get_text().replace(' ', '').replace(',', '.')) for content in tags]
            for i in range(0, len(tags)):
                if str(currencies[i]) != "EUR":
                    results[i] = np.nan
            return results
    except Exception as e:
        return None


def which_typeOfContract(fileXML):
    try:
        parentTag = search_tag(fileXML, "NC_CONTRACT_NATURE")
        value = get_value_tag(parentTag, "CODE")
        if int(value) == 1:
            return 'W'
        elif int(value) == 2:
            return 'S'
        elif int(value) == 4:
            return 'U'
    except Exception as e:
        return None


def get_awardDate(fileXML):
    try:
        tags = get_content_tag(fileXML, "DATE_CONCLUSION_CONTRACT")
        results = [content.get_text() for content in tags]
        if not results:
            tags = get_content_tag(fileXML, "CONTRACT_AWARD_DATE")
            dates = [content.get_text() for content in tags]
            formatted_dates = [date.strip().replace('\n', '-') for date in dates]
            return formatted_dates
        return results
    except Exception as e:
        return None


def is_gpa(fileXML):
    try:
        tag = get_content_tag(fileXML, "RP_REGULATION")
        if (str(tag[0]).lower()).count("gpa") > 0:
            return 1
    except Exception as e:
        try:
            tag = get_content_tag(fileXML, "CONTRACT_COVERED_GPA")
            value = get_value_tag(tag[0], "VALUE")
            return 1 if str(value) == "YES" else 0
        except Exception as e2:
            return 0
    return 0


def get_numberTenders(fileXML):
    try:
        tag = get_content_tag(fileXML, "NB_TENDERS_RECEIVED")
        return int(tag[0].get_text())
    except Exception as e:
        tags = get_content_tag(fileXML, "OFFERS_RECEIVED_NUMBER")
        results = [int(content.get_text()) for content in tags]
        if not results:
            return 0
        return results


def get_numberTendersSme(fileXML):
    try:
        tag = get_content_tag(fileXML, "NB_TENDERS_RECEIVED_SME")
        return int(tag[0].get_text())
    except Exception as e:
        return 0


def get_CPV(fileXML):
    try:
        parentTag = search_tag(fileXML, "ORIGINAL_CPV")
        value = get_value_tag(parentTag, "CODE")
        return value
    except Exception as e:
        try:
            parentTag = search_tag(fileXML, "OBJECT_DESCR")
            value = get_value_tag(parentTag, "ITEM")
            return value
        except Exception as e:
            return None


def get_lotsNumber(fileXML):
    try:
        parentTag = search_tag(fileXML, "AWARD_CONTRACT")
        value = get_value_tag(parentTag, "ITEM")
        return value
    except Exception as e:
        try:
            parentTag = search_tag(fileXML, "BIB_DOC_S")
            value = get_value_tag(parentTag, "ITEM")
            return value
        except Exception as e2:
            try:
                tags = get_content_tag(fileXML, "LOT_NUMBER")
                results = [int(content.get_text()) for content in tags]
                if not results:
                    tags = get_content_tag(fileXML, "CONTRACT_NUMBER")
                    results2 = [int(content.get_text()) for content in tags]
                    if not results2:
                        tags = get_content_tag(fileXML, "LOT_NO")
                        return [int(content.get_text()) for content in tags]
                    return results2 if results2 else results
                return results
            except Exception as e4:
                return 0


def is_accelerated(fileXML):
    try:
        tag = search_tag(fileXML, "ACCELERATED_PROC")
        if tag:
            return 1
    except Exception as e:
        return 0
    return 0
