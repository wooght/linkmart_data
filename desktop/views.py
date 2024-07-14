# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :views.py
@Author     :wooght
@Date       :2024/6/17 13:32
@Content    :前端View
"""
from django.shortcuts import render
from django.http import HttpRequest

# 首页
def index(request):
    return render(request, template_name='index.html')

# 登录页
def login(request):
    return render(request, template_name='login.html')

# 注册页面
def userinfo(request):
    return render(request, template_name='userinfo.html')

# 首页
def summarize(request):
    return render(request, template_name='summarize.html')

def store_list(request):
    return render(request, template_name='store_list.html')

def caidian_map(request):
    return render(request, template_name='caidian_map.html')

def save_cd_store(request):
    return render(request, template_name='save_cd_store2.html')

def save_cd_area(request):
    return render(request, template_name='save_cd_area.html')

def save_cd_data(request):
    return render(request, template_name='save_cd_data.html')

def user(request):
    return render(request, template_name='user.html')

def spider_list(request):
    return render(request, template_name='spider_list.html')

def barcode_toprint(request):
    return render(request, template_name='barcodeprint.html')

def sku_list(request):
    return render(request, template_name='sku_list.html')

def classify_analysis(request):
    return render(request, template_name='classify_analysis.html')

def quality_list(request):
    return render(request, template_name='quality_list.html')