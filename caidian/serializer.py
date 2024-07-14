# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :serializer.py
@Author     :wooght
@Date       :2024/6/18 16:13
@Content    :踩点数据序列化器
"""
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from desktop import models

# 踩点商圈序列化器
class CaiDianAreaSerializer(ModelSerializer):
    class Meta:
        model = models.CdArea
        fields = '__all__'
        extra_kwargs = {
            # 'id': {'read_only', True},
            'area_name': {
                'min_length': 4,
                'error_messages': {'min_length': '名称不规范', 'blank': '名称不能为空'},
            },
            'area_x': {
                'error_messages': {'blank': '坐标不能为空'}
            }
        }

    def validate(self, attrs):
        x = str(attrs.get('area_x'))
        y = str(attrs.get('area_y'))
        if len(x) < 5 or len(y) < 5:
            raise serializers.ValidationError('坐标填写有误')
        return attrs


# 踩点门店标签序列化器
class CaiDianLabelSerializer(ModelSerializer):
    class Meta:
        model = models.CdLabel
        fields = '__all__'

# 踩点数据序列化器
class CaiDianDataSerializer(ModelSerializer):
    class Meta:
        model = models.CdData
        fields = '__all__'

# 踩点门店序列化器
class CaiDianStoreSerializer(ModelSerializer):

    class Meta:
        model = models.CdStore
        fields = '__all__'

        extra_kwargs = {
            'store_name':{
                'min_length': 4,
                'error_messages':{'min_length':'名称太短'},
            },
        }

    def validate(self, attrs):
        x = str(attrs.get('store_x'))
        y = str(attrs.get('store_y'))
        if len(x) < 5 or len(y) < 5:
            raise serializers.ValidationError('坐标填写有误')
        return attrs
