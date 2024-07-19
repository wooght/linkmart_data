# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :urls.py
@Author     :wooght
@Date       :2024/7/19 13:31
@Content    :
"""
from django.urls import path, re_path
from store.views import StoreModelViewSet, StoreOneViewApi

urlpatterns = [
    path('list/', StoreModelViewSet.as_view()),
    re_path('update/(?P<pk>\d+)', StoreOneViewApi.as_view()),
]
