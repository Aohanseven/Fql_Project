# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
import pymysql
from..items import FangtianxiaDataItem
import re

class FangtainxiadataSpider(scrapy.Spider):
    name = 'fangtainxiadata'
    conn = pymysql.connect(host='127.0.0.1', user='root', password='a2577811',db='anjuke',port=3306,)
    def start_requests(self):
        sql = 'SELECT link from FTXshop_data WHERE is_ok = 0'
        df = pd.read_sql(sql,self.conn)
        for link in df['link'].get_values():
            yield scrapy.Request(link,self.parse)

    def parse(self, response):
        item = FangtianxiaDataItem()
        item['id'] = re.search('http://cd.shop.fang.com/zu/._(.*?)\.html',response.url).group(1)
        item['monthly_rent'] = re.search('<ul\sclass="wid305">\s*<li>\s*<span><b>(.*)</b>元/月</span>',response.text).group(1)
        item['acreage'] = re.search( '<b>建筑面积</b>\s*<span>(.*)㎡</span>',response.text).group(1)
        if re.search('<b>面宽</b>\s*<span>(.*)</span>',response.text) is not None:
            item['width'] = re.search('<b>面宽</b>\s*<span>(.*)</span>', response.text).group(1)
        else:
            item['width'] = ''
        if re.search('<b>楼盘地址</b>\s*<span\stitle=".*">(.*)</span>',response.text) is not None:
            item['address'] = re.search('<b>楼盘地址</b>\s*<span\stitle=".*">(.*)</span>', response.text).group(1)
        elif re.search('<b>楼盘地址</b>\s*<span>\s*(.*?)\s*</span>',response.text) is not None:
            item['address'] = re.search('<b>楼盘地址</b>\s*<span>\s*(.*?)\s*</span>', response.text).group(1)
        if re.search('<b>进深</b>\s*<span>(.*)</span>',response.text) is not None:
            item['depth'] = re.search('<b>进深</b>\s*<span>(.*)</span>',response.text).group(1)
        else:
            item['depth'] = ''
        if re.search('<b>层高</b>\s*<span>(.*)</span>',response.text) is not None:
            item['height'] = re.search('<b>层高</b>\s*<span>(.*)</span>', response.text).group(1)
        else:
            item['height'] = ''
        item['floor'] = re.search('<li>\s*<b>所在楼层</b>\s*<span>(.*)</span>\s*</li>',response.text).group(1)
        if re.search('<b>类.*型</b>\s*<span>(.*)</span>',response.text) is not None:
            item['shop_type'] = re.search('<b>类.*型</b>\s*<span>(.*)</span>', response.text).group(1)
        else:
            item['shop_type'] = ''
        if re.search('<b>适合经营</b>\s*<span\stitle=".*">(.*)</span>',response.text) is not None:
            item['business_industry'] = re.search('<b>适合经营</b>\s*<span\stitle=".*">(.*)</span>', response.text).group(1)
        else:
            item['business_industry'] = ''
        if re.search('<b>支付方式</b>\s*<span>(.*)</span>',response.text) is not None:
            item['payment_method'] = re.search('<b>支付方式</b>\s*<span>(.*)</span>', response.text).group(1)
        else:
            item['payment_method'] = ''
        if re.search('<b>楼盘名称</b>\s*<span>(.*)</span>',response.text) is not None:
            item['estate'] = re.search('<b>楼盘名称</b>\s*<span>(.*)</span>', response.text).group(1)
        else:
            item['estate'] = ''
        if  re.search('<b>物.*业.*费</b>\s*<span>(.*)</span>',response.text) is not None:
            item['property_fee'] = re.search('<b>物.*业.*费</b>\s*<span>(.*)</span>', response.text).group(1)
        else:
            item['property_fee'] = ''
        if re.search('<b>装.*修</b>\s*<span>(.*)</span>',response.text) is not None:
            item['renovation'] = re.search('<b>装.*修</b>\s*<span>(.*)</span>', response.text).group(1)
        else:
            item['renovation'] = ''
        if re.search('<iframe\ssrc="(.*)"\sscrolling="no"',response.text) is not None:
            url = 'http://' + re.search('<iframe\ssrc="(.*)"\sscrolling="no"',response.text).group(1)
            yield scrapy.Request(url,callback=self.map_parse,meta={'item':item})
        else:
            item['lat'] = ''
            item['lng'] = ''
            yield item
    def map_parse(self,response):
        item =response.meta['item']
        item['lat'] = re.search(',"coordx":"(.*?)",',response.text).group(1)
        item['lng'] = re.search(',"coordy":"(.*?)",',response.text).group(1)
        yield item