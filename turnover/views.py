# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :view.py
@Author     :wooght
@Date       :2024/7/8 15:38
@Content    :营业额分析视图
"""
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from desktop.models import BsData
from analysis.DateTimeMath import WDate
from analysis.TurnoverAnalysis import TurnoverAnalysis
from login.user_permissions import IsManagePermission


class TurnoverModeView(APIView):
    start_date = ''
    end_date = ''
    permissions = IsManagePermission()

    def get_queryset(self):
        store_id = self.request.COOKIES['store_id']
        self.end_date = WDate.before_day(1)[0]       # 营业额分析默认不包括当天
        self.start_date = WDate.before_day(2000)[0]
        return BsData.objects.filter(store_id=store_id, date__gt=self.start_date)

    def get(self, request):
        queryset = self.get_queryset()
        analysis = TurnoverAnalysis(queryset, self.start_date, self.end_date)
        turnover_data = analysis.turnover_pack()
        contrast_data = analysis.to_contrast('turnover', 'mean', True)
        contrast_gross_margin = analysis.to_contrast('gross_margin', 'mean', True)
        profit_data = None
        # 权限判断 有管理权限则返回利润数据
        if self.permissions.has_permission(request, self):
            profit_data = analysis.to_contrast('gross_profit', 'sum', True)

        return Response({'turnover_data': turnover_data,
                         'contrast_data': contrast_data,
                         'contrast_gross': contrast_gross_margin,
                         'profit_data':profit_data}, status=200)
