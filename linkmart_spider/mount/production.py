# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :production.py
@Author     :wooght
@Date       :2024/6/30 22:08
@Content    :生成任务测试
"""
from celery_object import run_classify_spider

if __name__ == '__main__':
    result = run_classify_spider.delay()
    print(result.id)