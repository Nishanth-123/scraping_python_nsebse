import json

import requests
import constants
import time
import csv
from datetime import *

NSE_DATE_FORMAT = '%d-%b-%Y %H:%M:%S'
DATE_TIME_STD_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

exceptions = []
escapes = '\b\n\r\t\\'
def fetch_data_from_api(startDate, endDate):
    url = "https://www.nseindia.com/api/corporate-announcements?index=equities&from_date="+startDate+"&to_date="+endDate+""
    session = requests.session()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
    }
    try:
        session.get("https://www.nseindia.com/companies-listing/corporate-filings-announcements", headers=headers)
    except Exception as e:
        print(e)

    r = session.get(url, headers=headers)
    # print("Response data from api: " + str(r.status_code))
    # print("Response from api: " + str(r.text))
    try:
        return json.loads(r.text)
    except Exception as e:
        exceptions.append(e)
        return []

def fetchUpdates():
    # date = str(datetime.strptime("2022-10-20 00:00:00.000000","%Y-%m-%d %H:%M:%S.%f").date()).replace('-', '')
    # print(date)
    # response = requests.get(
    #     "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?strPrevDate="+date+"&strScrip=&strSearch=P&strToDate="+date+"&strType=C"
    # )
    #
    # # response = requests.get(
    # #     "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?strPrevDate=20221020&strScrip=&strSearch=P&strToDate=20221020&strType=C"
    # # )
    #
    # print(response.status_code)
    # result = []
    # if response.status_code == int(200):
    #     jsonResponse = response.json()
    #     updates = jsonResponse['Table']
    #     for update in updates:
    #         model = parseFields(update)
    #         result.append(model)
    #
    # print(result)
    # return result

    with open('data/nse_dec_1_to_21_2022_actions.csv', 'a') as file:
        writer = csv.writer(file)
        # writer.writerow(["Type", "Symbol", "Company Name", "Company Isin", "Category",
        #                  "Description", "Exchange Received Time", "Exchange Disseminated Time", "Time Difference",
        #                  "Pdf Attachment"])
        # actionMasterList = []
        # lastMonths = 12
        # # currentMonth = int(date.today().month)
        # # currentYear = int(date.today().year)
        # currentMonth = 11
        # currentYear = 2022
        # while lastMonths > 0:
        #     prevYear = currentYear
        #     prevMonth = currentMonth - 1
        #     if currentMonth == 1:
        #         prevYear = prevYear - 1
        #         prevMonth = 12
        #     endDate = "01-" + f'{currentMonth:02d}' + "-" + str(currentYear)
        #     startDate = "01-" + f'{prevMonth:02d}' + "-" + str(prevYear)
        #     actionList = fetch_data_from_api(startDate, endDate)
        #     for actionItem in actionList:
        #         broadcastTime = datetime.strptime(actionItem["an_dt"], NSE_DATE_FORMAT)
        #         exchangeReceivedTime = broadcastTime
        #         exchangeDisseminatedTime = datetime.strptime(actionItem["exchdisstime"], NSE_DATE_FORMAT)
        #         writer.writerow([
        #             "NSE_CORPORATE_ACTION",
        #             actionItem["symbol"],
        #             actionItem["sm_name"],
        #             actionItem["sm_isin"],
        #             actionItem["desc"],
        #             actionItem["attchmntText"],
        #             exchangeReceivedTime.strftime(DATE_TIME_STD_FORMAT),
        #             exchangeDisseminatedTime.strftime(DATE_TIME_STD_FORMAT),
        #             actionItem["difference"],
        #             actionItem["attchmntFile"]
        #         ])
        #     lastMonths = lastMonths - 1
        #     currentMonth = prevMonth
        #     currentYear = prevYear



        endDate = "21-12-2022"
        startDate = "01-12-2022"
        actionList = fetch_data_from_api(startDate, endDate)
        for actionItem in actionList:
            broadcastTime = datetime.strptime(actionItem["an_dt"], NSE_DATE_FORMAT)
            exchangeReceivedTime = broadcastTime
            exchangeDisseminatedTime = datetime.strptime(actionItem["exchdisstime"], NSE_DATE_FORMAT)
            for c in escapes:
                actionItem["desc"] = actionItem["desc"].replace(c, '')
            writer.writerow([
                "NSE_CORPORATE_ACTION",
                actionItem["symbol"],
                actionItem["sm_name"],
                actionItem["sm_isin"],
                actionItem["desc"],
                actionItem["attchmntText"],
                exchangeReceivedTime.strftime(DATE_TIME_STD_FORMAT),
                exchangeDisseminatedTime.strftime(DATE_TIME_STD_FORMAT),
                actionItem["difference"],
                actionItem["attchmntFile"]
            ])


        print(exceptions)

fetchUpdates()
