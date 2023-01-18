import csv

import mysql.connector
import pandas as pd

def start(year, month, fromDate, toDate):
    # for reading cs file
    exceptions = []
    db = mysql.connector.connect(host="database-1.cluster-cw3dxs47qdds.ap-south-1.rds.amazonaws.com", user="root",
                                 password="bess_321", database="besseggen")
    cursor = db.cursor()
    for x in range(fromDate, toDate+1):
        yearStr = f'{year:04d}'
        monthStr = f'{month:02d}'
        dateStr = f'{x:02d}'
        queryDate = f"{yearStr}-{monthStr}-{dateStr}"
        fetchQuery = f'''SELECT * from corporate_action where exchange_received_time like "{queryDate}%"'''
        with open(f'data/CSVsFromDb/aug-2021/{queryDate}.csv', 'w') as file:
            writer = csv.writer(file)
            writer.writerow(["type", "symbol", "company_name", "category", "description", "exchange_received_time",
                             "exchange_disseminated_time", "time_difference", "pdf_attachment",
                             "xbrl_attachment", "announcement_type", "company_industry", "company_isin", "company_stocks_url",
                             "price_current", "price_5_min_before", "price_5_min_after", "price_15_min_after", "price_30_min_after",
                             "tags", "trading_holiday", "off_timing"
                             ])
            dayExceptions = [queryDate]
            try:
                cursor.execute(fetchQuery)
                responses = cursor.fetchall()
                for response in responses:
                    row = []
                    for index in range(1, len(response)-1):
                        row.append(response[index])
                    writer.writerow(row)
                    #
                    # writer.writerow(
                    #     [response[1], response[2], response[3], response[4], response[5], response[6],
                    #      response[7], response[8], response[9], response[10], response[11],
                    #      response[12], response[13], response[14],
                    #      response[15], response[16], response[17], response[18],
                    #      response[19],
                    #      response[20], response[21], response[22]
                    #      ])

            except Exception as e:
                dayExceptions.append(e)

        exceptions.append(dayExceptions)

    db.commit()
    db.close()


    print(exceptions)
    print(len(exceptions))




start(2021, 8, 1, 31)