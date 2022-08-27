from pkg_resources import yield_lines
from requests import Response
import scrapy


class HemnetSpider(scrapy.Spider):
    name = "hemnet"
    start_urls = [ 'https://www.hemnet.se/bostader?item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt']

    def parse(self, response):
        
        #Loop through listings to get ad data
        for advert in response.css("ul.normal-results > li.normal-results__hit > a::attr('href')"):
            yield scrapy.Request(url=advert.get(), callback=self.parseInnerPage)

            # Sending the extracted links to another parse method
            #Request a new page
    def parseInnerPage(self, response):
        print(response.text)
        
        