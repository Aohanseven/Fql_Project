# -*- coding: utf-8 -*-
import scrapy
import pymysql
import pandas as pd
from ..items import Data58ShopItem
import re


class Data58ShopSpider(scrapy.Spider):
    name = 'data_spider'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'Wuba.middlewares.ProxyMiddleware': 200,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 300,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        },
        'ITEM_PIPELINES': {
            'Wuba.pipelines.DATADBPipeline': 300
        }

    }
    conn = pymysql.connect(
        host='192.168.0.252',
        user='web_user',
        passwd='first2018pl,',
        db='FBDdata2',
        charset='utf8',
        port=3306)

    def start_requests(self):
        sql = "SELECT link FROM shop58_data WHERE is_ok = '0' "
        df = pd.read_sql(sql, self.conn)
        for link in df['link'].get_values():
            yield scrapy.Request(link, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = Data58ShopItem()
        if response.status == 200:
            if re.findall(r'该页面可能被删除、转移或暂时不可用', response.text) == []:
                item['is_ok'] = '1'
                item['id'] = re.search(
                    'http(s)*://cd.58.com/shangpu/(.*)x.shtml',
                    response.url).group(2)

                item['monthly_rent'] = re.search(
                    r'<span\sclass="house_basic_title_money_num">(.*?)</span>',
                    response.text).group(1)

                item['acreage'] = re.search(r'(\d*)', response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[1]/span[2]/text()').extract_first()).group(1)

                item['shop_type'] = response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[1]/span[4]/a/text()').extract_first()

                item['floor'] = response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[2]/span[2]/text()').extract_first().strip()

                norms = response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[2]/span[4]/text()').extract_first().strip()
                if norms != '暂无':
                    re_norms = re.search(
                        r'面宽(.*?)m.*?进深(.*?)m.*?层高(.*?)m.*?', norms)
                    item['width'], item['depth'], item['height'] = re_norms.group(
                        1), re_norms.group(2), re_norms.group(3)
                else:
                    item['width'], item['depth'], item['height'] = 0, 0, 0

                item['store_status'] = response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[3]/span[2]/text()').extract_first().strip()

                item['payment_method'] = response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[3]/span[4]/text()').extract_first().strip()

                business_industry = response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[4]/span[2]/text()').extract_first().strip()
                if business_industry != '':
                    item['business_industry'] = business_industry
                else:
                    item['business_industry'] = '暂无'

                item['lease_mode'] = response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[4]/span[4]/text()').extract_first().strip()

                address = []
                address1 = response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[6]/a[1]/text()').extract_first()
                address2 = response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[6]/a[2]/text()').extract_first()
                address3 = response.xpath(
                    '/html/body/div[4]/div[2]/div[2]/ul/li[6]/span[2]/text()').extract_first().strip().replace('\xa0', '')
                if address1 is not None:
                    address.append(address1)
                if address2 is not None:
                    address.append(address2)
                if address3 is not None:
                    address.append(address3)
                item['address'] = ','.join(address)

                if re.search('"baidulat":"(.*?)"', response.text) is not None:
                    item['lat'] = re.search(
                        '"baidulat":"(.*?)"', response.text).group(1)
                else:
                    item['lat'] = ''
                if re.search('"baidulon":"(.*?)"', response.text) is not None:
                    item['lng'] = re.search(
                        '"baidulon":"(.*?)"', response.text).group(1)
                else:
                    item['lng'] = ''
                content = response.xpath('//*[@id="generalSound"]')
                item['content'] = content.xpath('string(.)').extract()[0].replace(
                    ' ',
                    '').replace(
                    '\n',
                    '').replace(
                    '\t',
                    '').replace(
                    '\xa0',
                    '')
                yield item
            else:
                item['id'] = re.search(
                    'http(s)*://cd.58.com/shangpu/(.*)x.shtml',
                    response.url).group(2)
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
        else:
            item['id'] = re.search(
                'http(s)*://cd.58.com/shangpu/(.*)x.shtml',
                response.url).group(2)
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
