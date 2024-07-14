# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :urls.py
@Author     :wooght
@Date       :2024/6/17 13:32
@Content    :
"""
from django.urls import path
from desktop import views
urlpatterns = [
    # 系统
    path('login/', views.login),
    path('summarize/', views.summarize),
    path('userinfo/', views.userinfo),
    path('store_list/', views.store_list),
    path('user/', views.user),
    # 踩点
    path('caidian_map/', views.caidian_map),
    path('save_cd_store/', views.save_cd_store),
    path('save_cd_area/', views.save_cd_area),
    path('save_cd_data/', views.save_cd_data),
    # 工具
    path('spider_list/', views.spider_list),
    path('barcode_toprint', views.barcode_toprint),
    # 数据展示
    path('sku_list/', views.sku_list),
    path('classify_analysis/', views.classify_analysis),

    # 保质单
    path('quality_list/', views.quality_list),
]