from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from store.serializers import StoreSerializer
from desktop.models import StoreList
from login.user_permissions import IsManagePermission

class StoreModelViewSet(ModelViewSet):
    """
        linkmart 门店模型视图
    """
    queryset = StoreList.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsManagePermission,]