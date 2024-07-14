# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :celery_check.py
@Author     :wooght
@Date       :2024/6/30 22:41
@Content    : 检查任务状态
"""

from celery.result import AsyncResult
from celery_object import celery_spider

async_result = AsyncResult(id='60fc89cf-4663-46db-ad3d-2f02388336b3', app=celery_spider)
print('60fc89cf-4663-46db-ad3d-2f02388336b3')
print(async_result.status)
if async_result.successful():
    print('成功')
    print(async_result.get())
elif async_result.failed():
    print('失败')