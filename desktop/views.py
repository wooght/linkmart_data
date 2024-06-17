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

def summarize(request):
    return render(request, template_name='summarize.html')