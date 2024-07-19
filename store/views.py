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

    def get_permissions(self):
        # 获取门店列表不需要权限
        if self.request.method == 'GET':
            return []
        else:
            return [permission() for permission in self.permission_classes]


"""
    linkmart 门店视图
    API: get(pk): retrieve  put(pk): update
"""
class StoreOneViewApi(RetrieveUpdateAPIView):
    queryset = StoreList.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [IsManagePermission,]