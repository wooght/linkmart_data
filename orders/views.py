# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :views.py
@Author     :wooght
@Date       :2024/7/3 22:58
@Content    : 订单视图
"""
from rest_framework.views import APIView
from desktop.models import OrderForm, GoodsList, GoodsClassify, GoodsQuality, BsData
from analysis.DateTimeMath import WDate
from analysis.OrdersAnalysis import OrdersAnalysis
from analysis.ClassifyAnalysis import ClassifyAnalysis
from rest_framework.response import Response
from django.db.models import Q
from goods.serializers import QualitySerializer

class OrderFormView(APIView):
    """
        订单视图 继承 基类
        因为不需要定义queryset, serializer,permission等
    """
    # 默认订单近400 天数据
    start_date = WDate.before_day(400)[0]
    end_date = WDate.before_day(1)[0]

    def get(self, request):
        """
            通过Classify查询/全部数据
        """
        store_id = self.request.COOKIES['store_id']
        classify_id = self.request.query_params.get('categoryId')
        # 所有订单
        orders_list = OrderForm.objects.filter(store_id=store_id, form_date__gt=self.start_date)
        analysis = OrdersAnalysis(orders_list, self.start_date, self.end_date)
        if classify_id:
            # 通过类别计算商品数据
            # 所有商品
            goods_list = GoodsList.objects.filter(store_id=store_id)
            # 查询类别SKU数据
            classify = GoodsClassify.objects.filter(id=classify_id)
            if classify[0].parentId == 0:
                # 拥有子类
                classify_list = GoodsClassify.objects.filter(parentId=classify[0].id)
                # 没有子类
                if classify_list.count() < 1:
                    classify_list = classify
            else:
                classify_list = classify
            result_data = analysis.check_classify(classify_list, goods_list)
        else:
            # 通过订单计算订单数据
            analysis.just_chart_data = True
            analysis.get_just_orders()              # 一个订单一条数据
            chart_data, orders_ct, price_ct = analysis.orders_pack()
            # 所有订单数据
            result_data = {'chart_data':chart_data,
                           'orders_ct': orders_ct,
                           'price_ct': price_ct,
                           'orders_hour': analysis.orders_hour(),
                           'week_hour': analysis.week_7_24()}

        return Response(result_data, status=200)

    def post(self, request):
        """
            通过查询SKU获取订单
        """
        store_id = self.request.COOKIES['store_id']
        search_words = self.request.data['search']
        goods_queryset = GoodsList.objects.filter(
            Q(name__icontains=search_words) | Q(bar_code__icontains=search_words), store_id=store_id)
        if goods_queryset.count() == 1:
            # 如果是单个查询 只获取单个SKU的订单
            orders_queryset = OrderForm.objects.filter(
                store_id=store_id, form_date__gt=self.start_date, goods_code=goods_queryset[0].bar_code)
        else:
            orders_queryset = OrderForm.objects.filter(store_id=store_id, form_date__gt=self.start_date)
        analysis = OrdersAnalysis(orders_queryset, self.start_date, self.end_date)
        result_data = analysis.check_goods(goods_queryset)
        quality_data = None
        if goods_queryset.count() == 1:
            # get()获取单个 能获取外键的值  quality.goods_id 能得到外键 查询结果.values() 可以展开查询行
            # select_related 同时获取外键数据 如果serializer定义了外键,那么instance必须传递外键
            quality = GoodsQuality.objects.select_related('goods').filter(state=1, goods_id=goods_queryset[0].id)
            if quality:
                serializer_obj = QualitySerializer(instance=quality, many=True)
                quality_data = analysis.get_quality(serializer_obj.data)
        return Response({**result_data, 'quality': quality_data}, status=200)

class ClassifyOrdersView(APIView):
    # 默认订单近400 天数据
    start_date = WDate.before_day(400)[0]
    end_date = WDate.before_day(1)[0]

    def get(self, request):
        store_id = self.request.COOKIES['store_id']
        # 获取数据
        goods = GoodsList.objects.filter(store_id=store_id)
        # 需要查询的字段
        fields = ['form_code', 'goods_code', 'goods_num', 'form_date']
        orders = OrderForm.objects.values(*fields).filter(
            Q(form_date__gt=self.start_date) &
            Q(form_date__lt=self.end_date), store_id=store_id)
        classify = GoodsClassify.objects.filter(store_id=store_id)
        analysis = ClassifyAnalysis(orders, classify, goods)
        result_data = analysis.top_classify_pack()
        turnover = BsData.objects.filter(store_id=self.request.COOKIES['store_id'])
        classify_corr = analysis.turnover_corr(turnover)
        return Response({**result_data, 'corr':classify_corr}, status=200)
