"""
URL configuration for linkmart_data project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from desktop import views
from store.views import StoreModelViewSet

urlpatterns = [
    path('', views.index),                              # 首页
    path('admin/', admin.site.urls),                    # 后台
    path('desktop/', include('desktop.urls')),          # 页面
    path('userauth/', include('login.urls')),           # 用户API
    path('store/', StoreModelViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),

]
