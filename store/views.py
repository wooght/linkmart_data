from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from store.serializers import StoreSerializer
from desktop.models import StoreList
from login.user_permissions import IsManagePermission

"""
    linkmart 门店视图
    API: get:list   POST: Create
"""
class StoreModelViewSet(ListCreateAPIView):
    queryset = StoreList.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsManagePermission,]


"""
    linkmart 门店视图
    API: get(pk): retrieve  put(pk): update
"""
class StoreOneViewApi(RetrieveUpdateAPIView):
    queryset = StoreList.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsManagePermission]