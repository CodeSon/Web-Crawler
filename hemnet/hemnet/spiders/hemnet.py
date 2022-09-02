from scrapy import signals 
from pkg_resources import yield_lines
from requests import Response
from pydispatch import dispatcher
import scrapy
import json
import time


class HemnetSpider(scrapy.Spider):
    name = "hemnet"
    start_urls = [ 'https://www.hemnet.se/bostader?item_types%5B%5D=radhus&item_types%5B%5D=bostadsratt']

    counter = 0
    results = {}

# When the spider is done crawling, the spider closed method is executed
    def __init__(self):
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def parse(self, response):
        
        #Loop through listings to get ad data
        for advert in response.css("ul.normal-results > li.normal-results__hit > a::attr('href')"):
            #time.sleep(2)
            yield scrapy.Request(url=advert.get(), callback=self.parseInnerPage)

            # checking the next page button if i've reached the end of the inner pages
            nextPage = response.css("a.next_page::attr('href')").get()

            if nextPage is not None:
                #time.sleep(1)
                response.follow(nextPage, self.parse)


            # Sending the extracted links to another parse method
            #Request a new page
    def parseInnerPage(self, response):
       streetName = response.css("h1.property-address_street::text").get()
       price = response.css("p.property-info__price::text").get()
       
       # Removing the currency symbol in the price
       price = price.replace("kr","")
       price = price.replace(u"\xa0","")
       

       attributeData = {}

       for property_attributes in response.css("div.property-attributes > div.property-attributes-table > dl.property-attributes-table__area > div.property-attributes-table__row"):
        property_attribute_label = property_attributes.css("dt.property-attributes-table__label::text").get()

        # Cleaning the data
        if property_attribute_label is not None:
            property_attribute_label = property_attribute_label.replace(u"\n","")
            property_attribute_label = property_attribute_label.replace(u"\t","")
            property_attribute_label = property_attribute_label.strip()
        
        property_attribute_value = property_attributes.css("dd.property-attributes-table__value::text").get()
        if property_attribute_value is not None:
            property_attribute_value = property_attribute_value.replace(u"\n", "")
            property_attribute_value = property_attribute_value.replace(u"\t", "")
            property_attribute_value = property_attribute_value.replace(u"\xa0", "")
            property_attribute_value = property_attribute_value.replace("kr/m²", "")
            property_attribute_value = property_attribute_value.replace("m²", "")
            property_attribute_value = property_attribute_value.replace("kr/år", "")
            property_attribute_value = property_attribute_value.replace("kr/mån", "")
            property_attribute_value = property_attribute_value.strip()
        

        if property_attribute_label is not None:
            attributeData[property_attribute_label] = property_attribute_value
            
            self.results[self.counter]={
                "streetName": streetName,
                "price": price,
                "streetName": streetName,
                "attributeData": attributeData,
            }

            self.counter = self.counter + 1

    def spider_closed(self, spider):
        with open('results.json', 'w') as fp:
            json.dump(self.results, fp)