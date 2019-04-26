import re
import scrapy
import pymysql
import pandas as pd
from ..items import AgentItem


class Data58ShopSpider(scrapy.Spider):
    name = 'agent_spider'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'Wuba.middlewares.ProxyMiddleware': 200,
            'Wuba.middlewares.MyUserAgentMiddleware': 300,
        },
        'ITEM_PIPELINES': {
            'Wuba.pipelines.AgentPiplines': 300
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
        item = AgentItem()
        item['agent_name'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[1]/div/a/text()').extract_first()
        item['agent_phone'] = response.xpath(
            '//*[@id="houseChatEntry"]/div/p[1]/text()').extract_first()
        if re.findall(r'所属公司', response.text) != []:
            item['agent_company'] = response.xpath(
                '/html/body/div[4]/div[2]/div[2]/div[1]/p[1]/span[2]/text()').extract_first()
        else:
            item['agent_company'] = ''
        yield item