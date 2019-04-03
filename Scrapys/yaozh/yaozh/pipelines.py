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

redis_db = redis.Redis(host='127.0.0.1', port=6379, db=4)
redis_data_dict = "hospital_id"
#通过redis进行去重
class DuplicatesPipeline(object):
    host = settings['MYSQL_HOST']
    user = settings['MYSQL_USER']
    psd = settings['MYSQL_PASSWORD']
    db = settings['MYSQL_DB']
    c = settings['CHARSET']
    port = settings['MYSQL_PORT']
    conn = pymysql.connect(host=host, user=user, password=psd, db=db, charset=c, port=port)

    def __init__(self):
        redis_db.flushdb()
        if redis_db.hlen(redis_data_dict) == 0:
            sql = "SELECT id FROM hospital_data"
            df = pd.read_sql(sql, self.conn)
            for id in df['id'].get_values():
                redis_db.hset(redis_data_dict, id, 0)

    def process_item(self, item, spider):
        if redis_db.hexists(redis_data_dict, item['id']):
            raise DropItem("Duplicate book found:%s" % item)

        return item

#存入mysql数据库
class DBPipeline(object):
    def process_item(self, item, spider):
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        c = settings['CHARSET']
        port = settings['MYSQL_PORT']
        con=pymysql.connect(host=host,user=user,passwd=psd,db=db,charset=c,port=port)
        cue=con.cursor()
        print("mysql connect succes")
        try:
            cue.execute("INSERT INTO hospital_data(id, hospital_name, grade, hospital_type, create_year, Bed_number, outpatient_number, department_number, personnel_number, address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(item['id'],item['hospital_name'],item['grade'],item['hospital_type'],item['create_year'],item['Bed_number'],item['outpatient_number'],item['department_number'],item['personnel_number'],item['address']))
            print("Insert success")
        except Exception as e:
            print("Insert error:",e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item