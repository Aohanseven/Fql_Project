# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import pymysql
from scrapy.conf import settings
import pandas as pd
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem

redis_db = redis.Redis(host='127.0.0.1',port=6379,db=3)
redis_data_dict = "anjuke_community_id"

class DiplicatesPipeline(object):
    host = settings['MYSQL_HOSTS']
    user = settings['MYSQL_USER']
    psd = settings['MYSQL_PASSWORD']
    db = settings['MYSQL_DB']
    c = settings['CHARSET']
    port = settings['MYSQL_PORT']
    con = pymysql.connect(host=host,user=user, passwd=psd, db=db, charset='utf8', port=port)

    def __init__(self):
        redis_db.flushdb()
        if redis_db.hlen(redis_data_dict) == 0:
            sql= "SELECT link FROM anjuke_community2"
            df = pd.read_sql(sql, self.con)
            for link in df['link'].get_values():
                redis_db.hset(redis_data_dict,link,0)

    def process_item(self,item,spider):
       if redis_db.hexists(redis_data_dict,item['link']):
           raise  DropItem("Duplicate book found:%s" % item)
       return item

class DbPipeline(object):
    def process_item(self,item,spider):
        host = settings['MYSQL_HOSTS']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        c = settings['CHARSET']
        port = settings['MYSQL_PORT']
        con = pymysql.connect(host=host,user=user,passwd=psd,db=db,charset=c,port=port)
        cue=con.cursor()
        print('mysql content succes')
        try:
            cue.execute("INSERT INTO anjuke_community2(title,address,link) VALUES (%s,%s,%s)",(item['title'],item['address'],item['link']))
            print("insert succes")
        except Exception as e:
            print('insert error:',e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item


'''

class MysqlTwistedPipeline(object):
    def etree(self, dbpool):
        self.dbpool = dbpool


    @classmethod
    def from_settings(cls, settings):
        dbparms=dict(host=settings['MYSQL_HOSTS'],
                     db=settings['MYSQL_DB'],
                     user=settings['MYSQL_USER'],
                     password=settings['MYSQL_PASSWORD'],
                     port=settings['MYSQL_PORT'],
                     charset='utf8',
                     cursorclass=pymysql.cursors.DictCursor,
                     use_unicode=True
                     )
        dbpool = adbapi.ConnectionPool('pymysql', **dbparms)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)#处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # 执行具体的插入
            insert_sql, params = item.get_insert_sql()
            cursor.execute(insert_sql, params)

    '''