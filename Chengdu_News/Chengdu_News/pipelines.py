# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/it~em-pipeline.html

import pymysql
from scrapy.conf import settings
import redis
from scrapy.exceptions import DropItem
import pandas as pd
from .items import ChengduNewsItem, NewsImageItem

redis_db = redis.Redis(host="127.0.0.1", port=6379, db=2)
redis_news_dict = "f_url"
redis_image_dict = "image_url"


class MysqlPipeline(object):

    def __init__(self):
        self.host = settings['MYSQL_HOST']
        self.user = settings['MYSQL_USER']
        self.psd = settings['MYSQL_PASSWORD']
        self.db = settings['MYSQL_DB']
        self.c = settings['CHARSET']
        self.port = settings['MYSQL_PORT']
        self.con = pymysql.connect(host=self.host, user=self.user, passwd=self.psd, db=self.db, charset=self.c, port=self.port)
        redis_db.flushdb()
        if redis_db.hlen(redis_news_dict) == 0:
            sql = "SELECT link FROM News"
            df = pd.read_sql(sql, self.con)
            for link in df['link'].get_values():
                redis_db.hset(redis_news_dict, link, 0)

        if redis_db.hlen(redis_image_dict) == 0:
            sql = "SELECT image_url FROM news_image where image_type = 1"
            df1 = pd.read_sql(sql, self.con)
            for url in df1['image_url'].get_values():
                redis_db.hset(redis_image_dict, url, 0)

    def process_item(self, item, spider):
        if isinstance(item, ChengduNewsItem):
            if redis_db.hexists(redis_news_dict, item['link']):
                raise DropItem("Duplicate book found:%s" % item)
            else:
                cue = self.con.cursor()
                print('mysql connect success')
                try:
                    cue.execute("INSERT INTO News(link,source,content,title,create_time,image_urls) VALUES (%s,%s,%s,%s,%s,%s)",(item['link'],item['source'],item['content'],item['title'],item['create_time'],item['image_urls']))
                    print("Insert success")
                except Exception as e:
                    print("Insert error:", e)
                    self.con.rollback()
                else:
                    self.con.commit()
                return item

        if isinstance(item, NewsImageItem):
            if redis_db.hexists(redis_image_dict, item['image_url']):
                raise DropItem("Duplicate book found:%s" % item)
            else:
                cue = self.con.cursor()
                print('mysql connect success')
                try:
                    cue.execute("INSERT INTO news_image(id,image,image_url,new_image_url,image_type) VALUES (%s,%s,%s,%s,%s)",
                                (item['id'], item['image'], item['image_url'], item['new_image_url'], 1))
                    print("Insert success")
                except Exception as e:
                    print("Insert error:", e)
                    self.con.rollback()
                else:
                    self.con.commit()
                return item






