# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WubaurlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()


class Data58ShopItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    title = scrapy.Field()
    monthly_rent = scrapy.Field()
    acreage = scrapy.Field()
    width = scrapy.Field()
    address = scrapy.Field()
    depth = scrapy.Field()
    height = scrapy.Field()
    floor = scrapy.Field()
    shop_type = scrapy.Field()
    store_status = scrapy.Field()
    business_industry = scrapy.Field()
    payment_method = scrapy.Field()
    lease_mode = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    is_ok = scrapy.Field()
    content = scrapy.Field()