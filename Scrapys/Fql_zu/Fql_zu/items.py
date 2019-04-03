# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UrlItem(scrapy.Item):
    id = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()


class ShopsSpiderItem(scrapy.Item):
    id = scrapy.Field()
    monthly_rent = scrapy.Field()
    transfer_fee= scrapy.Field()
    property_fee = scrapy.Field()
    acreage = scrapy.Field()
    width = scrapy.Field()
    address = scrapy.Field()
    depth = scrapy.Field()
    height = scrapy.Field()
    store_status = scrapy.Field()
    floor = scrapy.Field()
    people = scrapy.Field()
    payment_method = scrapy.Field()
    lease_term = scrapy.Field()
    is_facestreet = scrapy.Field()
    lng = scrapy.Field()
    lat = scrapy.Field()
    is_ok = scrapy.Field()
    content = scrapy.Field()
    business_industry = scrapy.Field()
    image_urls = scrapy.Field()
    agent_name = scrapy.Field()
    agent_phone = scrapy.Field()

class ImagesItem(scrapy.Item):
    image = scrapy.Field()
    image_url = scrapy.Field()
    image_id = scrapy.Field()