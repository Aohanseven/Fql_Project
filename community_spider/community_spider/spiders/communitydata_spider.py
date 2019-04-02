# -*- coding: utf-8 -*-
import scrapy
import pymysql
import pandas as pd
import re
from ..items import CommunitySpiderItem
from scrapy.conf import settings


class CommunitydataSpiderSpider(scrapy.Spider):
    name = 'communitydata_spider'
    start_urls = []
    host = settings['MYSQL_HOSTS']
    user = settings['MYSQL_USER']
    psd = settings['MYSQL_PASSWORD']
    db = settings['MYSQL_DB']
    c = settings['CHARSET']
    port = settings['MYSQL_PORT']
    conn = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
    def start_requests(self):
        sql = "SELECT link FROM anjuke_community2"
        df = pd.read_sql(sql, self.conn)
        for link in df['link'].get_values():
            yield scrapy.Request(link,callback=self.parse)

    def parse(self, response):
        item = CommunitySpiderItem()
        item['price'] = re.findall(r'"comm_midprice":"(\d*)"',response.text)
        item['community_type'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[1]/selenium_text()').extract_first()
        item['create_year'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[5]/selenium_text()').extract_first()
        item['total_area'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[3]/selenium_text()').extract_first()
        item['plot_ratio'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[7]/selenium_text()').extract_first()
        item['developers'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[9]/selenium_text()').extract_first()
        item['property'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[10]/selenium_text()').extract_first()

        item['peripheral_school'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[11]/selenium_text()').extract_first()
        item['property_price'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[2]/selenium_text()').extract_first()
        item['households_number'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[4]/selenium_text()').extract_first()
        item['parking_space'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[6]/selenium_text()').extract_first()
        item['green'] = response.xpath('//*[@id="basic-infos-box"]/dl/dd[8]/selenium_text()').extract_first()
        item['lat'] = re.findall(r'lat\s*:\s*"(.*?)"', response.text)
        item['lng'] = re.findall(r'lng\s*:\s*"(.*?)"', response.text)
        yield item


