# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :BaseAnalysis.py
@Author     :wooght
@Date       :2024/7/12 18:00
@Content    :数据分析基类
"""
import pandas as pd
import numpy as np
from .DateTimeMath import WDateTime
class BaseAnalysis(object):
    bs_data = pd.DataFrame()        # 要进行分析的数据主体
    week_index = np.arange(0,7)     # 一周索引
    Wdt = WDateTime()

    def to_contrast(self, field, method='mean', to_dict=True, data=None):
        """
            同比, 环比
            return: contrast [{month, field, month_contrast, year_contrast},{},...]
        """
        bs_data = data if isinstance(data, pd.DataFrame) else self.bs_data
        # 按月分组
        by_month = bs_data.groupby('month').agg({field: method})
        # 与前值之差
        diff_1 = by_month[field].diff()
        diff_12 = by_month[field].diff(12)

        # 前值
        front_1 = by_month[field].shift()
        front_12 = by_month[field].shift(12)

        # 计算同比,环比
        by_month['month_contrast'] = (diff_1 / front_1).round(4)
        by_month['year_contrast'] = (diff_12 / front_12).round(4)
        # 空值填充 包括 inf
        by_month.replace([np.inf, -np.inf], np.nan, inplace=True)
        by_month.fillna(0, inplace=True)
        # 重置索引,会把现在的索引变成一列,然后从0开始索引
        by_month.reset_index(inplace=True)
        return by_month.to_dict('records') if to_dict else by_month
