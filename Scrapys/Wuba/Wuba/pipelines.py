# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import redis
import pandas as pd
from scrapy.exceptions import DropItem


redis_db = redis.Redis(host='127.0.0.1', port=6379, db=1)
redis_data_dict = "shops58_id"


class URLDiplicatesPipeline(object):
    con = pymysql.connect(
        host='192.168.0.252',
        user='web_user',
        passwd='first2018pl,',
        db='FBDdata2',
        charset='utf8',
        port=3306)

    def __init__(self):
        redis_db.flushdb()
        if redis_db.hlen(redis_data_dict) == 0:
            sql = "SELECT id FROM shop58_data"
            df = pd.read_sql(sql, self.con)
            for id in df['id'].get_values():
                redis_db.hset(redis_data_dict, id, 0)

    def process_item(self, item, spider):
        if redis_db.hexists(redis_data_dict, item['id']):
            raise DropItem("Duplicate book found:%s" % item)
        return item


class URLDBPipeline(object):

    def process_item(self, item, spider):
        con = pymysql.connect(
            host='192.168.0.252',
            user='web_user',
            passwd='first2018pl,',
            db='FBDdata2',
            charset='utf8',
            port=3306)
        cue = con.cursor()
        print('mysql content succes')
        try:
            cue.execute(
                "INSERT INTO shop58_data (id,title,link) VALUES (%s,%s,%s)",
                (item['id'],
                 item['title'],
                    item['link']))
            print("insert succes")
        except Exception as e:
            print('insert error:', e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item


class DATADBPipeline(object):
    def process_item(self, item, spider):
        con = pymysql.connect(
            host='192.168.0.252',
            user='web_user',
            passwd='first2018pl,',
            db='FBDdata2',
            charset='utf8',
            port=3306)
        cue = con.cursor()
        print("mysql connect succes")
        try:
            cue.execute(
                "UPDATE shop58_data SET is_ok='%s',monthly_rent='%s',store_status='%s',shop_type='%s',acreage='%s',width='%s',address='%s',depth='%s',height='%s',floor='%s',business_industry='%s',payment_method='%s',lease_mode='%s',lat='%s',lng='%s',content='%s' WHERE id='%s'" %
                (item['is_ok'],
                 item['monthly_rent'],
                    item['store_status'],
                    item['shop_type'],
                    item['acreage'],
                    item['width'],
                    item['address'],
                    item['depth'],
                    item['height'],
                    item['floor'],
                    item['business_industry'],
                    item['payment_method'],
                    item['lease_mode'],
                    item['lat'],
                    item['lng'],
                    item['content'],
                    item['id']))
            print("Update success")
        except Exception as e:
            print("Update error:", e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item


class AgentPiplines(object):
    def process_item(self, item, spider):
        con = pymysql.connect(
            host='192.168.0.252',
            user='web_user',
            passwd='first2018pl,',
            db='FBDdata2',
            charset='utf8',
            port=3306)
        cue = con.cursor()
        try:
            cue.execute(
                "insert into zu_agent_info(agent_name,agent_phone,agent_company,from_web) values (%s,%s,%s,2)", (item['agent_name'],item['agent_phone'],item['agent_company']))
            print("Update success")
        except Exception as e:
            print("Update error:", e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item
