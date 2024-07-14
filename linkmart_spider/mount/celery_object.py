# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :celery_object.py
@Author     :wooght
@Date       :2024/6/30 21:54
@Content    :
"""
import multiprocessing
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from celery import Celery
from celery.schedules import crontab
# 工作目录定位到当前目录
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 配置celery
backend = 'redis://192.168.101.101:6379/1'    # 存储结果
broker = 'redis://192.168.101.101:6379/2'     # 消息中间件
celery_spider = Celery(
    'celery_object',
    backend=backend,
    broker=broker
)
celery_spider.result_serializer = 'json'
celery_spider.conf.timezone = 'Asia/Shanghai'
celery_spider.conf.enable_utc = False

def run_spider(spider_name, last_goods=0, category_id=0):
    # 获取配置
    settings = get_project_settings()
    # 设置配置
    settings.set('last_goods', last_goods, priority='cmdline')
    process = CrawlerProcess(settings)
    if spider_name == 'goods':
        process.crawl(spider_name, category_id=category_id)
    else:
        process.crawl(spider_name)
    process.start(stop_after_crawl=True)    # 爬虫结束后 关闭引擎
    process.stop()

@celery_spider.task
def run_goods_spider(**kwargs):
    args = (val for val in kwargs.values())
    # 开启新的进程
    process = multiprocessing.Process(target=run_spider, args=args)
    process.start()
    # 等待进程结束
    process.join()


@celery_spider.task
def before_dawn():
    """
        凌晨运行爬虫
    """
    # 顺序执行
    process = multiprocessing.Process(target=run_spider, args=('goods', 0))
    process.start()
    process.join()
    process = multiprocessing.Process(target=run_spider, args=('turnover', 0))
    process.start()
    process.join()
    process = multiprocessing.Process(target=run_spider, args=('orderform', 0))
    process.start()
    process.join()

celery_spider.conf.beat_schedule = {
    'every-30-minutes':{
        'task': 'celery_object.before_dawn',
        'schedule': crontab(minute='37'),
        'args':(),
    }
}

"""
    启动worker的方法:
    celery multi start w1 -A celery_object -l info -P threads
"""