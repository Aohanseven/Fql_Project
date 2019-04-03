# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
class DBPiplines(object):
    def process_item(self, item, spider):
        con = pymysql.connect(host='127.0.0.1', user='root', passwd='a2577811', db='anjuke',charset='utf8', port=3306)
        cue=con.cursor()
        print("mysql connect succes")
        try:
            cue.execute("UPDATE FTXshop_data SET is_ok = 1,monthly_rent='%s',shop_type='%s',acreage='%s',width='%s',address='%s',depth='%s',height='%s',floor='%s',business_industry='%s',payment_method='%s',lat='%s',lng='%s' WHERE id='%s'" %
                        (item['monthly_rent'],item['shop_type'],item['acreage'],item['width'],item['address'],item['depth'],item['height'],item['floor'],item['business_industry'],item['payment_method'],item['lat'],item['lng'],item['id']))
            print("Update success")
        except Exception as e:
            print("Update error:",e)
            con.rollback()
        else:
            con.commit()
        con.close()
        return item