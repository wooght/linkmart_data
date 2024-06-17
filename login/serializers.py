# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :serializers.py
@Author     :wooght
@Date       :2024/6/17 18:11
@Content    :用户模块序列化器
"""

from rest_framework import serializers
from login import models

def check_name(name):
    exclude_char = ['*', '-', '\\', '/', '#']
    for char in exclude_char:
        if char in name:
            raise serializers.ValidationError('不能有特殊字符')
    return name
class LoginSerializer(serializers.ModelSerializer):
    """
        登录序列化器
    """
    uuid = serializers.CharField(label='token', read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ['nid', 'username', 'password', 'store_id', 'uuid']
        extra_kwargs = {
            'nid': {'read_only': True},
            'store_id': {'read_only': True},
            'username': {
                'min_length': 4,
                'error_messages': {'min_length': '请输入正确用户名'},
                'validators': [check_name],
            },
            'password':{
                'min_length':8,
                'error_messages':{'min_length':'密码长度不够'}
            },
        }

class UserSerializer(serializers.ModelSerializer):
    """
        注册,列表等序列化
    """
    password_again = serializers.CharField(label='验证密码', write_only=True)
    class Meta:
        model = models.UserInfo
        fields = ['nid', 'username', 'password', 'password_again', 'store_id']
        extra_kwargs = {
            'nid': {'read_only': True},
            'store_id': {'read_only': True},
            'username': {
                'min_length': 4,
                'error_messages': {'min_length': '请输入正确用户名'},
                'validators': [check_name],
            },
            'password': {
                'write_only':True,
                'min_length': 8,
                'error_messages': {'min_length': '密码长度不够'}
            }
        }

    def validate(self, attrs):
        """
            全局钩子
        """
        password = attrs.get('password')
        password_again = attrs.get('password_again')
        if password != password_again:
            raise serializers.ValidationError('两次输入密码不一样')
        return attrs

    def create(self, validated_data):
        """
            执行注册用户/创建用户
        """
        validated_data.pop('password_again')
        user = models.UserInfo.objects.create_user(**validated_data)
        return user
