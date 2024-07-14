# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :urls.py
@Author     :wooght
@Date       :2024/6/30 22:49
@Content    :
"""
from django.urls import path
from run_spider import views

urlpatterns = [
    path('orderform/', views.RunSpiderView.as_view())
]