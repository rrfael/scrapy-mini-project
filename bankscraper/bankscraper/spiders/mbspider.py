import scrapy
import json
from bankscraper.items import MetrobankItem

class MbspiderSpider(scrapy.Spider):
    name = "mbspider"
    allowed_domains = ["www.metrobank.com.ph"]
    start_urls = ["https://www.metrobank.com.ph/assets-for-sale/properties?geographicalArea=ALL_OPTIONS"]

    def start_requests(self):
        
        for page in range(1,65):
            yield scrapy.Request(url=f"https://www.metrobank.com.ph/.netlify/functions/ropa-request/assets?page={page}&order=newest&display=12", callback=self.parse)



    def parse(self, response):
        data = json.loads(response.body)

        for item in data["result"]:
            metrobank_item = MetrobankItem()

            metrobank_item["property_id"] = item.get("propAcctNo")
            metrobank_item["property_type"] = item.get("propType")
            metrobank_item["property_class"] = item.get("propClass")
            metrobank_item["property_category"] = item.get("propCategory")
            metrobank_item["province"] = item.get("province")
            metrobank_item["city"] = item.get("city")
            metrobank_item["country"] = item.get("country")
            metrobank_item["zipcode"] = item.get("zipcode")
            metrobank_item["address"] = item.get("address")
            metrobank_item["price"] = item.get("price")
            metrobank_item["lot_area_sqm"] = item.get("lotArea")
            metrobank_item["floor_area_sqm"] = item.get("floorArea")

            yield metrobank_item

