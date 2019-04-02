# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YaozhItem(scrapy.Item):
    # define the fields for your item here like:

    hospital_name = scrapy.Field() #医院名称
    grade = scrapy.Field() #医院等级
    hospital_type = scrapy.Field()  #医院类型
    create_year = scrapy.Field() #建院年份
    Bed_number = scrapy.Field()     #床位数
    outpatient_number = scrapy.Field()  #门诊量(日)
    department_number = scrapy.Field()  #医院科室
    personnel_number =scrapy.Field()     #员工数
    address = scrapy.Field()    #医院地址
    id = scrapy.Field()