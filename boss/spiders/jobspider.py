import scrapy
import json
import re
import time
from scrapy import Request
from boss.items import BossItem


class JobspiderSpider(scrapy.Spider):
    name = "jobspider"
    allowed_domains = ["www.zhipin.com"]

    def __init__(self, kwd):
        # 获得搜索岗位字段
        self.kwd = kwd
        # 拼接URL
        self.start_urls = (
            f"https://www.zhipin.com/web/geek/job?query={kwd}&city=101280100"
        )

    def start_requests(self):
        # 为请求带参 flag为网站状态
        yield Request(self.start_urls, meta={"flag": "false"}, callback=self.parse)

    def parse(self, response):
        # 获取本页所有岗位和下一个按钮
        job_list = response.css("li.job-card-wrapper")
        next_page = response.css(
            "div.options-pages>a:last-child::attr(class)"
        ).extract_first()
        # 获取当前页码
        page = (
            int(response.css("div.options-pages>a.selected::text").extract_first()) + 1
        )
        print("page---" + str(type(page)))
        # 循环每一个岗位标签
        for i in job_list:
            # 爬取岗位名
            job_name = i.css("span.job-name::text").extract_first()
            # 爬取城市名
            city_name = i.css("span.job-area::text").extract_first()
            # 多个城市用.分割
            if city_name.find("·") > -1:
                city_name = city_name.split("·")[0]
            # 爬取公司名
            brand_name = i.css("h3.company-name>a::text").extract_first()
            # 爬取薪酬水平
            salaryDesc = i.css("span.salary::text").extract_first()
            # 爬取工作经验
            jobExperience = i.css("ul.tag-list>li:nth-child(1)::text").extract_first()
            # 爬取学习要求
            jobDegree = i.css("ul.tag-list>li:nth-child(2)::text").extract_first()
            # 获取岗位描述URL
            job_desc_url = i.css(
                "div.job-card-body.clearfix>a::attr(href)"
            ).extract_first()
            job_desc_url_per = job_desc_url[job_desc_url.find(".html?") + 6 :]

            # 拼接 https://www.zhipin.com/wapi/zpgeek/job/card.json? + str(job_desc_url_per)
            job_desc_json_url = (
                "https://www.zhipin.com/wapi/zpgeek/job/card.json?"
                + str(job_desc_url_per)
            )

            # 实例化Item
            item = BossItem()
            # 传递参数
            item["jobkwd"] = self.kwd
            item["jobName"] = job_name
            item["cityName"] = city_name
            item["companyName"] = brand_name
            item["salaryDesc"] = salaryDesc
            item["jobExperience"] = jobExperience
            item["jobDegree"] = jobDegree
            item["jobDescJsonUrl"] = job_desc_json_url

            yield item

        # 如果不存在下一页按钮且页数小于5 则被反爬 手动拼接下一页URL
        if not next_page and page <= 5:
            next_url = self.start_urls + "&page=" + str(page)
            # 发起下一页网络请求
            yield scrapy.Request(
                url=next_url,
                meta={"flag": "true"},
                callback=self.parse,
                dont_filter=True,
            )

    def close(spider, reason):
        print("爬虫运行完毕")
