import scrapy
import pymysql
import pandas as pd
import re
from ..items import AgentItem


class Agent_spdier(scrapy.Spider):
    name = 'anjuke_agentspdier'
    custom_settings = {
        "ITEM_PIPELINES": {
            'Anjuke.pipelines.AgentPiplines': 200
        },
        "DOWNLOADER_MIDDLEWARES": {
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
        item = AgentItem()
        if response.status == 200:
            item['agent_name'] = response.xpath(
                '//*[@id="content"]/div[1]/div[2]/div[2]/div[1]/div[1]/h5/text()').extract_first().strip()
            item['agent_company'] = response.xpath(
                '//*[@id="content"]/div[1]/div[2]/div[2]/div[1]/div[1]/p/a[1]/text()').extract_first().strip()
            item['agent_phone'] = re.search(r'<div class="broker_tel"><i class="ico tel_icon"></i>\s*(.*?)\s*</div>', response.text).group(1).replace(' ','')

            yield item