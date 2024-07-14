# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :serializers.py
@Author     :wooght
@Date       :2024/6/17 18:11
@Content    :用户模块序列化器
"""

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from login import models
from store.serializers import StoreSerializer

def check_name(name):
    exclude_char = ['*', '-', '\\', '/', '#']
    # UniqueValidator 同样功能
    # all_user = models.UserInfo.objects.all()
    # name_lists = [row.username for row in all_user]
    # if name in name_lists:
    #     raise serializers.ValidationError('用户名已经存在')
    for char in exclude_char:
        if char in name:
            raise serializers.ValidationError('不能有特殊字符')
    return name

class LoginSerializer(serializers.ModelSerializer):
    """
        登录序列化器
    """
    uuid = serializers.CharField(label='token', read_only=True)
    new_password = serializers.CharField(label='新密码', write_only=True)
    confirm_password = serializers.CharField(write_only=True, label='确认密码')
    # 外检对应的序列化器
    SStore = StoreSerializer

    def get_foreign_keys(self, instance):
        """
            获取外键关联信息
            外检关联对应的序列化器serializer(instance.foreign_key)
        """
        store_id_serializer = self.SStore(instance.store_id)
        return store_id_serializer.data
    # 获取外键字段
    store_name = serializers.SerializerMethodField(method_name='get_foreign_keys')

    class Meta:
        model = models.UserInfo
        fields = ['nid', 'username', 'password', 'store_id', 'uuid', 'store_name', 'last_login',
                  'new_password', 'confirm_password']
        extra_kwargs = {
            'nid': {'read_only': True},
            'store_id': {'read_only': True},
            'last_login': {'read_only':True},
            'username': {
                'min_length': 4,
                'error_messages': {'min_length': '请输入正确用户名'},
                'validators': [check_name],
            },
            'password':{
                'write_only':True,
                'min_length':8,
                'error_messages':{'min_length':'密码格式错误'}
            },
        }

    def validate(self, attrs):
        new_pas = attrs.get('new_password')
        confirm_pas = attrs.get("confirm_password")
        if new_pas != confirm_pas:
            raise serializers.ValidationError('两次输入密不一样')
        return attrs


class UserSerializer(serializers.ModelSerializer):
    """
        注册序列化
    """
    password_again = serializers.CharField(label='验证密码', write_only=True)

    class Meta:
        model = models.UserInfo
        fields = ['nid', 'username', 'password', 'password_again', 'store_id']
        extra_kwargs = {
            # 'nid': {'read_only': True},
            'username': {
                'min_length': 4,
                'error_messages': {'min_length': '请输入正确用户名'},
                # user 模型默认有 validators 进行去重判断
                # 如果是登录,则需要替换掉,所有user表登录时必须重新声明validators
                'validators': [check_name, UniqueValidator(queryset=models.UserInfo.objects.all(), message='用户名已经存在')],
            },
            'password': {
                'write_only':True,
                'min_length': 8,
                'error_messages': {'min_length': '密码长度不够', 'blank':'未填写密码'}
            },
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

class UpdatePasswordSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(label='新密码', write_only=True)
    confirm_password = serializers.CharField(write_only=True, label='确认密码')

    class Meta:
        model = models.UserInfo
        new_password = serializers.CharField(write_only=True)
        confirm_password = serializers.CharField(write_only=True)

        fields = ['nid', 'username', 'password', 'new_password', 'confirm_password']

        extra_kwargs = {
            'nid': {'read_only':True},
            'password':{
                'write_only':True,
                'min_length': 1,
                'error_messages':{'min_length':'密码长度不够', 'blank':'密码必填'}
            },
            'username':{'validators':[check_name,]},
            'new_password':{
                'write_onely':True,
                'min_length':8,
                'error_messages':{'min_length':'新密码长度不够', 'blank':'新密码未填写'},
            }   # 不起作用的原因 不是数据库字段?
        }

    def validate(self, attrs):
        new_pas = attrs.get('new_password')
        confirm_pas = attrs.get("confirm_password")
        if new_pas != confirm_pas:
            raise serializers.ValidationError('两次输入密不一样')
        elif len(new_pas) < 8:
            raise serializers.ValidationError('新密码长度不够')
        return attrs
