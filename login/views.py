# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :views.py
@Author     :wooght
@Date       :2024/6/17 13:32
@Content    :登录模块VIEWAPI
"""
from rest_framework.response import Response        # Response 返回能序列化的Response
from login.serializers import LoginSerializer, UserSerializer, UpdatePasswordSerializer
from rest_framework.views import APIView            # rest_framework 视图基类
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from django.contrib import auth                     # django 认证
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token   # rest framework Token 认证
from rest_framework.filters import OrderingFilter
from login.user_permissions import IsManagePermission
from login.models import UserInfo
import datetime

"""
    用户登录/修改/个人视图
    API: post:post  put:put     get:get
"""
class LoginAPIView(APIView):
    # permission_classes = []     # 指定权限为空,登录不需要权限

    def get_permissions(self):
        if self.request.method == 'POST':
            return []       # 登录不需要权限
        else:
            # 获取个人信息,修改密码为登录即可操作
            return [permission() for permission in self.permission_classes]


    def post(self, request):
        """
            POST登录
        """
        # 创建序列化器
        serializer_obj = LoginSerializer(data=request.data, partial=True)
        # 验证提交数据
        if serializer_obj.is_valid():
            # 数据库验证提交数据
            verify = auth.authenticate(**serializer_obj.validated_data)
            if verify:
                # auth.login(request, verify)   session 认证,会自动修改最近登录时间
                # 删除旧的Token
                old_token = Token.objects.filter(user=verify)
                old_token.delete()
                # 创建新的Token
                new_token = Token.objects.create(user=verify)
                # 将Token key 写入登录验证后的对象
                setattr(verify, 'uuid', new_token.key)
                # 修改登录时间
                now_date = datetime.datetime.now()
                serializer_obj.update(instance=verify, validated_data={'last_login':now_date})
                # 登录数据序列化
                instance = LoginSerializer(instance=verify, partial=True)
                return Response(instance.data)
            else:
                return Response({'error':'用户名或者密码错误'}, status=400)
        else:
            return Response(serializer_obj.errors, status='400')

    def put(self, request):
        """
            修改密码
            获取当前username与POST数据组装,然后提交给serializer
            serializer验证后,给auth.authenticate验证()
            auth通过后,make_password(new_password)获取新密码
            serializer.update(instance, validated_data) 保存数据 validated_data为要修改数据
        """
        # dict(request.data) 得到的数据格式为 {key:[value], ...}
        submit_data = {key: value[0] for key, value in dict(request.data).items()}
        # 由于提交的数据没有username, 这里获取当前登录者的username
        submit_data['username'] = request.user.username
        # 进行序列化验证 partial /ˈpɑːʃl/  部分的 =True  没有全部字段
        serializer_obj = UpdatePasswordSerializer(data=submit_data, partial=True)
        if serializer_obj.is_valid():
            verify = auth.authenticate(username=submit_data['username'], password=submit_data['password'])
            if verify:
                # 对密码进行加密
                new_password = make_password(submit_data['new_password'])
                # 修改密码
                serializer_obj.update(instance=verify, validated_data={'password': new_password})
                return Response({'status': '修改成功'})
            else:
                return Response({'error': '密码错误'}, status=400)
        else:
            return Response(serializer_obj.errors, status=400)

    def get(self, request):
        instance = LoginSerializer(instance=request.user, partial=True)
        return Response(instance.data)


"""
    用户注册/列表视图
    API:    post:post   get:list
    需要管理员权限
"""
class UserModelViewApi(ViewSet, ListAPIView):
    permission_classes = [IsManagePermission,]
    serializer_class = UserSerializer
    queryset = UserInfo.objects.all()
    filter_backends = [OrderingFilter]
    ordering_fields = ['nid', ]  # 可排序的字段 /?ordering=-nid 倒序

    # 序列化选择
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LoginSerializer
        else:
            return UserSerializer

    def add_one(self, request):
        """
            注册新用户
        """
        serializer_obj = self.get_serializer(data=request.data, partial=True)
        if serializer_obj.is_valid():
            serializer_obj.save()
            return Response(serializer_obj.data)
        else:
            return Response(serializer_obj.errors, status=400)



