# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :views.py
@Author     :wooght
@Date       :2024/7/2 22:51
@Content    :linkmart 商品视图
"""
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from desktop.models import GoodsClassify, GoodsList, GoodsQuality, OrderForm
from goods.serializers import GoodsSerializer, QualitySerializer, QualityPutSerializer
from rest_framework.filters import SearchFilter
from django.db.models import Q
from analysis.DateTimeMath import WDate
from analysis.OrdersAnalysis import OrdersAnalysis

class GoodsClassifyView(ListAPIView):
    """
        类别视图 输出全部分类
        API get:list
        RETURN DATA: {top_classify:{name:id,..}, children:{parentID:{name:id},..},..}
    """
    def list(self, request, *args, **kwargs):
        store_id = request.COOKIES.get('store_id')
        all_classify = GoodsClassify.objects.filter(store_id=store_id)
        top_classify = {}       # 顶级分类
        other_classify = {}     # 次级分类
        for classify in all_classify:
            if classify.parentId == 0:
                if classify.id not in top_classify.keys():
                    top_classify[classify.name] = classify.id
            else:
                if classify.parentId not in other_classify.keys():
                    other_classify[classify.parentId] = {}
                other_classify[classify.parentId][classify.name] = classify.id

        return Response({'top_classify':top_classify, 'children':other_classify}, status=200)

class GoodsView(ReadOnlyModelViewSet):
    """
        SKU 视图  根据类别返回SKU列表 根据PK差当个SKU
        API: get:list   get(pk):retrieve
    """
    serializer_class = GoodsSerializer

    def get_queryset(self):
        category_id = self.request.query_params.get('categoryId')
        store_id = self.request.COOKIES['store_id']
        filter_args = {'store_id':store_id}
        if category_id:
            if int(category_id) != 0:
                filter_args['category_id'] = category_id
        return GoodsList.objects.filter(**filter_args).order_by('-id')


class GoodsSearchView(GenericAPIView):
    """
        查询SKU 返回SKU列表
        API: get(search):get
    """
    serializer_class = GoodsSerializer
    filter_backends = [SearchFilter, ]
    search_fields = ['name', 'bar_code']

    def get_queryset(self):
        store_id = self.request.COOKIES['store_id']
        search_words = self.request.query_params.get('search', None)
        if search_words:
            return GoodsList.objects.filter(Q(name__icontains=search_words) | Q(bar_code__icontains=search_words),store_id=store_id)

    def get(self, request, *args, **kwargs):
        query_set = self.get_queryset()
        serializer = self.get_serializer(instance=query_set, many=True)
        return Response(serializer.data)

class QualityView(GenericViewSet, UpdateModelMixin):
    """
        保质单视图
    """
    # 不需要翻页功能
    pagination_class = None
    serializer_class = QualitySerializer

    def get_queryset(self):
        # 指定门店ID和状态 返回queryset
        self.store_id = self.request.COOKIES['store_id']
        queryset = GoodsQuality.objects.filter(store_id=self.store_id, state=1)
        return queryset

    def list(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        serializer_obj = self.get_serializer(queryset, many=True)
        start_date = WDate.before_day(300)[0]
        end_date = WDate.now_date
        orders = OrderForm.objects.filter(form_date__gt=start_date, store_id=self.store_id)
        analysis = OrdersAnalysis(orders, start_date, end_date)
        result_data = analysis.get_quality(serializer_obj.data)
        return Response(result_data, status=200)


    def get_serializer_class(self):
        # 修改不用传全部字段
        if self.request.method == 'PUT':
            return QualityPutSerializer
        else:
            return QualitySerializer

    def add_one(self, request):
        request_data = {key:value for key,value in request.data.items()}
        request_data['state'] = 1
        request_data['store_id'] = self.request.COOKIES['store_id']
        request_data['add_date'] = WDate.now_date
        serializer_obj = self.get_serializer(data=request_data)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data)
        else:
            return Response(serializer_obj.errors, status=400)

    def get_one(self, request, pk):
        quality_one = self.queryset.filter(goods=pk, state=1).first()
        serializer_obj = self.get_serializer(instance=quality_one)
        return Response(serializer_obj.data, status=200)
