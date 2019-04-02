# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html



import pymysql

from scrapy.conf import settings



#存入mysql数据库
class DBPiplines(object):
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
            cue.execute("update anjuke_community2 set is_ok = '1',community_type='%s',price='%s',create_year='%s',total_area='%s',plot_ratio='%s',developers='%s',property='%s',peripheral_school='%s',property_price='%s',households_number='%s',parking_space='%s',green='%s',lat='%s',lng='%s' )% (item['community_type'],item['price'],item['create_year'],item['total_area'],item['plot_ratio'],item['developers'],item['property'],item['peripheral_school'],item['property_price'],item['households_number'],item['parking_space'],item['green'],item['lat'],item['lng'])")
            print("Insert success")
        except Exception as e:
            print("Insert error:",e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item

