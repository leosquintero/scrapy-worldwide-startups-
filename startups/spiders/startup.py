from scrapy import Spider
from ..items import StartupsItem
import scrapy
import re 

class StartupsSpider(Spider):
    name = "startups"
    allowed_domains = ['www.startupranking.com']
    # Defining the list of pages to scrape
    start_urls = ['https://www.startupranking.com/top'] + ['https://www.startupranking.com/top/0/' + str(1 * i)  for i in range(0, 3)]

    def parse(self, response):
        rows = response.xpath('//tr')
        for row in rows:
            name = row.xpath('.//td/div/a/text()').extract_first()
            country = row.xpath('.//td/a/img/@title').extract_first()
            
            item = StartupsItem()
            item['name'] = name
            item['country'] = country
            yield scrapy.Request(link,
                                 callback=self.parse_detail,
                                 meta={'item': item})

        

    def parse_detail(self, response):
        item = response.meta['item']
        link = response.xpath('/html/body/div[5]/section[1]/div[3]/h2/a')
        yield item