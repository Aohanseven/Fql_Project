# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import redis,pymysql
from scrapy.exceptions import DropItem
import pandas as pd

redis_db = redis.Redis(host='127.0.0.1',port=6379,db=12)
redis_data_dict = "FTX_shops_id"

class DiplicatesPipeline(object):

    con = pymysql.connect(host='127.0.0.1',user='root', passwd='a2577811', db='anjuke', charset='utf8', port=3306)

    def __init__(self):
        redis_db.flushdb()
        if redis_db.hlen(redis_data_dict) == 0:
            sql= "SELECT id FROM FTXshop_data"
            df = pd.read_sql(sql, self.con)
            for id in df['id'].get_values():
                redis_db.hset(redis_data_dict,id,0)

    def process_item(self,item,spider):
       if redis_db.hexists(redis_data_dict,item['id']):
           raise  DropItem("Duplicate book found:%s" % item)
       return item

class DbPipeline(object):
    def process_item(self,item,spider):
        con = pymysql.connect(host='127.0.0.1', user='root', passwd='a2577811', db='anjuke',charset='utf8', port=3306)
        cue=con.cursor()
        print('mysql content succes')
        try:
            cue.execute("INSERT INTO FTXshop_data(id,title,link) VALUES (%s,%s,%s)",(item['id'],item['title'],item['link']))
            print("insert succes")
        except Exception as e:
            print('insert error:',e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item
