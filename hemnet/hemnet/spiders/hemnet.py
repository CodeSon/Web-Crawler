from requests import Response
import scrapy


class HemnetSpider(scrapy.Spider):
   
    name = "hemnet"
    start_urls = [ 'https://www.hemnet.se/bostader?item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt']

    def parse(self, response):
        print(response.text)
        