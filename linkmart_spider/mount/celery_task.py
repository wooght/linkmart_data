# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :celery_task.py
@Author     :wooght
@Date       :2024/6/30 22:00
@Content    :celery 任务
"""
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import multiprocessing
from celery_object import celery_spider

@celery_spider.task
def run_classify_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl('classify')
    process.start(stop_after_crawl=True)    # 爬虫结束后 关闭引擎
