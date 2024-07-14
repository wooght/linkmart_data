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
from analysis.SecretCode import Wst

class StoreSerializer(ModelSerializer):
    """
        linkmart 门店
    """
    class Meta:
        model = StoreList
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'name': {
                'min_length': 4,
                'error_messages': {'min_length': '名字太短', 'blank':'名字不能为空'},
            },
        }

    # 序列化时对字段进行额外操作
    def to_representation(self, instance):
        """
            对密码进行解密
        """
        representation = super().to_representation(instance)
        representation['mt_password'] = Wst.decryption(representation['mt_password'])
        return representation

    # 反序列化时对字段进行额外操作
    def to_internal_value(self, data):
        """
            对密码进行加密
        """
        internal_value = super().to_internal_value(data)
        internal_value['mt_password'] = Wst.encryption(data['mt_password'])
        return internal_value
