# Scrapy settings for boss project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'boss'

SPIDER_MODULES = ['boss.spiders']
NEWSPIDER_MODULE = 'boss.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  "accept": "application/json, text/plain, */*",
"accept-encoding": "gzip, deflate, br",
"accept-language": "zh-CN,zh;q=0.9",
"cache-control": "no-cache",
"cookie": "sid=sem_pz_bdpc_dasou_title; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1670893279; __zp_seo_uuid__=26028d16-d602-4589-8b1f-3792b853a701; __g=sem_pz_bdpc_dasou_title; lastCity=100010000; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1670893325; wd_guid=d7c12463-4a28-437d-baba-5a965a0101f0; historyState=state; _bl_uid=I3lgwbUUl5CiFIqI1uaa6yp4m9vC; __c=1670893279; __l=r=https%3A%2F%2Fwww.baidu.com%2Fother.php%3Fsc.K60000aGJpzS3Zilrxms6ioiJ0TerjCRTQphFSGe9jj593uGzhQEqNec19rztY1XzwrCKCE07rFPgR0hlM4VK2crl3_crcVaXkYME_d3gzNl88QB1PxZC922-e1vCic_Textd0Lq9sSUldyylco5SjoGot9rQcHQDEnelkJsIX3K98Z_iS_zMlvZASpbtBEm8VI1CItWNIU05X8xUJp3UM7Cxlcg.7D_NR2Ar5Od663rj6t8AGSPticrtXFBPrM-kt5QxIW94UhmLmry6S9wiGyAp7BEIu80.TLFWgv-b5HDkrfK1ThPGujYknHb0THY0IAYqmhq1TsKdTvNzgLw4TARqn0K9u7qYXgK-5Hn0IvqzujdBULP10ZFWIWYs0ZNzU7qGujYkPHfkn1fLrHcv0Addgv-b5HDdnjmdPjcz0AdxpyfqnHD3rH0znj00UgwsU7qGujYknW6zP6KsI-qGujYs0A-bm1dcHbc0TA-b5Hcs0APGujYLn6KWThnqPjTzrHD%26dt%3D1670893258%26wd%3Dboss%26tpl%3Dtpl_12826_30685_0%26l%3D1541347926%26us%3DlinkVersion%253D1%2526compPath%253D10036.0-10032.0%2526label%253D%2525E4%2525B8%2525BB%2525E6%2525A0%252587%2525E9%2525A2%252598%2526linkType%253D%2526linkText%253D&l=%2Fwww.zhipin.com%2Fweb%2Fgeek%2Fjob%3Fquery%3DJava%26city%3D100010000%26page%3D9&s=3&g=%2Fwww.zhipin.com%2Fnanchang%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&friend_source=0&s=3&friend_source=0; __a=13852657.1670893279..1670893279.5.1.5.5; __zp_stoken__=9bd6eEEoxRT8xam07QR11c3pbB0pEQFAuSkcOEl0mdSo5XiJkai5hMg5DABAVSUBAF0w1FlE4MXcUCRJkHXxwdAMRMwsjTj9mRzQAKyMzdy8vK0VCVFIIQ2shL3NuYBw%2FVXUHdyBDRVwKRxY%3D",
"pragma": "no-cache",
"referer": "https://www.zhipin.com/web/geek/job?query=Java&city=100010000&page=6",
"sec-ch-ua": '";Not A Brand";v="99", "Chromium";v="94"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "same-origin",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36 Core/1.94.186.400 QQBrowser/11.3.5195.400",
"x-requested-with": "XMLHttpRequest"
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'boss.middlewares.BossSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'boss.middlewares.jobmiddleware': 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'boss.pipelines.BossPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = '2.7'
TWISTED_REACTOR = 'twisted.internet.asyncioreactor.AsyncioSelectorReactor'
