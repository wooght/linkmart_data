# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :serializers.py
@Author     :wooght
@Date       :2024/6/17 21:25
@Content    :linkmart 门店序列化
"""

from rest_framework.serializers import ModelSerializer
from desktop.models import StoreList

class StoreSerializer(ModelSerializer):
    """
        linkmart 门店
    """
    class Meta:
        model = StoreList
        fields = ['id', 'name', 'adds']
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {
                'min_length': 4,
                'error_messages': {'min_length': '名字太短'},
            }
        }
