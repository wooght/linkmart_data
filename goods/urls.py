# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :urls.py
@Author     :wooght
@Date       :2024/7/2 22:51
@Content    :
"""
from django.urls import path, re_path
from goods.views import GoodsClassifyView, GoodsView, GoodsSearchView, QualityView

urlpatterns = [
    path('classify/', GoodsClassifyView.as_view()),
    path('classify_goods/', GoodsView.as_view({'get':'list'})),
    # SetView get可以两个不同方向,因为要指定get到谁
    re_path('classify_goods/(?P<pk>\d+)', GoodsView.as_view({'get':'retrieve'})),
    path('search_goods/', GoodsSearchView.as_view()),
    path('quality/', QualityView.as_view({'post':'add_one', 'get':'list'})),
    re_path('quality/(?P<pk>\d+)', QualityView.as_view({'get':'get_one', 'put':'update'})),
]