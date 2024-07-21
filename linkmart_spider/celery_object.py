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
import os, sys, redis, time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from app_spider import models

# 配置celery
backend = 'redis://{}:{}/1'.format(models.REDIS_HOST,models.REDIS_PORT)    # 存储结果
broker = 'redis://{}:{}/2'.format(models.REDIS_HOST, models.REDIS_PORT)     # 消息中间件
celery_spider = Celery(
    'celery_object',
    backend=backend,
    broker=broker
)
celery_spider.result_serializer = 'json'
celery_spider.conf.timezone = 'Asia/Shanghai'
celery_spider.conf.enable_utc = False
# 连接REDIS
pool = redis.ConnectionPool(host=models.REDIS_HOST, port=models.REDIS_PORT, db=0, socket_connect_timeout=2,
                            decode_responses=True)
r = redis.Redis(connection_pool=pool)

def run_spider(spider_name, last_goods=0, category_id=0):
    """
        运行spider
        params: spider_name 爬虫名称 last_goods 是否只更新最近商品, category_id 类别/custom_date
    """
    # 获取配置
    settings = get_project_settings()
    # 设置配置
    settings.set('last_goods', last_goods, priority='cmdline')
    process = CrawlerProcess(settings)
    # 不同spider传递不同params
    if spider_name == 'goods':
        process.crawl(spider_name, category_id=category_id)
    elif spider_name == 'orderform':
        process.crawl(spider_name, custom_date=category_id)
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
    r.set('spider_store_id', 0)

@celery_spider.task
def before_dawn():
    """
        凌晨运行爬虫
    """
    # 查询需要爬取数据的门店信息
    store_list = models.db.query(models.StoreList).filter(models.StoreList.mt_number != '00')
    for store in store_list:
        # 修改spider_store_id 为当前钥爬取的门店store_id
        r.set('spider_store_id', store.id)
        # 顺序执行
        # 爬取最近跟新goods
        process = multiprocessing.Process(target=run_spider, args=('goods', 0))
        process.start()
        process.join()
        time.sleep(5)
        # 爬取最近一月(不包括今天)的营业额
        process = multiprocessing.Process(target=run_spider, args=('turnover', 0))
        process.start()
        process.join()
        time.sleep(5)
        # 爬取不包括今天的订单(过去2天)
        process = multiprocessing.Process(target=run_spider, args=('orderform', 0))
        process.start()
        process.join()
        time.sleep(30)
    # 爬虫运行结束后,将spider_store_id 归零
    r.set('spider_store_id', 0)
    models.end()

celery_spider.conf.beat_schedule = {
    'every-30-minutes':{
        'task': 'celery_object.before_dawn',
        'schedule': crontab(minute='19', hour='17'),
        'args':(),
    }
}

"""
    启动worker的方法:
    celery multi start w1 -A celery_object worker -l info -P threads
    停止:
    celery multi stop w1 -A celery_object -l info
    celery multi stop worker -A celery_object -l info
    等待执行完再停止:
    celery multi stopwait w1 -A celery_object -l info
"""