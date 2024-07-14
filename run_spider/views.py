# -- coding: utf-8 -
"""
@project    :run_spider
@file       :serializer.py
@Author     :wooght
@Date       :2024/6/18 16:13
@Content    :run spider 视图
"""
from rest_framework.views import APIView
from rest_framework.response import Response

import os,sys
# 调用celery和celery运行的路径必须一致
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/linkmart_spider/')
from celery.result import AsyncResult
import celery_object
from celery_object import celery_spider
from django.conf import settings
import redis
from linkmart_spider.app_spider import models


class RunSpiderView(APIView):
    pool = redis.ConnectionPool(host=models.REDIS_HOST, port=models.REDIS_PORT, db=0, socket_connect_timeout=2, decode_responses=True)
    r = redis.Redis(connection_pool=pool)

    def get(self, request):
        """
            运行爬虫
        """
        # 获取爬虫参数
        spider_name = request.GET['spider_name']
        last_goods = request.GET['last_goods']
        category_id = request.GET['categoryId']
        # 设置spider_store_id
        current_store_id = self.r.get('spider_store_id')
        if int(current_store_id) == 0:
            self.r.set('spider_store_id', self.request.COOKIES['store_id'])
            # 异步运行爬虫
            result = celery_object.run_goods_spider.delay(
                spider_name=spider_name,
                last_goods=last_goods,
                category_id=category_id
            )
            # 返回task ID
            return Response({'id': result.id}, status=200)
        else:
            return Response({'error': '等会再试!'}, status=400)

    def post(self, request):
        """
            获取task运行状态
        """
        id = request.POST['id']
        asynec_result = AsyncResult(id=id, app=celery_spider)
        if asynec_result.failed():
            return Response({'error': 'failed'}, status=400)
        else:
            return Response({'status': asynec_result.status}, status=200)


"""
    django spider 运行思路:
        WEB页面:罗列所有可用的爬虫
            turnover
            orderform->last 2 days
            orderform->date
            goods->last
            goods->all
            goods->classify
            classify
    守护进程运行:
        celery 传 parameter   需解决问题:守护进程
        redis 分布式 挂载所有spider 需解决问题:scrapy 守护进程
"""