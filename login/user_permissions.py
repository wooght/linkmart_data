# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :user_permissions.py
@Author     :wooght
@Date       :2024/6/17 21:15
@Content    :权限判断
"""
from rest_framework.permissions import BasePermission

class IsManagePermission(BasePermission):
    message = '权限不足'

    def has_permission(self, request, view):
        """
            是否有权限   固定格式
        """
        if request.user.is_superuser:
            # 如果是管理员,拥有所有权限
            return True
        # 判断是否是门店管理员,及是否在store_manager组里面
        groups = request.user.groups.filter(name='store_manager')
        return groups.exists()
