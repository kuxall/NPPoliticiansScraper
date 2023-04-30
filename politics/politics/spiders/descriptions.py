import scrapy
import csv
from politics.items import PoliticsItem

class WikiSpider(scrapy.Spider):
    name = 'wiki'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['https://en.wikipedia.org/wiki/List_of_Nepalese_politicians']

    def parse(self, response):
        urls = response.css('div.div-col li a:not([href^="#"])::attr(href)').getall()

        for url in urls:
            yield scrapy.Request(f'https://en.wikipedia.org{url}', callback=self.parse_description)

    def parse_description(self, response):
        title = response.css('#firstHeading > span::text').get()
        description = response.css('#mw-content-text > div.mw-parser-output > p::text').get()

        # yield {
        #     'title': title,
        #     'url': response.url,
        #     'description': description
        # }

        # Extracting descriptions of individual politicians
        for politician_url in response.css('#mw-content-text > div.mw-parser-output > ul > li > a::attr(href)').getall():
            yield scrapy.Request(f'https://en.wikipedia.org{politician_url}', callback=self.parse_politician_description)

    def parse_politician_description(self, response):
        title = response.css('#firstHeading > span::text').get()
        description = response.css('#mw-content-text > div.mw-parser-output > p::text').get()

        yield {
            'title': title,
            'url': response.url,
            'description': description
        }
