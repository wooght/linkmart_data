# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :urls.py
@Author     :wooght
@Date       :2024/6/17 21:00
@Content    :用户认证路由(/userauth/)
"""
from django.urls import path, re_path
from login import views
urlpatterns = [
    path('login/', views.LoginAPIView.as_view()),
    path('user/', views.UserModelViewApi.as_view({'get':'list', 'post':'add_one'})),
]
