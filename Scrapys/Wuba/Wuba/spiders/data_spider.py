# -*- coding: utf-8 -*-
import scrapy
import pymysql
import pandas as pd
from ..items import Data58ShopItem
import re


class Data58ShopSpider(scrapy.Spider):
    name = 'data_spider'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES' : {
            'Wuba.middlewares.ProxyMiddleware': 200,
            'Wuba.middlewares.MyUserAgentMiddleware': 300,
         },
        'ITEM_PIPELINES': {
            'Wuba.pipelines.DATADBPipeline': 300
        }

    }
    conn = pymysql.connect(host='192.168.0.252', user='web_user', passwd='first2018pl,', db='FBDdata2', charset='utf8',
                          port=3306)

    def start_requests(self):
        sql = "SELECT link FROM shop58_data WHERE is_ok = '0' "
        df = pd.read_sql(sql, self.conn)
        for link in df['link'].get_values():
            yield scrapy.Request(link, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = Data58ShopItem()
        try:
            item['is_ok'] = '1'
            item['id'] = re.search('http(s)*://cd.58.com/shangpu/(.*)x.shtml',response.url).group(2)
            item['monthly_rent'] = re.search('<span\sclass="house_basic_title_money_num">(.*?)</span>',response.text).group(1)
            acreage= re.search('<span\sclass="house_basic_title_content_item1">房屋面积:</span>\s*<span\sclass="house_basic_title_content_item2">(.*?)</span>',response.text).group(1)
            item['acreage'] = re.search(r'(\d*)',acreage).group(1)
            item['width'] = re.search('宽:</span>\s*<span class="house_basic_title_content_item2">\s(.*?)m\s</span>',response.text).group(1)
            if re.search('onclick="clickLog\(\'from=fcpc_shangpu_detail_jichuxinxi@name=1\'\)"\starget="_blank">(.*?)</a>',response.text):
                address1 = re.search('onclick="clickLog\(\'from=fcpc_shangpu_detail_jichuxinxi@name=1\'\)"\starget="_blank">(.*?)</a>',response.text).group(1)
            else:
                address1 = ''
            if re.search('onclick="clickLog\(\'from=fcpc_shangpu_detail_jichuxinxi@name=2\'\)"\starget="_blank">(.*?)</a>',response.text):
                address2 = re.search('onclick="clickLog\(\'from=fcpc_shangpu_detail_jichuxinxi@name=2\'\)"\starget="_blank">(.*?)</a>',response.text).group(1)
            else:
                address2 = ''
            if re.search('<span\sclass="house_basic_title_content_item3\sxxdz-des">\s*(.*?)\s*</span>',response.text):
                address3 = re.search('<span\sclass="house_basic_title_content_item3\sxxdz-des">\s*(.*?)\s*</span>',response.text).group(1)
            else:
                address3 = ''
            item['address'] = (address1+ ',' + address2 +','+ address3).replace('&nbsp','' )

            item['depth'] = re.search('深:</span>\s*<span\sclass="house_basic_title_content_item2">\s(.*?)m\s</span>',response.text).group(1)
            item['height'] = re.search('高:</span>\s*<span\sclass="house_basic_title_content_item2">\s(.*?)m\s</span>',response.text).group(1)
            item['floor'] = re.search('层:</span>\s*<span\sclass="house_basic_title_content_item2">\s*(.*?)\s*</span>',response.text).group(1)
            item['shop_type'] = re.search('onclick="clickLog\(\'from=fcpc_shangpu_detail_jichuxinxi@name=4\'\)">(.*?)</a>',response.text).group(1)
            item['store_status'] = re.search('态:</span>\s*<span\sclass="house_basic_title_content_item3">\s*(.*?)\s*</span>',response.text).group(1)
            business_industry = re.search('历史经营:</span>\s*<span class="house_basic_title_content_item3">\s*(.*?)\s*-&nbsp;(.*?)\s*</span>\s*</li>',response.text)
            if business_industry is not None:
                item['business_industry'] = business_industry.group(1) + ',' + business_industry.group(2)
            elif  re.search('历史经营:</span>\s*<span class="house_basic_title_content_item3">\s*(.*?)\s*</span>',response.text) is not None:
                item['business_industry'] = re.search('历史经营:</span>\s*<span class="house_basic_title_content_item3">\s*(.*?)\s*</span>',response.text).group(1)
            else:
                item['business_industry'] = '暂无'
            item['payment_method'] = re.search('付款方式:</span>\s*<span\sclass="house_basic_title_content_item3">(.*?)</span>\s*',response.text).group(1)
            item['lease_mode'] = re.search('租约方式:</span>\s*<span\sclass="house_basic_title_content_item3">(.*?)</span>',response.text).group(1)
            if re.search('"baidulat":"(.*?)"',response.text) is not None:
                item['lat'] = re.search('"baidulat":"(.*?)"',response.text).group(1)
            else:
                item['lat'] = ''
            if re.search('"baidulon":"(.*?)"',response.text) is not None:
                item['lng'] = re.search('"baidulon":"(.*?)"',response.text).group(1)
            else:
                item['lng'] = ''
            content = response.xpath('//*[@id="generalSound"]')
            if content.extract()!= []:
                item['content'] = content.xpath('string(.)').extract()[0].replace(' ','').replace('\n','').replace('\t','')
            else:
                item['content'] = ''
            yield item
        except Exception as e:
            print(e)
            item['is_ok'] = '2'
            item['monthly_rent'] = ''
            item['acreage'] = ''
            item['width'] = ''
            item['address'] = ''
            item['depth'] = ''
            item['height'] = ''
            item['floor'] = ''
            item['shop_type'] = ''
            item['store_status'] = ''
            item['business_industry'] = ''
            item['payment_method'] = ''
            item['lease_mode'] = ''
            item['lat'] = ''
            item['lng'] = ''
            item['content'] = ''
            yield item
