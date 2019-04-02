# -*- coding: utf-8 -*-
import scrapy
import re
class LoupanUrlSpiderSpider(scrapy.Spider):
    name = 'loupan_url_spider'
    def start_requests(self):
        for i in range(62):
            url = 'https://cd.fang.anjuke.com/loupan/all/p'+ i + '/'
            yield scrapy.Request(url,callback=self.parse)
    def parse(self, response):
        links = response.xpath('//*[@id="container"]/div[2]/div[1]/div[3]/div/div/a[1]/@href').extract()
        for link in links:
            yield scrapy.Request(link,callback=self.parse)

    def estateparse(self,response):
        geo = re.search('lat: (.*？), lng: (.*?)}',response.text)
        lat = geo.group(1)
        lng =geo.group(2)
        details = response.xpath('//*[@id="container"]/div[1]/div[2]/div[2]/a/@herf').extract()
        for link in details:
            yield scrapy.Request(link,callback=self.detailsparse,meta={'lat':lat,'lng': lng})

    def detailsparse(self,response):
        estatename = response.xpath('//*[@id="container"]/div[1]/div[2]/div[1]/div/div[1]/h2/text').extract()

