import scrapy
import json
from bankscraper.items import BpiItem


class BpispiderSpider(scrapy.Spider):
    name = "bpispider"
    allowed_domains = ["www.bpi.com.ph"]
    start_urls = ["https://www.bpi.com.ph/group/buenamano/properties-for-sale"]

    def start_requests(self):
        zones = ["ncr", "luzon", "visayas", "mindanao"]

        for zone in zones:
            url = f"https://www.bpi.com.ph/group/buenamano/properties-for-sale/{zone}"
            print(f"THIS IS THE URL {url}")
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        table_rows = response.css("table tr")

        for index in range(2, len(table_rows)):
            bpi_item = BpiItem()
            
            bpi_item["property_id"] = response.xpath(f'//table/tbody/tr[{index}]/td[1]//text()').get().strip()
            bpi_item["address"] = response.xpath(f'//table/tbody/tr[{index}]/td[2]//text()').get().strip()
            bpi_item["area"] = response.xpath(f'//table/tbody/tr[{index}]/td[3]//text()').get().strip()
            bpi_item["price"] = response.xpath(f'//table/tbody/tr[{index}]/td[4]//text()').get().strip()
            bpi_item["property_type"] = response.xpath(f'//table/tbody/tr[{index}]/td[5]//text()').get().strip()
            bpi_item["lister"] = response.xpath(f'//table/tbody/tr[{index}]/td[6]//text()').get().strip()
            
            yield bpi_item
