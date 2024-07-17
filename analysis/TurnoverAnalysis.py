# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :turnover_analysis.py
@Author     :wooght
@Date       :2024/7/8 15:47
@Content    :营业额数据分析
"""
from django_pandas.io import read_frame
import numpy as np
from .BaseAnalysis import BaseAnalysis, pd


class TurnoverAnalysis(BaseAnalysis):
    bs_data = pd.DataFrame()

    def __init__(self, data, start_date, end_date):
        """
            对数据进行筛选,替换,组装
            params: date_queryset, start_date_str, end_date_str
        """
        bs_data = read_frame(data)
        # 去重
        bs_data.drop_duplicates(['date'], keep='last', inplace=True)
        # 按时间排序
        bs_data.sort_values('date', ascending=True, inplace=True)
        # 日期为索引
        bs_data.index = bs_data['date']
        # 日期序列
        self.date_list = pd.date_range(start_date, end_date, freq='D')
        # 新索引,不存在则Nan代替
        self.bs_data = pd.DataFrame(bs_data, index=self.date_list)
        self.bs_data['date'] = self.bs_data.index
        # 替换控制
        self.bs_data.fillna(0, inplace=True)

    def turnover_pack(self):
        """
            进行营业额数据封装
            return: bs_data [{date,turnover,mean, ...},{},...]
        """
        # 30日移动平均值
        self.bs_data['rolling_30'] = self.bs_data['turnover'].rolling(window=30, min_periods=1).mean()
        # 月平均值
        self.set_month()
        by_month = self.bs_data.groupby('month').agg({'turnover': ['mean', 'sum'], 'gross_profit': 'sum'})
        # 广播分组数据
        self.bs_data = self.bs_data.merge(by_month['turnover'], on='month', how='left')
        # 名字重复时,会自动加X,Y,后入为Y
        self.bs_data = self.bs_data.merge(by_month['gross_profit'], on='month', how='left')
        self.bs_data['gross_margin'] = self.bs_data['sum_y'] / self.bs_data['sum_x']
        self.bs_data.fillna(0, inplace=True)
        self.bs_data = self.bs_data.round(2)
        return self.bs_data.to_dict('records')

    def profit_pack(self):
        """
            毛利额数据封装
            return: [{month,gross_profit, monty_contrast, year_contrast},...]
        """
        by_month = self.bs_data.groupby('month').agg({'gross_profit': 'sum'})
        by_month.reset_index(inplace=True)
        contrast = self.to_contrast('gross_profit', 'sum', False)
        by_month = by_month.merge(contrast, on='month', how='left')
        by_month = by_month.round(2)
        return by_month.to_dict('records')


    def set_month(self):
        """
            对月份字段进行组装
        """
        self.bs_data['month'] = self.bs_data['date'].dt.strftime('%Y-%m')
        self.bs_data['date'] = self.bs_data['date'].dt.strftime('%Y-%m-%d')
