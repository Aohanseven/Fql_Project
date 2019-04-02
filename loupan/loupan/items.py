# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LoupanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link_id = scrapy.Field()
    estatename = scrapy.Field()
    price = scrapy.Field()
    features = scrapy.Field()
    address =scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    floor = scrapy.Field()
    estate_type = scrapy.Field()
