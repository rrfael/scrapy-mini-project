import scrapy
from bankscraper.items import EastWestbankItem

class EwbspiderSpider(scrapy.Spider):
    name = "ewbspider"
    allowed_domains = ["pre-owned-properties.eastwestbanker.com"]
    start_urls = ["https://pre-owned-properties.eastwestbanker.com/"]

    def start_requests(self):
        yield scrapy.Request(url="https://pre-owned-properties.eastwestbanker.com/", callback=self.parse)


    def parse(self, response):
        item_list = response.css('.content_card')

        for item in item_list:
            ewb_item = EastWestbankItem()

            ewb_item["property_id"] =       item.css('[fs-cmssort-field="item"]::text').get()
            ewb_item["property_type"] =     item.css('[fs-cmsfilter-field="property type"]::text').get()
            ewb_item["lot_area_sqm"] =      item.css('[fs-cmssort-field="lotarea"]::text').get()
            ewb_item["floor_area_sqm"] =    item.css('[fs-cmssort-field="floorarea"]::text').get()
            ewb_item["location"] =          item.css('[fs-cmssort-field="location"]::text').get()
            ewb_item["city"] =              item.css('[fs-cmssort-field="city"]::text').get()
            ewb_item["price"] =             item.css('[fs-cmssort-field="price"]::text').get()
            ewb_item["lister_email"] =      item.xpath('//*[@id="wf-form-filter"]/div/div/div/div[2]/div[2]/div[2]/a/text()').get()
            ewb_item["lister_phone_num"] =  item.css('.text-block-40::text').get()

            yield ewb_item

        next_page = response.css('[aria-label="Next Page"]::attr(href)').get()

        next_page_url=  f"https://pre-owned-properties.eastwestbanker.com/{next_page}"
        print(f"PAGE {next_page} NOW")

        yield response.follow(url=next_page_url, callback=self.parse)
