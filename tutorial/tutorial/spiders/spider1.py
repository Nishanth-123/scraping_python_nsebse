import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'announcements'

    start_urls = ["https://www.bseindia.com/corporates/ann.html"]

    # def start_requests(self):
    #     # url=['https://www.bseindia.com/corporates/ann.html',
    #     #       'http://quotes.toscrape.com/page/2/']
    #     # for url in urls:
    #     url = "https://www.bseindia.com/corporates/ann.html"
    #     yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for dataTable in response.xpath('//table[@ng-show="CorpannData.Table.length"]'):
            dataRow = dataTable.css('tr')
            columns = dataRow.css('td .tdcolumngrey')
            yield {
                'name': columns.xpath('[@width="70%"]/a/text()').get(),
                'updateType': columns.xpath('[')
            }


        # greyColumns = response.css('td .tdcolumngrey')
        # print(len(greyColumns))
        # rows = len(greyColumns) // 4
        # for i in range(rows):
        #     row = int(4 * i)
        #     yield {
        #         'name': greyColumns[row].css('a::text').get(),
        #         'type': greyColumns[row + 1].css('::text').get(),
        #         'pdfUrl': greyColumns[row + 2].xpath('.//a/@href').get(),
        #         'xbrl': greyColumns[row+3].css('a::text').get()
        #     }

        # for announcement in response.css('div.quote'):
        # for announcement in response.css('table .ng-scope'):
        #     yield {
        #         'rows':announcement.css('tbody tr').getAll()
        #     }
        #     # rows = announcement.css('tbody tr').getAll()
        #     # firstRowData = rows[0].css('td.tdcolumngrey').getAll()
        #     # yield {
        #     #     'url': firstRowData[0].css('::text').get(),
        #     #     'name' : firstRowData[1].css('::text').get(),
        #     #     'pdfUrl' : firstRowData[2].css('a.tablebluelink::text').get(),
        #     #     'xbrl':firstRowData[3].css('a::text').get()
        #     # }

        # print(response.url)
        # filename = 'announcements.html'
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('saved file %s' % filename)

        # print(response)
        # page = response.url.split["/"][-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('saved file %s' % filename)
