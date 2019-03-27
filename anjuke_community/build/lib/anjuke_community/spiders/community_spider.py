# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import AnjukeCommunityItem


class CommunitySpiderSpider(scrapy.Spider):
    name = 'community_spider'
    start_urls = ['https://chengdu.anjuke.com/community/']

    def parse(self, response):
        region_list = response.xpath('/html/body/div[5]/div[2]/div[1]/span[2]/a/@href').extract()[1:]
        for url in region_list:
            yield scrapy.Request(url,callback=self.region_parse)

    def region_parse(self,response):
        local_list = response.xpath('/html/body/div[5]/div[2]/div[1]/span[2]/div/a/@href').extract()
        for url in local_list:
                yield  scrapy.Request(url,callback=self.local_list)

    def local_list(self,response):
        item = AnjukeCommunityItem()
        titles = response.xpath('//*[@id="list-content"]/div/a/@title').extract()
        links= response.xpath('//*[@id="list-content"]/div/a/@href').extract()
        addresss = re.findall(r'\s*<address>\s*(.*?)\s*</address>',response.text)
        for title,address,link in zip(titles,addresss,links):
            item['link'] = link
            item['title'] = title
            item['address'] = address.strip()
            item['id'] = int(re.findall(r'https://chengdu.anjuke.com/community/view/(.*)',link)[0])
            yield item
        next_page = response.xpath('//div[@class="multi-page"]/a[last()]/@href').extract()[0]
        if next_page is not None:
            yield scrapy.Request(next_page,callback=self.local_list)


