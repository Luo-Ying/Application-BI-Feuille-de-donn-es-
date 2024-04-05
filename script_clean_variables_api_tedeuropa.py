import numpy as np
import csv

from datetime import datetime
from bs4 import BeautifulSoup
from getTedXML import *
from scriptReadSql import *


def correctedData(conn):
    all_tedCanId = create_df_from_query(
        conn,
        f"SELECT DISTINCT(tedCanId) FROM Lots",
    )
    for tedCanId in all_tedCanId.index:
        tedCanId = all_tedCanId['tedCanId'][tedCanId]
        ted = transform(tedCanId)
        createXML(ted)
        fileXML = openXML(ted)
        # fileJSON = openJSON(ted)
        # print("NEW")
        # display_information(tedCanId, fileXML)
        # Récupération des ids des Lots
        lots_numbers_xml = get_lotsNumber(fileXML)

        i = 0
        if lots_numbers_xml:
            cur = conn.cursor()
            update_lotsNumber_from_xml(conn, cur, tedCanId, lots_numbers_xml)
            for lot_number in lots_numbers_xml:
                cur.execute(f"SELECT * FROM Lots WHERE tedCanId = {tedCanId} AND lotsNumber = {lot_number}")
                row = cur.fetchone()
                en_tetes = ['tedCanId', 'lot_number', 'columnName', 'oldValue', 'newValue']
                filename = 'historique_modifications.csv'
                fichier_vide = not os.path.exists(filename) or os.stat(filename).st_size == 0
                with open('historique_modifications.csv', mode='a', newline='') as file:
                    writer = csv.writer(file)
                    if fichier_vide:
                        writer.writerow(en_tetes)
                    """awardDate"""
                    if get_awardDate(fileXML):
                        if i < len(get_awardDate(fileXML)) and type(get_awardDate(fileXML)) == list:
                            new_value_awardDate = get_awardDate(fileXML)[i]
                            if row and row[4] != new_value_awardDate and new_value_awardDate is not None:
                                writer.writerow([tedCanId, lot_number, 'awardDate', row[4], new_value_awardDate])
                                cur.execute("UPDATE Lots SET awardDate = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                            (new_value_awardDate, tedCanId, lot_number))
                                conn.commit()

                    """awardEstimatedPrice"""
                    if get_awardEstimatedPrice(fileXML):
                        if i < len(get_awardEstimatedPrice(fileXML)) and type(get_awardEstimatedPrice(fileXML)) == list:
                            new_value_awardEstimatedPrice = get_awardEstimatedPrice(fileXML)[i]
                            if row and row[
                                5] != new_value_awardEstimatedPrice and new_value_awardEstimatedPrice is not None:
                                writer.writerow(
                                    [tedCanId, lot_number, 'awardEstimatedPrice', row[5],
                                     new_value_awardEstimatedPrice])
                                cur.execute(
                                    "UPDATE Lots SET awardEstimatedPrice = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                    (new_value_awardEstimatedPrice, tedCanId, lot_number))
                                conn.commit()

                    """awardPrice"""
                    if get_awardPrice(fileXML):
                        if i < len(get_awardPrice(fileXML)) and type(get_awardPrice(fileXML)) == list:
                            new_value_awardPrice = get_awardPrice(fileXML)[i]
                            if row and row[6] != new_value_awardPrice and new_value_awardPrice is not None:
                                writer.writerow([tedCanId, lot_number, 'awardPrice', row[6], new_value_awardPrice])
                                cur.execute("UPDATE Lots SET awardPrice = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                            (new_value_awardPrice, tedCanId, lot_number))
                                conn.commit()

                    """CPV"""
                    new_value_cpv = get_CPV(fileXML)
                    if row and new_value_cpv is not None:
                        if row[7] != new_value_cpv:
                            writer.writerow([tedCanId, lot_number, 'cpv', row[7], new_value_cpv])
                            cur.execute("UPDATE Lots SET cpv = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                        (new_value_cpv, tedCanId, lot_number))
                            conn.commit()

                    """NumberTenders"""
                    if get_numberTenders(fileXML):
                        if i < len(get_numberTenders(fileXML)) and type(get_numberTenders(fileXML)) == list:
                            new_value_numberTenders = get_numberTenders(fileXML)[i]
                            if row and new_value_numberTenders is not None:
                                if row[8] != new_value_numberTenders:
                                    writer.writerow(
                                        [tedCanId, lot_number, 'numberTenders', row[8], new_value_numberTenders])
                                    cur.execute(
                                        "UPDATE Lots SET numberTenders = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                        (new_value_numberTenders, tedCanId, lot_number))
                                    conn.commit()

                    """fraAgreement"""
                    new_value_fraAgreement = is_fraAgreement(fileXML)
                    if row and new_value_fraAgreement is not None:
                        if row[11] != new_value_fraAgreement:
                            writer.writerow([tedCanId, lot_number, 'fraAgreement', row[11], new_value_fraAgreement])
                            cur.execute("UPDATE Lots SET fraAgreement = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                        (new_value_fraAgreement, tedCanId, lot_number))
                            conn.commit()

                    """accelerated"""
                    new_value_accelerated = is_accelerated(fileXML)
                    if row and new_value_accelerated is not None:
                        if row[14] != new_value_accelerated:
                            writer.writerow([tedCanId, lot_number, 'accelerated', row[14], new_value_accelerated])
                            cur.execute("UPDATE Lots SET accelerated = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                        (new_value_accelerated, tedCanId, lot_number))
                            conn.commit()

                    """NumberTendersSme"""
                    new_value_numberTendersSme = get_numberTendersSme(fileXML)
                    if row and new_value_numberTendersSme is not None:
                        if row[17] != new_value_numberTendersSme:
                            writer.writerow(
                                [tedCanId, lot_number, 'numberTendersSme', row[17], new_value_numberTendersSme])
                            cur.execute("UPDATE Lots SET numberTendersSme = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                        (new_value_numberTendersSme, tedCanId, lot_number))
                            conn.commit()

                    """GPA"""
                    new_value_gpa = is_gpa(fileXML)
                    if row and new_value_gpa is not None:
                        if row[19] != new_value_gpa:
                            writer.writerow([tedCanId, lot_number, 'gpa', row[19], new_value_gpa])
                            cur.execute("UPDATE Lots SET gpa = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                        (new_value_gpa, tedCanId, lot_number))
                            conn.commit()

                    """typeOfContract"""
                    new_value_typeOfContract = which_typeOfContract(fileXML)
                    if row and new_value_typeOfContract is not None:
                        if row[21] != new_value_typeOfContract:
                            writer.writerow([tedCanId, lot_number, 'typeOfContract', row[21], new_value_typeOfContract])
                            cur.execute("UPDATE Lots SET typeOfContract = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                        (new_value_typeOfContract, tedCanId, lot_number))
                            conn.commit()

                    """renewal"""
                    new_value_renewal = is_renewal(fileXML)
                    if row and new_value_renewal is not None:
                        if row[23] != new_value_renewal:
                            writer.writerow([tedCanId, lot_number, 'renewal', row[23], new_value_renewal])
                            cur.execute("UPDATE Lots SET renewal = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                        (new_value_renewal, tedCanId, lot_number))
                            conn.commit()

                    """contractDuration"""
                    new_value_contractDuration = get_contractDuration(fileXML)
                    if row and len(new_value_contractDuration) > 0:
                        if row[24] != new_value_contractDuration:
                            writer.writerow(
                                [tedCanId, lot_number, 'contractDuration', row[24], new_value_contractDuration])
                            cur.execute("UPDATE Lots SET contractDuration = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                        (new_value_contractDuration, tedCanId, lot_number))
                            conn.commit()

                    """publicityDuration"""
                    new_value_publicityDuration = calculate_publicityDuration(fileXML)
                    if row and new_value_publicityDuration is not None:
                        if row[25] != new_value_publicityDuration:
                            writer.writerow(
                                [tedCanId, lot_number, 'publicityDuration', row[25], new_value_publicityDuration])
                            cur.execute("UPDATE Lots SET publicityDuration = ? WHERE tedCanId = ? AND lotsNumber = ?",
                                        (new_value_publicityDuration, tedCanId, lot_number))
                            conn.commit()
                    i += 1


def display_information(tedCanId, fileXML):
    """TedCanId"""
    print(f"TedCanId : {tedCanId}")
    """AwardDate"""
    print(f"AwardDate : {get_awardDate(fileXML)}")
    """awardEstimatedPrice"""
    print(f"awardEstimatedPrice : {get_awardEstimatedPrice(fileXML)}")
    """awardPrice"""
    print(f"awardPrice : {get_awardPrice(fileXML)}")
    """CPV"""
    print(f"CPV : {get_CPV(fileXML)}")
    """NumberTenders"""
    print(f"NumberTenders : {get_numberTenders(fileXML)}")
    """fraAgreement"""
    print(f"fraAgreement  : {is_fraAgreement(fileXML)}")
    """LotsNumber"""
    print(f"LotsNumber : {get_lotsNumber(fileXML)}")
    """Accelerated"""
    print(f"Accelerated ? {is_accelerated(fileXML)}")
    """NumberTendersSme"""
    print(f"NumberTendersSme : {get_numberTendersSme(fileXML)}")
    """GPA"""
    print(f"GPA ? {is_gpa(fileXML)}")
    """TypeOfContract"""
    print(f"TypeOfContract : {which_typeOfContract(fileXML)}")
    """renewal"""
    print(f"is_renewal  : {is_renewal(fileXML)}")
    """contractDuration"""
    print(f"contractDuration : {get_contractDuration(fileXML)}")
    """publicityDuration"""
    print(f"publicityDuration : {calculate_publicityDuration(fileXML)}")


def check_lotsNumber_empty(cur, tedCanId):
    cur.execute("SELECT COUNT(*) FROM Lots WHERE tedCanId = ? AND lotsNumber IS NULL", (tedCanId,))
    count = cur.fetchone()[0]
    return count == 0


def get_lot_ids(cur, tedCanId):
    cur.execute(f"SELECT lotId FROM Lots WHERE tedCanId = {tedCanId}")
    return [row[0] for row in cur.fetchall()]


def update_lotsNumber_from_xml(conn, cur, tedCanId, lots_numbers_xml):
    lot_ids = get_lot_ids(cur, tedCanId)
    if check_lotsNumber_empty(cur, tedCanId):
        for i in range(0, len(lots_numbers_xml)):
            with open('historique_modifications.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                cur.execute(
                    f"UPDATE Lots SET lotsNumber = {lots_numbers_xml[i]} WHERE tedCanId = {tedCanId} AND lotId = {lot_ids[i]}")
                writer.writerow([tedCanId, '', 'lotsNumber', 'empty', lots_numbers_xml[i]])
            conn.commit()


def calculate_publicityDuration(fileXML):
    try:
        dateReceiptTenders = datetime.strptime(get_dateReceiptTenders(fileXML), '%Y-%m-%d')
        dateDispatchNotice = datetime.strptime(get_dateDispatchNotice(fileXML), '%Y-%m-%d')
        if dateReceiptTenders and dateDispatchNotice:
            return (dateReceiptTenders - dateDispatchNotice).days
        else:
            return None
    except Exception as e:
        return None


def get_dateDispatchNotice(fileXML):
    try:
        tags = get_content_tag(fileXML, "DATE_DISPATCH_NOTICE")
        return str(tags[0].get_text())
    except Exception as e:
        return None


def get_dateReceiptTenders(fileXML):
    try:
        tags = get_content_tag(fileXML, "DATE_RECEIPT_TENDERS")
        return str(tags[0].get_text())
    except Exception as e:
        return None


def get_contractDuration(fileXML):
    try:
        tags = get_content_tag(fileXML, "DURATION")
        return [int(content.get_text()) for content in tags] if tags == [] else None
    except Exception as e:
        return None


def is_renewal(fileXML):
    try:
        tag = get_content_tag(fileXML, "RENEWAL")
        return 1 if tag else 0
    except Exception as e:
        return None


def is_fraAgreement(fileXML):
    try:
        tag = get_content_tag(fileXML, "NOTICE_INVOLVES_DESC")
        fraAgreement = [get_value_tag(content, "VALUE") for content in tag]
        return 1 if fraAgreement[0] == "CONCLUSION_FRAMEWORK_AGREEMENT" else 0
    except Exception as e:
        return None


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
        dates_converties = [datetime.strptime(date, '%d%m%Y').strftime('%Y-%m-%d') for date in results]
        if not dates_converties:
            tags = get_content_tag(fileXML, "CONTRACT_AWARD_DATE")
            dates = [content.get_text() for content in tags]
            formatted_dates = [date.strip().replace('\n', '-') for date in dates]
            dates_converties = [datetime.strptime(date, '%d%m%Y').strftime('%Y-%m-%d') for date in formatted_dates]
            return dates_converties
        return dates_converties
    except Exception as e:
        return None


def is_gpa(fileXML):
    try:
        tag = get_content_tag(fileXML, "RP_REGULATION")
        return 1 if str(tag[0]).lower().count("gpa") else 0
    except Exception as e:
        try:
            tag = get_content_tag(fileXML, "CONTRACT_COVERED_GPA")
            value = get_value_tag(tag[0], "VALUE")
            return 1 if str(value) == "YES" else 0
        except Exception as e2:
            return None
    return None


def get_numberTenders(fileXML):
    try:
        tag = get_content_tag(fileXML, "NB_TENDERS_RECEIVED")
        return int(tag[0].get_text())
    except Exception as e:
        tags = get_content_tag(fileXML, "OFFERS_RECEIVED_NUMBER")
        results = [int(content.get_text()) for content in tags]
        if not results:
            return None
        return results


def get_numberTendersSme(fileXML):
    try:
        tag = get_content_tag(fileXML, "NB_TENDERS_RECEIVED_SME")
        return int(tag[0].get_text())
    except Exception as e:
        return None


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
                return None


def is_accelerated(fileXML):
    try:
        tag = search_tag(fileXML, "ACCELERATED_PROC")
        return 1 if tag else 0
    except Exception as e:
        return None
    return None
