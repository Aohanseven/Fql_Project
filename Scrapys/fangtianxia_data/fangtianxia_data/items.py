# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FangtianxiaDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    monthly_rent = scrapy.Field()
    acreage = scrapy.Field()
    width = scrapy.Field()
    address = scrapy.Field()
    depth = scrapy.Field()
    height = scrapy.Field()
    floor = scrapy.Field()
    shop_type = scrapy.Field()
    business_industry = scrapy.Field()
    payment_method = scrapy.Field()
    renovation = scrapy.Field()
    property_fee = scrapy.Field()
    estate = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()