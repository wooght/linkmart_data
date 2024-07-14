# Scrapy settings for app_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import sys
import os.path

# 设置运行根目录
now_dir = os.path.dirname(__file__)
up_dir = os.path.dirname(now_dir)
top_dir = os.path.dirname(up_dir)
sys.path.append(top_dir)


BOT_NAME = "app_spider"

SPIDER_MODULES = ["app_spider.spiders"]
NEWSPIDER_MODULE = "app_spider.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 8                # 系统并发量
DOWNLOAD_DELAY = 5                     # 下载延迟时间 单位秒
CONCURRENT_REQUESTS_PER_DOMAIN = 1     # 同域并发量
CONCURRENT_REQUESTS_PER_IP = 1         # 同IP并发量
COOKIES_ENABLED = True                 # 是否启动cookie
RETRY_TIMES = 1                        # 重试次数
# 日志级别  ERROR/WARNING/CRITICAL/DEBUG
LOG_LEVEL = "INFO"
LOG_ENABLED = True
LOG_STDOUT = False   # True 可能会导致scrapyd显示问题
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 "
              "Safari/537.36")
# 默认请求request headers
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "zh-Hans-CN;q=1",
   "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
   "Connection": "keep-alive",
}
DOWNLOADER_MIDDLEWARES = {
    "app_spider.d_middlewares.loginmiddlewares.LoginMiddelWare": 543
}

# 自定义参数
LAST_GOODS = 0

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "app_spider.middlewares.AppSpiderSpiderMiddleware": 543,
#}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "app_spider.pipelines.AppSpiderPipeline": 300,
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
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
