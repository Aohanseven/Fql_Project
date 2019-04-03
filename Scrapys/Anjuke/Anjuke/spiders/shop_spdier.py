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
            'Anjuke.middlewares.MyUserAgentMiddleware': 300,
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
    conn = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=charset, port=port)

    def start_requests(self):
        sql = "SELECT link FROM anjuke_shop_data WHERE is_ok='0'"
        df = pd.read_sql(sql, self.conn)
        for link in df['link'].get_values():
            yield scrapy.Request(link, callback=self.parse, dont_filter=True, meta={'handle_httpstatus_all': True})

    def parse(self, response):
        # self.logger.debug("(parse_page) response: status=%d, URL=%s" % (response.status, response.url))
        # if response.status in (302,) and 'Location' in response.headers:
        #     self.logger.debug("(parse_page) Location header: %r" % response.headers['Location'])
        #     yield scrapy.Request(
        #         response.urljoin(response.headers['Location']),
        #         callback=self.parse)]

        item = ShopsSpiderItem()
        if response.status == 200:
            item['is_ok'] = '1'
            item['id'] = re.search('https://cd.sp.anjuke.com/zu/(.*?)/', response.url).group(1)
            monthly_rent = re.findall(r'<span\s*class="fst">月租：</span>\s*<span\s*class="desc">(.*?)</span>', response.text)[0]
            if re.search(r'元', monthly_rent):
                item['monthly_rent'] = re.search(r'(\d*)',monthly_rent).group(1)
            else:
                item['monthly_rent'] = int(re.search(r'(\d*)', monthly_rent).group(1))*10000
            item['transfer_fee'] = \
            re.findall(r'<span\s*class="fst">转让费：</span>\s*<span\s*class="desc">(.*?)</span>', response.text)[0]
            item['property_fee'] = \
            re.findall(r'<span\s*class="fst">物业费：</span>\s*<span\s*class="desc">(.*?)</span>', response.text)[0]
            acreage = re.findall(r'<span\s*class="fst">面积：</span>\s*<span\s*class="desc">(.*?)</span>', response.text)[0]
            item['acreage'] = re.search(r'(\d*)',acreage).group(1)
            item['width'] = \
            re.findall(r'<span\s*class="fst">面宽：</span>\s*<span\s*class="desc">(.*?)m</span>', response.text)[0]
            item['height'] = \
            re.findall(r'<span\s*class="fst">层高：</span>\s*<span\s*class="desc">(.*?)m</span>', response.text)[0]
            if re.findall(r'<span\s*class="fst">进深：</span>\s*<span\s*class="desc">(.*?)m</span>', response.text):
                item['depth'] = \
                re.findall(r'<span\s*class="fst">进深：</span>\s*<span\s*class="desc">(.*?)m</span>', response.text)[0]
            else:
                item['depth'] = ''
            item['floor'] = \
            re.findall(r'<span\s*class="fst">楼层：</span>\s*<span\s*class="desc">(.*?)</span>', response.text)[0]
            store_status = \
            re.findall(r'<span\s*class="fst">状态：</span>\s*<span\s*class="desc"\s*title="(.*?)">.*</span>',
                       response.text)[0]
            if re.search('空铺', store_status) is not None:
                item['store_status'] = '空铺出租/转让'
            elif re.search('营业中', store_status) is not None:
                item['store_status'] = '营业中'
            if re.search('<b>(.*?)</b>', store_status) is not None:
                item['business_industry'] = re.search('<b>(.*?)</b>', store_status).group(1)
            else:
                item['business_industry'] = ''
            # store_status = re.findall(r'(.*?), 之前为', re.findall(r'<span\s*class="fst">状态：</span>\s*<span\s*class="desc"\s*title="(.*?)">.*</span>', response.text)[0])
            # if store_status != []:
            #     item['store_status'] = store_status[0]
            # else:
            #     item['store_status'] = re.findall(r'<span\s*class="fst">状态：</span>\s*<span\s*class="desc"\s*title="(.*?)">.*</span>',response.text)[0]
            if re.findall(r'<span\s*class="fst">起租期：</span>\s*<span\s*class="desc">(.*?)</span>', response.text):
                item['lease_term'] = \
                re.findall(r'<span\s*class="fst">起租期：</span>\s*<span\s*class="desc">(.*?)</span>', response.text)[0]
            else:
                item['lease_term'] = ''
            item['people'] = \
            re.findall(r'<span\s*class="fst">人群：</span>\s*<span\s*class="desc"\s*title="(.*?)">.*', response.text)[0]
            item['payment_method'] = \
            re.findall(r'<span\s*class="fst">押付：</span>\s*<span\s*class="desc">(.*?)</span>', response.text)[0]
            item['address'] = re.findall(
                r'<span\s*class="fst">地址：</span>\s*<span\s*class="desc addresscommu"\s*title=".*">\s*(.*?)\s*</span>',
                response.text)[0].replace('                    ', ',')
            item['is_facestreet'] = \
            re.findall(r'<span\s*class="fst">是否临街：</span>\s*<span\s*class="desc">(.*?)</span>', response.text)[0]
            item['lat'] = re.findall(r'lat\s*:\s*"(.*?)"', response.text)[0]
            item['lng'] = re.findall(r'lng\s*:\s*"(.*?)"', response.text)[0]
            data = response.xpath('//*[@id="xzl_desc"]/div')
            item['content'] = data.xpath('string(.)').extract()[0].replace(' ', '').replace('\n', '').replace('\t', '')
            # item['matching'] =','.join(re.findall(r'<li\sclass="">\s*<i class=".*"></i>\s*<p>(.*?)</p>',response.text))
            yield item
        elif response.status == 404:
            item['is_ok'] = '2'
            item['id'] = re.search('https://cd.sp.anjuke.com/zu/(.*?)/', response.url).group(1)
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
