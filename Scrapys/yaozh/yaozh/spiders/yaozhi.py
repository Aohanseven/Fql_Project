# -*- coding: utf-8 -*-
import scrapy
from ..items import YaozhItem
import re


class YaozhiSpider(scrapy.Spider):
    name = 'yaozhi'
    start_urls = ['https://db.yaozh.com/hmap/']

    def parse(self, response):
        for i in range(1,7000):
            yield scrapy.Request(url='https://db.yaozh.com/hmap/'+ str(i)+'.html',callback=self.hospital_parse)

    def hospital_parse(self,response):
        item = YaozhItem()
        item['hospital_name'] = re.findall(r'<th\s*class.*?>医院名称</th>\s*<td>\s*<span\s*class="toFindImg">\s*(.*?)\s*</span>',response.text)[0]
        item['grade'] = re.findall(r'<th\s*class.*?>医院等级</th>\s*<td>\s*<span\s*class="toFindImg">\s*(.*?)\s*</span>',response.text)[0]
        item['hospital_type'] = re.findall(r'<th\s*class.*?>医院类型</th>\s*<td>\s*<span\s*class="toFindImg">\s*(.*?)\s*</span>',response.text)[0]
        create_year =re.findall(r'<th\s*class.*?>建院年份</th>\s*<td>\s*<span\s*class="toFindImg">\s*(.*?)\s*</span>',response.text)
        if len(create_year) != 0:
            item['create_year'] = str(create_year[0])
        else:
            item['create_year'] = None
        Bed_number = re.findall(r'<th\s*class.*?>床位数</th>\s*<td>\s*<span\s*class="toFindImg">\s*(.*?)\s*</span>',response.text)
        if len(Bed_number) != 0:
            item['Bed_number'] = int(Bed_number[0])
        else:
            item['Bed_number'] = None
        outpatient_number = re.findall(r'<th\s*class.*?>门诊量\(日\)</th>\s*<td>\s*<span\s*class="toFindImg">\s*(.*?)\s*</span>',response.text)
        if len(outpatient_number) != 0:
            item['outpatient_number'] = int(outpatient_number[0])

        else:
            item['outpatient_number'] = None
        department_number = re.findall(r'<th\s*class.*?>医院科室</th>\s*<td>\s*<span\s*class="toFindImg">\s*(.*?)\s*</span>',response.text)
        if len(department_number) != 0:
            item['department_number'] = len(department_number[0])
        else:
            item['department_number'] = None
        personnel_number = re.findall(r'<th\s*class.*?>员工数</th>\s*<td>\s*<span\s*class="toFindImg">\s*(.*?)\s*</span>',response.text)
        if len(personnel_number) != 0:
            item['personnel_number'] = int(personnel_number[0])
        else:
            item['personnel_number'] = None
        item['address'] = re.findall(r'<th\s*class.*?>医院地址</th>\s*<td>\s*<span\s*class="toFindImg">\s*(.*?)\s*</span>',response.text)[0]
        item['id'] = int(re.findall(r'https://db.yaozh.com/hmap/(.*?).html',response.url)[0])
        yield item
