import scrapy
import json
from bankscraper.items import MetrobankItem, BpiItem, EastWestbankItem

class BankspiderSpider(scrapy.Spider):
    name = "bankspider"
    allowed_domains = ["www.metrobank.com.ph", "www.bpi.com.ph", "pre-owned-properties.eastwestbanker.com"]
    start_urls = ["https://www.metrobank.com.ph/assets-for-sale/properties?geographicalArea=ALL_OPTIONS", "https://www.bpi.com.ph/group/buenamano/properties-for-sale", "https://pre-owned-properties.eastwestbanker.com/"]


    def start_requests(self):
# METROBANK
        for page in range(1, 65):
            yield scrapy.Request(url=f"https://www.metrobank.com.ph/.netlify/functions/ropa-request/assets?page={page}&order=newest&display=12", callback=self.parse_metrobank)

# BPI        
        zones = ["ncr", "luzon", "visayas", "mindanao"]

        for zone in zones:
            yield scrapy.Request(url=f"https://www.bpi.com.ph/group/buenamano/properties-for-sale/{zone}", callback=self.parse_bpi)

# EASTWESTBANK
        yield scrapy.Request(url="https://pre-owned-properties.eastwestbanker.com/", callback=self.parse_eastwestbank)



# PARSE DATA
    def parse_metrobank(self, response):
        data = json.loads(response.body)

        for item in data["result"]:

            metrobank_item = MetrobankItem()

            metrobank_item["property_id"] = item.get("propAcctNo")
            metrobank_item["property_type"] = item.get("propClass")
            metrobank_item["property_category"] = item.get("propCategory")
            metrobank_item["city"] = item.get("city")
            metrobank_item["address"] = item.get("address")
            metrobank_item["price"] = item.get("price")
            metrobank_item["lot_area_sqm"] = item.get("lotArea")
            metrobank_item["floor_area_sqm"] = item.get("floorArea")

            yield metrobank_item


    def parse_bpi(self, response):
        table_rows = response.css("table tr")

        for index in range(2, len(table_rows)):
            bpi_item = BpiItem()
            
            bpi_item["property_id"] = response.xpath(f'//table/tbody/tr[{index}]/td[1]//text()').get().strip()
            bpi_item["property_type"] = response.xpath(f'//table/tbody/tr[{index}]/td[5]//text()').get().strip()
            bpi_item["address"] = response.xpath(f'//table/tbody/tr[{index}]/td[2]//text()').get().strip()
            bpi_item["area"] = response.xpath(f'//table/tbody/tr[{index}]/td[3]//text()').get().strip()
            bpi_item["price"] =  response.xpath(f'//table/tbody/tr[{index}]/td[4]//text()').get().strip()
            bpi_item["listing_url"] = response.url
            yield bpi_item

    
    def parse_eastwestbank(self, response):
        item_list = response.css('.content_card')

        for item in item_list:
            ewb_item = EastWestbankItem()

            ewb_item["property_id"] = item.css('[fs-cmssort-field="item"]::text').get()
            ewb_item["property_type"] = item.css('[fs-cmsfilter-field="property type"]::text').get()
            ewb_item["city"] = item.css('[fs-cmssort-field="city"]::text').get()
            ewb_item["address"] = item.css('[fs-cmssort-field="location"]::text').get()
            ewb_item["price"] = item.css('[fs-cmssort-field="price"]::text').get()
            ewb_item["lot_area_sqm"] = item.css('[fs-cmssort-field="lotarea"]::text').get()
            ewb_item["floor_area_sqm"] = item.css('[fs-cmssort-field="floorarea"]::text').get()
            ewb_item["listing_url"] = item.css('[class="btn_inquire w-button"]::attr(href)').get()
            yield ewb_item

        next_page = response.css('[aria-label="Next Page"]::attr(href)').get()

        next_page_url=  f"https://pre-owned-properties.eastwestbanker.com/{next_page}"

        yield response.follow(url=next_page_url, callback=self.parse_eastwestbank)
