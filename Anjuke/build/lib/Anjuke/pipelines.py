# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import redis
import pandas as pd
from scrapy.conf import settings
from scrapy.exceptions import DropItem

redis_db =redis.Redis(host='127.0.0.1', port=6379, db=1)
redis_data_dict = "anjuke_shopid"


# 通过redis进行去重
class DiplicatesPipeline(object):
    host = settings['MYSQL_HOSTS']
    user = settings['MYSQL_USER']
    psd = settings['MYSQL_PASSWORD']
    db = settings['MYSQL_DB']
    c = settings['CHARSET']
    port = settings['MYSQL_PORT']
    con = pymysql.connect(host='192.168.0.252', user='web_user', passwd='first2018pl,', db='FBDdata2', charset='utf8',
                          port=3306)
    def __init__(self):
        redis_db.flushdb()
        if redis_db.hlen(redis_data_dict) == 0:
            sql = "SELECT id FROM anjuke_shop_data"
            df = pd.read_sql(sql, self.con)
            for id in df['id'].get_values():
                redis_db.hset(redis_data_dict, id, 0)

    def process_item(self, item, spider):
        if redis_db.hexists(redis_data_dict, item['id']):
            raise DropItem("Duplicate book found:%s" % item)

        return item


# 存入mysql数据库
class URLDBPipeline(object):

    def process_item(self, item, spider):
        con = pymysql.connect(host='192.168.0.252', user='web_user', passwd='first2018pl,', db='FBDdata2',
                              charset='utf8',
                              port=3306)
        cue=con.cursor()
        print("mysql connect succes")
        try:
            cue.execute("INSERT INTO anjuke_shop_data(id,link,title) VALUES (%s,%s,%s)",(item['id'],item['link'],item['title']))
            print("Insert success")
        except Exception as e:
            print("Insert error:", e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item


class DATADBPiplines(object):

    def process_item(self, item, spider):
        con = pymysql.connect(host='192.168.0.252', user='web_user', passwd='first2018pl,', db='FBDdata2',
                              charset='utf8',
                              port=3306)
        cue = con.cursor()
        print("mysql connect succes")
        try:
            cue.execute("UPDATE anjuke_shop_data SET is_ok='%s',monthly_rent='%s',transfer_fee='%s',property_fee='%s',acreage='%s',width='%s',address='%s',depth='%s',height='%s',store_status='%s',floor='%s',people='%s',is_facestreet='%s',lease_term='%s',payment_method='%s',lat='%s',lng='%s',content ='%s',business_industry='%s' WHERE id='%s'"
                        % (item['is_ok'],item['monthly_rent'],item['transfer_fee'],item['property_fee'],item['acreage'],item['width'],item['address'],item['depth'],item['height'],item['store_status'],item['floor'],item['people'],item['is_facestreet'],item['lease_term'],item['payment_method'],item['lat'],item['lng'],item['content'], item['business_industry'],item['id']))
            print("Update success")
        except Exception as e:
            print("Update error:",e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item