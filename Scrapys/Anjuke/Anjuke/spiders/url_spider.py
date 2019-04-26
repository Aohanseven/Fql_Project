# -*- coding: utf-8 -*-
import scrapy
from ..items import UrlItem
import re


class AnjukeUrlSpiderSpider(scrapy.Spider):
    name = 'anjuke_urlspider'
    custom_settings = {
        "ITEM_PIPELINES": {
            'Anjuke.pipelines.DiplicatesPipeline': 200,
            'Anjuke.pipelines.URLDBPipeline': 300
        },
        "DOWNLOADER_MIDDLEWARES": {
            # 'Anjuke.middlewares.ProxyMiddleware': 200,
            'Anjuke.middlewares.MyUserAgentMiddleware': 300,
        },
        'DOWNLOAD_DELAY': 4
    }
    start_urls = ['https://cd.sp.anjuke.com/zu/']

    def parse(self, response):
        region_list = response.xpath(
            '/html/body/div[5]/div[2]/div/div[1]/div/a/@href').extract()
        for url in region_list:
            yield scrapy.Request(url, callback=self.region_parse)

    def region_parse(self, response):
        local_list = response.xpath(
            '/html/body/div[5]/div[2]/div/div[1]/div/div/a/@href').extract()
        for url in local_list:
            yield scrapy.Request(url, callback=self.local_list, dont_filter=False)

    def local_list(self, response):
        item = UrlItem()
        titles = response.xpath(
            '//*[@id="list-content"]/div/dl/dt/text()').extract()
        links = response.xpath('//*[@id="list-content"]/div/@link').extract()
        for title, link in zip(titles, links):
            item['link'] = link
            item['title'] = title
            item['id'] = int(re.search('http://cd.sp.anjuke.com/zu/(.*?)/.*', link).group(1))
            yield item
        next_page = response.xpath(
            '//div[@class="multi-page"]/a[last()]/@href').extract()[0]
        if next_page is not None:
            yield scrapy.Request(next_page, callback=self.local_list)
