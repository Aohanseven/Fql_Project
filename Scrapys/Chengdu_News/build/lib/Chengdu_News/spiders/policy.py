# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import ChengduNewsItem,  NewsImageItem
import time
import random


class PropertySpider(scrapy.Spider):
    name = 'policy'
    start_urls = ['https://cd.focus.cn/zixun/shichang/']

    def parse(self, response):
        for i in range(1, 10):
            url = response.url + str(i) + '/'
            yield scrapy.Request(url, callback=self.ArticleLinkParse, dont_filter=True)

    def ArticleLinkParse(self, response):
        urls = response.xpath('//*[@id="bd-left"]/div[1]/ul/li/div/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url , callback = self.ArticleParse,dont_filter=True)

    def ArticleParse(self, response):
        item = ChengduNewsItem()
        item['link'] = response.url
        item['title'] = response.xpath('//*[@id="bd-left"]/div[2]/div[1]/h1/text()').extract()
        item['source'] = response.xpath('//*[@id="bd-left"]/div[2]/div[1]/div[1]/div[1]/span[1]/a/text()').extract()
        create_time = response.xpath('//*[@id="bd-left"]/div[2]/div[1]/div[1]/div[1]/span[2]/text()').extract()[0]
        item['create_time'] = re.search(r'(\d{4}-\d{1,2}-\d{1,2}).*',create_time).group(1)
        content = response.xpath('//*[@id="bd-left"]/div[2]/div[1]/div[3]').extract()
        item['content'] = content
        image_urls =re.findall(r'src="(.*?)"', str(content))
        item['image_urls'] = ','.join(image_urls)
        if item['create_time'] != []:
            yield item
        for image_url in image_urls:
            yield scrapy.Request(url=image_url, callback=self.Image_url_parse)

    def Image_url_parse(self, response):
        item = NewsImageItem()
        item['image'] = response.body
        item['image_url'] = response.url
        new_image_url = 'http://fbd.fangqianli.com/FBDweb/News_pic?img=' + str(int(time.time())) + str(
            random.randint(1000, 9999)) + '.img'
        item['new_image_url'] = new_image_url
        item['id'] = re.findall(r'http://fbd\.fangqianli\.com/FBDweb/News_pic\?img=(.*?)\..*', new_image_url)[0]
        item['image_type'] = 1
        yield item



