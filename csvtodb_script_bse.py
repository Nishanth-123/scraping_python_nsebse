import csv

import mysql.connector
import pandas as pd


def start():
    # for reading cs file
    exceptions = []
    rowCount = 0
    with open(r'data/bse_last_one_year_actions.csv') as file_obj:

        # connect to the database
        db = mysql.connector.connect(host="database-1.cluster-cw3dxs47qdds.ap-south-1.rds.amazonaws.com", user="root",
                                     password="bess_321", database="besseggen")
        cursor = db.cursor()

        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            type = row[0]
            symbol = row[1]
            companyName = row[2]
            category = row[3]
            description = row[4]
            exchangeReceivedTime = row[5]
            exchangeDessiminatedTime = row[6]
            timeDifference = row[7]
            pdfAttachment = row[8]
            xbrlAttachment = row[9]
            announcementType = row[10]
            companyIsin = row[11]
            companyStocksUrl = row[12]

            checkQuery = '''SELECT EXISTS(SELECT * from corporate_action WHERE type=type AND symbol = symbol AND )'''
            insertQuery = '''INSERT INTO corporate_action (type, symbol, company_name, category, description, exchange_received_time, exchange_disseminated_time, time_difference, pdf_attachment, xbrl_attachment, announcement_type, company_isin, company_stocks_url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

            try:

                cursor.execute(insertQuery, (
                type, symbol, companyName, category, description, exchangeReceivedTime, exchangeDessiminatedTime,
                timeDifference, pdfAttachment, xbrlAttachment, announcementType, companyIsin, companyStocksUrl))

                responses = cursor.fetchall()

            except Exception as e:
                exceptions.append(e)

            rowCount += 1

        db.commit()
        db.close()

    print("exceptions : ", len(exceptions), exceptions)
    print("rows : ", rowCount)


start()
