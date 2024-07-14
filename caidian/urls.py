# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :urls.py
@Author     :wooght
@Date       :2024/6/18 16:40
@Content    :踩点模块路由
"""
from django.urls import path, re_path
from caidian import views
urlpatterns = [
    path('area/', views.CaiDianAreaAPIView.as_view({'get': 'list', 'post':'create'})),
    re_path('area/(?P<pk>\d+)/', views.CaiDianAreaAPIView.as_view({'get':'retrieve', 'put':'update'})),
    path('label/', views.CaiDianLabelAPIView.as_view()),
    path('store/', views.CaiDianStoreAPIView.as_view()),
    re_path('store/(?P<pk>\d+)/', views.CaiDianStoreAPIView.as_view()),
    path('data/', views.CaiDianDataAPIView.as_view()),
    re_path('data/(?P<pk>\d+)', views.CaiDianDataAPIView.as_view()),
]
