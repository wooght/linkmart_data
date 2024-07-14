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
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/linkmart_spider/mount/')
from celery.result import AsyncResult
import celery_object
from celery_object import celery_spider


class RunSpiderView(APIView):
    def get(self, request):
        """
            运行爬虫
        """
        # 获取爬虫参数
        spider_name = request.GET['spider_name']
        last_goods = request.GET['last_goods']
        category_id = request.GET['categoryId']
        # 异步运行爬虫
        result = celery_object.run_goods_spider.delay(
            spider_name=spider_name,
            last_goods=last_goods,
            category_id=category_id
        )
        # 返回task ID
        return Response({'id': result.id}, status=200)

    def post(self, request):
        """
            获取task运行状态
        """
        id = request.POST['id']
        asynec_result = AsyncResult(id=id, app=celery_spider)
        if asynec_result.failed():
            return Response({'status': 'failed'}, status=400)
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