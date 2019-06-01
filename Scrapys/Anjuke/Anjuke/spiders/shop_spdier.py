# -*- coding: utf-8 -*-
import scrapy
import pymysql
import re
import pandas as pd
from ..items import ShopsSpiderItem


class ShopSpdierSpider(scrapy.Spider):
    name = 'anjuke_dataspdier'
    custom_settings = {
        "ITEM_PIPELINES": {
            'Anjuke.pipelines.DATADBPiplines': 200
        },
        "DOWNLOADER_MIDDLEWARES": {
            # 'Anjuke.middlewares.ProxyMiddleware': 200,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 300,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,

        },
        'DOWNLOAD_DELAY': 4
    }
    start_urls = []
    host = '192.168.0.252'
    user = 'web_user'
    psd = 'first2018pl,'
    db = 'FBDdata2'
    charset = 'utf8'
    port = 3306
    conn = pymysql.connect(
        host=host,
        user=user,
        passwd=psd,
        db=db,
        charset=charset,
        port=port)

    def start_requests(self):
        sql = "SELECT link FROM anjuke_shop_data WHERE is_ok='0'"
        df = pd.read_sql(sql, self.conn)
        for link in df['link'].get_values():
            yield scrapy.Request(link, callback=self.parse, dont_filter=True, meta={'handle_httpstatus_all': True})

    def parse(self, response):
        item = ShopsSpiderItem()
        if response.status == 200:
            item['is_ok'] = '1'

            item['id'] = re.search(
                'http.*://cd.sp.anjuke.com/zu/(.*?)/.*',
                response.url).group(1)

            monthly_rent = response.xpath(
                '//*[@id="fy_info"]/ul[1]/li[1]/span[3]/text()').extract_first()
            if re.search(r'元', monthly_rent):
                item['monthly_rent'] = re.search(
                    r'(\d*)', monthly_rent).group(1)
            else:
                item['monthly_rent'] = int(
                    re.search(r'(\d*)', monthly_rent).group(1)) * 10000

            item['payment_method'] = response.xpath(
                '//*[@id="fy_info"]/ul[1]/li[2]/span[3]/text()').extract_first().strip()

            item['lease_term'] = response.xpath(
                '//*[@id="fy_info"]/ul[1]/li[3]/span[3]/text()').extract_first().strip()

            item['floor'] = response.xpath(
                '//*[@id="fy_info"]/ul[1]/li[4]/span[3]/text()').extract_first().strip()

            norms = response.xpath(
                '//*[@id="fy_info"]/ul[1]/li[5]/span[3]/text()').extract_first().strip()

            if norms != '暂无数据':
                re_norms = re.search(
                    r'面宽(.*?)m.*?层高(.*?)m.*?进深(.*?)m.*?', norms)
                item['width'] = re_norms.group(1)
                item['height'] = re_norms.group(2)
                item['depth'] = re_norms.group(3)
            else:
                item['width'] = 0
                item['height'] = 0
                item['depth'] = 0

            item['address'] = response.xpath(
                '//*[@id="fy_info"]/ul[1]/li[7]/span[3]/text()').extract_first().replace('\n', '').strip('  ').replace(' ', ',')

            item['store_status'] = response.xpath(
                '//*[@id="fy_info"]/ul[2]/li[4]/span[3]/text()').extract_first().strip()

            item['business_industry'] = response.xpath(
                '//*[@id="fy_info"]/ul[2]/li[3]/span[3]/text()').extract_first().replace('-临街','')

            item['is_facestreet'] = '临街'

            item['people'] = response.xpath(
                '//*[@id="fy_info"]/ul[2]/li[6]/span[3]/text()').extract_first().strip()

            item['lat'] = re.findall(r'lat\s*:\s*"(.*?)"', response.text)[0]

            item['lng'] = re.findall(r'lng\s*:\s*"(.*?)"', response.text)[0]

            data = response.xpath('//*[@id="xzl_desc"]/div')

            item['content'] = data.xpath('string(.)').extract()[0].replace(
                ' ', '').replace(
                '\n', '').replace(
                '\t', '')

            item['transfer_fee'] = '面议'

            item['property_fee'] = '面议'

            item['acreage'] = response.xpath(
                '//*[@id="fy_info"]/ul[2]/li[1]/span[3]/text()').extract_first().strip('m²')
            yield item
        elif response.status == 404:
            item['is_ok'] = '2'
            item['id'] = re.search(
                'https://cd.sp.anjuke.com/zu/(.*?)/',
                response.url).group(1)
            item['monthly_rent'] = ''
            item['transfer_fee'] = ''
            item['property_fee'] = ''
            item['acreage'] = ''
            item['width'] = ''
            item['height'] = ''
            item['depth'] = ''
            item['floor'] = ''
            item['store_status'] = ''
            item['lease_term'] = ''
            item['people'] = ''
            item['payment_method'] = ''
            item['address'] = ''
            item['is_facestreet'] = ''
            item['lat'] = ''
            item['lng'] = ''
            item['content'] = ''
            item['business_industry'] = ''

            yield item
