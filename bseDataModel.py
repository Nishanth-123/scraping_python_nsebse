
class BSEDataModel:
    pdfBaseUrl = "https://www.bseindia.com/xml-data/corpfiling/AttachLive/"
    xbrlBaseUrl = "https://www.bseindia.com/Msource/90D/CorpXbrlGen.aspx"

    def __init__(self, newsId:str, scripCd:str, newsSub:str, attachmentName:str, categoryName:str, headline:str):
        self.newsId = newsId
        self.scripCd = scripCd
        self.newsSub = newsSub
        self.attachmentName = attachmentName
        self.categoryName = categoryName
        self.headline = headline

    def pdfUrl(self):
        url = self.pdfBaseUrl + self.attachmentName
        return url

    def xbrlUrl(self):
        url = self.xbrlBaseUrl+str("?Bsenewid=")+self.newsId+str("&Scripcode=")+self.scripCd
        return url

    def subject(self):
        return self.newsSub

    def category(self):
        return self.categoryName

