# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ChengduNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    link = scrapy.Field()
    title = scrapy.Field()
    source = scrapy.Field() #文章出处
    create_time = scrapy.Field()
    content = scrapy.Field()
    image_urls = scrapy.Field()


class NewsImageItem(scrapy.Item):
    image = scrapy.Field()
    image_url = scrapy.Field()
    id = scrapy.Field()
    new_image_url = scrapy.Field()
    image_type = scrapy.Field()

