# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :serializer.py
@Author     :wooght
@Date       :2024/6/18 16:13
@Content    :踩点数据视图
"""
from caidian import serializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from desktop import models
from analysis.caidian_odds import caidian_odds
from login.user_permissions import IsManagePermission

""" 
    商圈视图
    API: get:list,  get(pk):retrieve    post:create     put(pk):update
"""
class CaiDianAreaAPIView(ModelViewSet):
    pagination_class = None                                 # 禁止翻页功能
    serializer_class = serializer.CaiDianAreaSerializer     # 序列化器
    queryset = models.CdArea.objects.all()                  # queryset 查询数据集
    permission_classes = [IsManagePermission,]

    def list(self, request, *args, **kwargs):
        """
            return 数据结构:
                [
                    [store_data, store_data,...],
                    [area_data, area_data,...]
                ]
        """
        # 将所有商圈进行序列化
        serializer_obj = self.get_serializer(self.queryset, many=True)
        # 获取所有踩点数据,门店数据
        cd_data = models.CdData.objects.all()
        cd_store = models.CdStore.objects.all()
        # 数据运算:踩点数据 ->归并 门店 ->归并 商圈
        store_orders, area_orders = caidian_odds(serializer_obj.data, cd_store, cd_data)
        # 有翻页功能, 这里就没法输出?
        return Response([store_orders, area_orders])


"""
    踩点门店视图
    API:    get:list       post:create     put(pk):update
"""
class CaiDianStoreAPIView(generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView):
    pagination_class = None
    queryset = models.CdStore.objects.all()
    serializer_class = serializer.CaiDianStoreSerializer
    permission_classes = [IsManagePermission,]

    # def update(self, request, *args, **kwargs):
    #     print(pk)
    #     serializer_obj = self.get_serializer(data=request.data)
    #     if serializer_obj.is_valid():
    #         print(serializer_obj.validated_data)
    #         serializer_obj.update(instance=serializer_obj.data, validated_data=serializer_obj.validated_data)
    #         return Response({'status':'ok'})
    #     else:
    #         return Response({'status':'修改失败'}, status=400)


"""
    门店描述标签视图
    API:    get:list
"""
class CaiDianLabelAPIView(generics.ListAPIView):
    pagination_class = None
    serializer_class = serializer.CaiDianLabelSerializer
    queryset = models.CdLabel.objects.all()
    permission_classes = [IsManagePermission,]

"""
    踩点数据视图
    API:    get(pk):list    post:create
"""
class CaiDianDataAPIView(generics.ListAPIView, generics.CreateAPIView):
    pagination_class = None
    serializer_class = serializer.CaiDianDataSerializer
    queryset = models.CdData.objects.all()
    permission_classes = [IsManagePermission,]

    def get_queryset(self):
        """
            重写 get_queryset()
            return: 过滤后的queryset
        """
        queryset = super().get_queryset()
        # 获取get 传参
        store_id = self.request.query_params.get('pk')
        if store_id:
            # filter过滤
            queryset = queryset.filter(cd_store_id=store_id)
        return queryset
