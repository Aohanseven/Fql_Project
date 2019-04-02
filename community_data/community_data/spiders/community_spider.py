# -*- coding: utf-8 -*-

import scrapy
import pymysql
import pandas as pd
import re
from ..items import CommunityDataItem
from scrapy.conf import settings

class CommunitySpiderSpider(scrapy.Spider):
    name = 'community_spider'
    start_urls = []
    host = settings['MYSQL_HOSTS']
    user = settings['MYSQL_USER']
    psd = settings['MYSQL_PASSWORD']
    db = settings['MYSQL_DB']
    c = settings['CHARSET']
    port = settings['MYSQL_PORT']
    conn = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)

    def start_requests(self):
        sql = "SELECT link,id FROM anjuke_community2 WHERE is_ok='0'"
        df = pd.read_sql(sql, self.conn)
        for link , id in zip(df['link'],df['id']):
            yield scrapy.Request(link, callback=self.parse,meta={'id':id})

    def parse(self, response):
        item = CommunityDataItem()
        item['id'] = response.meta['id']
        item['price'] = re.findall(r'"comm_midprice":"(\d*)"', response.text)[0]
        item['community_type'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[1]/text()').extract_first()
        item['create_year'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[5]/text()').extract_first()
        item['total_area'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[3]/text()').extract_first()
        item['plot_ratio'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[7]/text()').extract_first()
        item['developers'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[9]/text()').extract_first()
        item['property'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[10]/text()').extract_first()
        item['peripheral_school'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[11]/text()').extract_first()
        item['property_price'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[2]/text()').extract_first()
        item['households_number'] = response.xpath( '//*[@id="basic-infos-box"]/dl/dd[4]/text()').extract_first()
        item['parking_space'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[6]/text()').extract_first()
        item['green'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[8]/text()').extract_first()
        item['lat'] = re.findall(r'lat\s*:\s*"(.*?)"', response.text)[0]
        item['lng'] = re.findall(r'lng\s*:\s*"(.*?)"', response.text)[0]
        yield item
