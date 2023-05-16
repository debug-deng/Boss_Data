# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
import scrapy
from scrapy.http import HtmlResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import requests
import urllib.parse 


class BossSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BossDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

# 岗位页面下载中间件 
class jobmiddleware:
    def __init__(self):
        # 实例化浏览器对象
        # self.driver = webdriver.Chrome()

        # PROXY = self.get_proxy()
        # print("代理池信息:"+PROXY)
        options = webdriver.EdgeOptions()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # options.add_argument('--proxy-server=http://%s' % PROXY)
        

        self.driver = webdriver.Edge(options=options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 50)
    
    def get_proxy(self):
      url = 'http://proxy.siyetian.com/apis_get.html?token=gHbi1STqNWeORUVz4ERVl3TB1STqFUeNpXQx0ERZlXT6VUNOpXRx0kaZJTTUFVM.gN0QTM2MzM4YTM&limit=1&type=0&time=&split=1&split_text=&area=0&repeat=0&isp=0'
      response = requests.get(url)
      proxy = response.text
      return proxy

    # 反爬处理
    def process_request(self, request, spider):
        offset = request.meta['flag']
        print(f'offset---{offset}')
        time.sleep(5)
        # 判断当前页面是否正常，如果正常则进入下一页，否则不断刷新
        if offset=='true':
            # 等待加载完成 分页状态   
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.options-pages>a:last-child')))
            self.driver.find_element(By.CSS_SELECTOR,"div.options-pages>a:last-child").click()
        else:
            self.driver.get(request.url)

        # 等待加载完成 直到查找到岗位标签
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'li.job-card-wrapper')))
        # 检查当前url是否包含 /403.html 如果包含则刷新页面
        if '/403.html' in self.driver.current_url:
            print('403页面')
            time.sleep(5)

        return scrapy.http.HtmlResponse(url=request.url, body=self.driver.page_source,encoding="utf-8",request=request,status=200)  # Called for each request that goes through the downloader

    def __del__(self):
        self.driver.close()