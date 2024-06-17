# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :views.py
@Author     :wooght
@Date       :2024/6/17 13:32
@Content    :登录模块VIEWAPI
"""
from rest_framework.response import Response        # Response 返回能序列化的Response
from login.serializers import LoginSerializer, UserSerializer
from rest_framework.views import APIView            # rest_framework 视图基类
from rest_framework.viewsets import ModelViewSet
from django.contrib import auth                     # django 认证
from rest_framework.authtoken.models import Token   # rest framework Token 认证
from login.user_permissions import IsManagePermission
from login.models import UserInfo

class LoginAPIView(APIView):
    print('kkkk')
    permission_classes = []     # 指定权限为空,登录不需要权限

    def post(self, request):
        """
            POST登录
        """
        # 创建序列化器
        serializer_obj = LoginSerializer(data=request.data)
        # 验证提交数据
        if serializer_obj.is_valid():
            # 数据库验证提交数据
            verify = auth.authenticate(**serializer_obj.validated_data)
            if verify:
                # 删除旧的Token
                old_token = Token.objects.filter(user=verify)
                old_token.delete()
                # 创建新的Token
                new_token = Token.objects.create(user=verify)
                # 将Token key 写入登录验证后的对象
                setattr(verify, 'uuid', new_token.key)
                # 登录数据序列化
                instance = LoginSerializer(instance=verify)
                return Response(instance.data)
            else:
                return Response({'error':'用户名或者密码错误'})
        else:
            return Response(serializer_obj.errors, status='400')

class UserModelViewApi(ModelViewSet):
    permission_classes = [IsManagePermission,]
    serializer_class = UserSerializer
    queryset = UserInfo.objects.all()

    def add_one(self, request):
        """
            注册新用户
        """
        serializer_obj = self.get_serializer(data=request.data, partial=True)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data)
        else:
            return Response(serializer_obj.errors)
