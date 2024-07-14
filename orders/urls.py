# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :urls.py
@Author     :wooght
@Date       :2024/7/3 22:59
@Content    :
"""
from django.urls import path
from orders.views import OrderFormView, ClassifyOrdersView

urlpatterns = [
    path('classify_orders/', OrderFormView.as_view()),
    path('classify_analysis/', ClassifyOrdersView.as_view()),
]