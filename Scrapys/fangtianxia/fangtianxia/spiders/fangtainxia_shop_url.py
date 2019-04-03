# -*- coding: utf-8 -*-
import scrapy
from ..items import FangtianxiaItem
import re


class FangtainxiaShopUrlSpider(scrapy.Spider):
    name = 'fangtainxia_shop_url'
    start_urls = ['http://cd.shop.fang.com/zu/house/']

    def parse(self, response):
        region_urls = response.xpath('/html/body/div[6]/div[2]/div[2]/ul/li[1]/ul/li/a/@href').extract()
        for region_url in region_urls:
            yield  scrapy.Request(url='http://cd.shop.fang.com'+ region_url,callback=self.region_parse)

    def region_parse(self,response):
        item = FangtianxiaItem()
        titles = response.xpath('/html/body/div[6]/div[3]/div[3]/dl/dd[1]/h4/a/span/text()').extract()
        links = response.xpath('/html/body/div[6]/div[3]/div[3]/dl/dd[1]/h4/a/@href').extract()
        for title,link in zip(titles,links):
            item['title'] = title
            item['link'] = 'http://cd.shop.fang.com' + link
            item['id'] = re.search('/zu/._(.*?)\.html',link).group(1)
            yield item
        next_page = response.xpath('//*[@id="PageControl1_hlk_next"]/@href').extract()[0]
        if next_page is not None:
            yield scrapy.Request(url='http://cd.shop.fang.com'+next_page,callback=self.region_parse)

