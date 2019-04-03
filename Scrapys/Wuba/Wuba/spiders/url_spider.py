# -*- coding: utf-8 -*-
import scrapy
from ..items import WubaurlItem
import re


class Shop58UrlSpider(scrapy.Spider):
    name = 'url_spider'
    custom_settings = {
         'DOWNLOADER_MIDDLEWARES' : {
            'Wuba.middlewares.ProxyMiddleware': 200,
             'Wuba.middlewares.MyUserAgentMiddleware': 300,

         },
        "ITEM_PIPELINES": {
            'Wuba.pipelines.URLDiplicatesPipeline': 200,
            'Wuba.pipelines.URLDBPipeline': 300
        }
    }

    start_urls = ['https://cd.58.com/shangpucz/']

    def parse(self, response):
        region_list = response.xpath('/html/body/div[5]/div[3]/dl[1]/dd/a/@href').extract()
        for url in region_list:
            region_url = 'https://cd.58.com' + url
            yield scrapy.Request(region_url, callback=self.region_parse )

    def region_parse(self, response):
        item = WubaurlItem()
        links = re.findall('<a href="(https://cd\.58\.com/shangpu/.*?\.shtml)"\starget=',response.text)
        titles = response.xpath('/html/body/div[5]/div[5]/div[1]/ul/li/div[2]/h2/a/span/text()').extract()
        for link, title in zip(links,titles):
            item['link'] = link
            item['title'] = title
            item['id'] = re.findall('https://cd.58.com/shangpu/(.*?)x.shtml',link)[0]
            yield item
        next_page = response.xpath('/html/body/div[5]/div[5]/div[1]/div/a[@class="next"]/@href').extract_first()
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.region_parse)
