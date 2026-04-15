# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg
from bankscraper.items import MetrobankItem, BpiItem, EastWestbankItem


class PostgreSQLPipeline:
    def open_spider(self, spider):
        self.conn = psycopg.connect(
            host="localhost",
            dbname="scrapy_db",
            user="postgres",
            password="root@postgres"
        )
        
        self.cur = self.conn.cursor()

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                property_id VARCHAR(25) NOT NULL PRIMARY KEY,
                bank_property_id VARCHAR(25),
                property_type VARCHAR(55),
                city VARCHAR(55),
                address TEXT,
                price DECIMAL DEFAULT 0,
                lot_area_sqm DECIMAL DEFAULT 0,
                floor_area_Sqm DECIMAL DEFAULT 0,
                listed_on VARCHAR(25),
                listing_url TEXT
            );
        """)

        self.count = 0
        
        self.conn.commit()



    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        self.count += 1
        formatted_id = f"P{self.count:06d}" 
        
        try:
            if isinstance(item, MetrobankItem):
# METROBANK
                listed_on = "Metrobank"

                # combine property type and property category
                property_type_raw = adapter.get('property_type', '')
                property_category_raw = adapter.get('property_category', '')
                property_type = f"{property_category_raw}-{property_type_raw}"

                # format each listing with respective page
                page_id = adapter.get('property_id')
                item_url = f"https://www.metrobank.com.ph/assets-for-sale/properties/details?id={page_id}"

                self.cur.execute("""
                    INSERT INTO properties(property_id, bank_property_id, property_type, city, address, price, lot_area_sqm, floor_area_sqm, listed_on, listing_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    formatted_id,
                    item.get("property_id"),
                    property_type,
                    item.get("city"),
                    item.get("address"),
                    item.get("price"),
                    item.get("lot_area_sqm"),
                    item.get("floor_area_sqm"),
                    listed_on,
                    item_url
                ))
            elif isinstance(item, BpiItem):
# BPI
                listed_on = "BPI"
                city = "unknown"
                
    # Processes for bpi data
                def safe_split(text, sep, index):
                    if not text or sep not in text:
                        return text if index == 0 else None
                    parts = text.split(sep)
                    return parts[index].strip() if len(parts) > index else None
                
            # Process Property Types
                pt_raw = adapter.get('property_type', '')
                property_type = safe_split(pt_raw, '-', 0)

            # Process Address
                address_raw = adapter.get('address', '')
                address_split = address_raw.split()
                for i in address_split:
                    if i == "City":
                        item_index = address_split.index(i)
                        city = address_split[item_index - 1] + " " + address_split[item_index]

            # Process Areas
                area_raw = adapter.get('area', '')
                lot_area_sqm = safe_split(area_raw, '/', 0) or 0
                floor_area_sqm = safe_split(area_raw, '/', 1) or 0

            # Clean Price (Removes PHP and commas)
                price_raw = adapter.get('price', '0')
                price = price_raw.replace('PHP', '').replace(',', '').strip() or 0


                self.cur.execute("""
                    INSERT INTO properties(property_id, bank_property_id, property_type, city, address, price, lot_area_sqm, floor_area_sqm, listed_on, listing_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """,(
                    formatted_id,
                    item.get("property_id"),
                    property_type,
                    city,
                    item.get("address"),
                    price,
                    lot_area_sqm,
                    floor_area_sqm,
                    listed_on,
                    item.get("listing_url")
                ))
            
            elif isinstance(item, EastWestbankItem):
# EASTWESTBANK
                listed_on = "EastWestBank"

                # format each listing with respective page
                page_url = adapter.get('listing_url')
                item_url = f"https://pre-owned-properties.eastwestbanker.com" + page_url

                # remove commas from price values
                price_raw = adapter.get('price', '')
                price = price_raw.replace(',', '').strip()

                self.cur.execute("""
                    INSERT INTO properties(property_id, bank_property_id, property_type, city, address, price, lot_area_sqm, floor_area_sqm, listed_on, listing_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                    formatted_id,
                    item.get("property_id"),
                    item.get("property_type"),
                    item.get("city"),
                    item.get("address"),
                    price,
                    item.get("lot_area_sqm"),
                    item.get("floor_area_sqm"),
                    listed_on,
                    item_url
                    ))
            
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            spider.logger.error(f"DATABASE ERROR: {str(e)} | ITEM: {item.get('property_id')}")
        return item

    def close_spider(self, spider=None):
        self.cur.close()
        self.conn.close()