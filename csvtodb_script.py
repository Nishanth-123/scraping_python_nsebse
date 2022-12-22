import csv

import mysql.connector
import pandas as pd

def start():
    # for reading cs file
    exceptions = []
    with open(r'data/nse_oct_2022_actions.csv') as file_obj:

        # connect to the database
        db = mysql.connector.connect(host="database-1.cluster-cw3dxs47qdds.ap-south-1.rds.amazonaws.com", user="root",
                                     password="bess_321", database="besseggen")
        cursor = db.cursor()

        reader_obj = csv.reader(file_obj)
        for row in reader_obj:
            type = row[0]
            symbol = row[1]
            companyName = row[2]
            companyIsin = row[3]
            category = row[4]
            description = row[5]
            exchangeReceivedTime = row[6]
            exchangeDessiminatedTime = row[7]
            timeDifference = row[8]
            pdfAttachment = row[9]

            checkQuery = '''SELECT EXISTS(SELECT * from corporate_action WHERE type=type AND symbol = symbol AND )'''
            insertQuery = '''INSERT INTO corporate_action (type, symbol, company_name, category, description, exchange_received_time, exchange_disseminated_time, time_difference, pdf_attachment, company_isin) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

            try:

                cursor.execute(insertQuery, (type, symbol, companyName, category, description, exchangeReceivedTime, exchangeDessiminatedTime, timeDifference, pdfAttachment, companyIsin))

                responses = cursor.fetchall()

            except Exception as e:
                exceptions.append(e)


        db.commit()
        db.close()

    print(exceptions)
    print(len(exceptions))





start()