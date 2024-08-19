# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :serializers.py
@Author     :wooght
@Date       :2024/7/3 15:19
@Content    :
"""
from rest_framework import serializers
from desktop.models import GoodsList, GoodsQuality

class GoodsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsList
        fields = '__all__'

class QualitySerializer(serializers.ModelSerializer):
    """
        保质单序列化器
    """
    # 外键对应的序列化器
    SGoods = GoodsSerializer

    # 获取外键方法
    def get_foreign_keys(self, instance):
        goods_id_serializer = self.SGoods(instance.goods)
        return goods_id_serializer.data
    # 绑定字段到外键获取方法
    quality_goods = serializers.SerializerMethodField(method_name='get_foreign_keys')

    class Meta:
        model = GoodsQuality
        fields = '__all__'
        extra_kwargs = {
            'id': {'read_only': True},
            'stock_nums': {
                'min_value': 1,
                'error_messages': {'min_value': '商品个数必填'}
            },
            'date_nums': {
                'min_value': 1,
                'error_messages': {'min_value': '剩余天数必填'}
            }
        }

    def create(self, validated_data):
        if GoodsQuality.objects.filter(goods=validated_data['goods'], state=validated_data['state']):
            raise serializers.ValidationError({'error':'已经存在'})
        else:
            return GoodsQuality.objects.create(**validated_data)

class QualityPutSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsQuality
        fields = ['id', 'state']
        extra_kwargs = {
            'id': {'read_only': True},
            'state': {
                'min_value': 2,
                'error_messages':{'min_value': '状态错误'}
            }
        }