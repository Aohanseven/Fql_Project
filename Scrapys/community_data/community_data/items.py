# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CommunityDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    price = scrapy.Field()
    community_type = scrapy.Field()
    create_year = scrapy.Field()
    total_area = scrapy.Field()
    plot_ratio = scrapy.Field()
    developers = scrapy.Field()
    property = scrapy.Field()
    peripheral_school = scrapy.Field()
    property_price = scrapy.Field()
    households_number = scrapy.Field()
    parking_space = scrapy.Field()
    green = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()

