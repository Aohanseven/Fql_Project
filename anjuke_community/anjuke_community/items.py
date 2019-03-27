# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AnjukeCommunityItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    link = scrapy.Field()
    address = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """INSERT INTO anjuke_community(id, title, link )VALUES(%s, %s, %s)"""
        params = (self['id'],self['title'],self['link'])
        return insert_sql, params