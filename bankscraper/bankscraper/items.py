# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
    # define the fields for your item here like:
    # name = scrapy.Field()
    

class MetrobankItem(scrapy.Item):
    property_id = scrapy.Field()
    property_type = scrapy.Field()
    property_category = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    lot_area_sqm = scrapy.Field()
    floor_area_sqm = scrapy.Field()

class BpiItem(scrapy.Item):
    property_id = scrapy.Field()
    property_type = scrapy.Field()    
    address  = scrapy.Field()
    price = scrapy.Field()    
    area = scrapy.Field() # to be divided into lot_area_sqm & floor_area_sqm
    listing_url = scrapy.Field()

class EastWestbankItem(scrapy.Item):
    property_id = scrapy.Field()
    property_type = scrapy.Field()
    city = scrapy.Field()
    address = scrapy.Field()
    price = scrapy.Field()
    lot_area_sqm = scrapy.Field()
    floor_area_sqm = scrapy.Field()
    listing_url = scrapy.Field()
