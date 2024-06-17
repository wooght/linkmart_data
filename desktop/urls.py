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
    path('login/', views.login),
    path('summarize/', views.summarize),
    path('userinfo/', views.userinfo),
]