# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :urls.py
@Author     :wooght
@Date       :2024/7/8 15:39
@Content    :
"""
from django.urls import path
from turnover.views import TurnoverModeView
urlpatterns = [
    path('index/', TurnoverModeView.as_view()),
]