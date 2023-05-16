# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BossItem(scrapy.Item):
    # 搜索岗位名
    jobkwd=scrapy.Field()
    # 岗位名称
    jobName=scrapy.Field()
    # 工作区域
    cityName=scrapy.Field()
    # 招聘单位
    companyName=scrapy.Field()
    # 薪酬
    salaryDesc=scrapy.Field()
    # 工作经验年限
    jobExperience=scrapy.Field()
    # 学历
    jobDegree=scrapy.Field()
    # 岗位描述url
    jobDescJsonUrl=scrapy.Field()
    # 岗位描述
    postDescription=scrapy.Field()

