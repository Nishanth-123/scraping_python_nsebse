import json

import requests
import math
import csv
import constants
import time
from datetime import *

BSE_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'
BSE_DATE_FORMAT2 = '%Y-%m-%dT%H:%M:%S'
DATE_TIME_STD_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
START_DATE_FOR_SYNC = '2022-10-01 00:00:00.000000'
DEFAULT_TIME_DIFFERENCE = "00:00:00"

# https://www.bseindia.com/xml-data/corpfiling/AttachLive/a76c2d66-2a7f-4108-a0f4-f5fa5946fd58.pdf
PDF_BASE_URL = "https://www.bseindia.com/xml-data/corpfiling/AttachLive/"

# https://www.bseindia.com/Msource/90D/CorpXbrlGen.aspx?Bsenewid=3c610263-f780-4671-a2a6-3e32c8edc380&Scripcode=524687
XBRL_BASE_URL = "https://www.bseindia.com/Msource/90D/CorpXbrlGen.aspx"


exceptions = []
escapes = '\b\n\r\t\\'
def fetch_data_from_api(pageno, startDate, endDate):
    url = "https://api.bseindia.com/BseIndiaAPI/api/AnnGetData/w?pageno=" + str(
        pageno) + "&strPrevDate=" + startDate + "&strScrip=&strSearch=P&strToDate=" + endDate + "&strType=C"

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

    r = requests.get(url, headers=headers)
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

    scripToDetails = {}
    scripFile = open('/Users/ashwanirai/Downloads/SCRIP/BSE_EQ_SCRIP_28102022.csv')
    scripReader = csv.reader(scripFile)
    for row in scripReader:
        if len(row) >= 5:
            scripToDetails[row[0]] = [row[1], row[4]]
    scripFile.close()
    with open('data/bse_nov_2021_actions.csv', 'a') as file:
        writer = csv.writer(file)
        # writer.writerow(["Type", "Symbol", "Company Name", "Category", "Description", "Exchange Received Time",
        #                  "Exchange Disseminated Time", "Time Difference", "Pdf Attachment", "XBRL Attachment",
        #                  "Announcement Type", "Company Isin", "Company Stocks Url"])










        endDate = '20211112'
        startDate = '20211101'
        data = fetch_data_from_api(1, startDate, endDate)
        if "Table" not in data:
            exceptions.append("could not fetch 1st page from " + startDate + " to " + endDate)
            return
        pageNums = math.ceil(data["Table1"][0]["ROWCNT"] / 50)
        for i in range(pageNums):
            data = fetch_data_from_api(i + 1, startDate, endDate)
            if "Table" not in data:
                exceptions.append("could not fetch " + str(i+1) + " page from " + startDate + " to "+ endDate)
                continue
            actionList = data["Table"]
            # Filter only new actions and then append those in masterList
            for actionItem in actionList:
                if actionItem["News_submission_dt"] is not None:
                    try:
                        broadcastTime = datetime.strptime(actionItem["News_submission_dt"], BSE_DATE_FORMAT2)
                    except:
                        broadcastTime = datetime.strptime(actionItem["News_submission_dt"], BSE_DATE_FORMAT)
                else:
                    try:
                        broadcastTime = datetime.strptime(actionItem["NEWS_DT"], BSE_DATE_FORMAT)
                    except:
                        broadcastTime = datetime.strptime(actionItem["NEWS_DT"], BSE_DATE_FORMAT2)

                pdfAttachment = PDF_BASE_URL + actionItem["ATTACHMENTNAME"]
                xbrlAttachment = XBRL_BASE_URL + "?Bsenewid=" + actionItem["NEWSID"] + "&Scripcode=" + str(
                    actionItem["SCRIP_CD"])

                exchangeReceivedTime = broadcastTime
                if actionItem["DissemDT"] is not None:
                    try:
                        exchangeDisseminatedTime = datetime.strptime(actionItem["DissemDT"], BSE_DATE_FORMAT)
                    except:
                        exchangeDisseminatedTime = datetime.strptime(actionItem["DissemDT"], BSE_DATE_FORMAT2)
                else:
                    exchangeDisseminatedTime = None

                scrip_cd = str(actionItem["SCRIP_CD"])

                if scrip_cd in scripToDetails:
                    symbol = scripToDetails[scrip_cd][0]
                    isin = scripToDetails[scrip_cd][1]
                else:
                    symbol = None
                    isin = None

                for c in escapes:
                    actionItem["NEWSSUB"] = actionItem["NEWSSUB"].replace(c, '')

                writer.writerow([
                    "BSE_CORPORATE_ACTION",
                    symbol,
                    actionItem["SLONGNAME"],
                    actionItem["CATEGORYNAME"],
                    actionItem["NEWSSUB"],
                    exchangeReceivedTime.strftime(DATE_TIME_STD_FORMAT) if exchangeReceivedTime is not None else None,
                    exchangeDisseminatedTime.strftime(DATE_TIME_STD_FORMAT) if exchangeDisseminatedTime is not None else None,
                    actionItem["TimeDiff"] if actionItem[
                                                  "TimeDiff"] is not None else DEFAULT_TIME_DIFFERENCE,
                    pdfAttachment,
                    xbrlAttachment,
                    actionItem["ANNOUNCEMENT_TYPE"],
                    isin,
                    actionItem["NSURL"]
                ])









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
        #     endDate = str(currentYear) + f'{currentMonth:02d}' + "01"
        #     startDate = str(prevYear) + f'{prevMonth:02d}' + "01"
        #     data = fetch_data_from_api(1, startDate, endDate)
        #     if "Table" not in data:
        #         continue
        #     pageNums = math.ceil(data["Table1"][0]["ROWCNT"] / 50)
        #     for i in range(pageNums):
        #         data = fetch_data_from_api(i + 1, startDate, endDate)
        #         if "Table" not in data:
        #             continue
        #         actionList = data["Table"]
        #         # Filter only new actions and then append those in masterList
        #         for actionItem in actionList:
        #             if actionItem["News_submission_dt"] is not None:
        #                 try:
        #                     broadcastTime = datetime.strptime(actionItem["News_submission_dt"], BSE_DATE_FORMAT2)
        #                 except:
        #                     broadcastTime = datetime.strptime(actionItem["News_submission_dt"], BSE_DATE_FORMAT)
        #             else:
        #                 try:
        #                     broadcastTime = datetime.strptime(actionItem["NEWS_DT"], BSE_DATE_FORMAT)
        #                 except:
        #                     broadcastTime = datetime.strptime(actionItem["NEWS_DT"], BSE_DATE_FORMAT2)
        #
        #             pdfAttachment = PDF_BASE_URL + actionItem["ATTACHMENTNAME"]
        #             xbrlAttachment = XBRL_BASE_URL + "?Bsenewid=" + actionItem["NEWSID"] + "&Scripcode=" + str(
        #                 actionItem["SCRIP_CD"])
        #
        #             exchangeReceivedTime = broadcastTime
        #             try:
        #                 exchangeDisseminatedTime = datetime.strptime(actionItem["DissemDT"], BSE_DATE_FORMAT)
        #             except:
        #                 exchangeDisseminatedTime = datetime.strptime(actionItem["DissemDT"], BSE_DATE_FORMAT2)
        #
        #             scrip_cd = str(actionItem["SCRIP_CD"])
        #
        #             if scrip_cd in scripToDetails:
        #                 symbol = scripToDetails[scrip_cd][0]
        #                 isin = scripToDetails[scrip_cd][1]
        #             else:
        #                 symbol = None
        #                 isin = None
        #
        #             for c in escapes:
        #                 actionItem["NEWSSUB"] = actionItem["NEWSSUB"].replace(c, '')
        #
        #             writer.writerow([
        #                 "BSE_CORPORATE_ACTION",
        #                 symbol,
        #                 actionItem["SLONGNAME"],
        #                 actionItem["CATEGORYNAME"],
        #                 actionItem["NEWSSUB"],
        #                 exchangeReceivedTime.strftime(DATE_TIME_STD_FORMAT),
        #                 exchangeDisseminatedTime.strftime(DATE_TIME_STD_FORMAT),
        #                 actionItem["TimeDiff"] if actionItem[
        #                                               "TimeDiff"] is not None else DEFAULT_TIME_DIFFERENCE,
        #                 pdfAttachment,
        #                 xbrlAttachment,
        #                 actionItem["ANNOUNCEMENT_TYPE"],
        #                 isin,
        #                 actionItem["NSURL"]
        #             ])
        #
        #     print('fetched data for the month ' + currentMonth)
        #     lastMonths = lastMonths - 1
        #     currentMonth = prevMonth
        #     currentYear = prevYear


    file.close()
    print(exceptions)
    print("Succeeded")



fetchUpdates()
