# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :caidian_odds.py
@Author     :wooght
@Date       :2024/6/18 20:01
@Content    :踩点数据分析
"""
import pandas as pd
from django_pandas.io import read_frame


def json_to_dict(data, key):
    result = {}
    for value in data.values():
        result[value[key]] = value
    return result


def caidian_odds(area, store, data):
    """
        计算消费概率
    """
    pd_area = pd.DataFrame(area)  # 区域
    pd_store = read_frame(store)  # 门店
    pd_caidian = read_frame(data)  # 踩点数据

    """
        计算每个门店的总订单及预估订单
    """
    # 分组聚合
    by_store_caidian = pd_caidian.groupby('cd_store_id')
    store_caidian = by_store_caidian.agg(
        {'cd_orders': 'sum', 'contrast_orders': 'sum', 'contrast_total_orders': 'mean'})
    # 重命名列
    store_caidian['store_id'] = store_caidian.index
    store_caidian.rename(columns={'contrast_orders': 'contrast_caidian'}, inplace=True)
    pd_store.rename(columns={'id': 'store_id'}, inplace=True)
    # 归并 门店 < 门店踩点数据
    store_orders = pd_store.merge(store_caidian, how='left', on='store_id')
    # 替换nan值
    store_orders.fillna(value=0, inplace=True)
    is_24 = [0.72, 1, 0.85]
    # 踩点单量/对标单量*对标日单量*24H占比 部分没有踩点量,就采用填入的订单量
    # 这里得到要返回的门店数据
    store_orders['store_orders'] = store_orders.apply(
        lambda row: row['cd_orders'] / row['contrast_caidian'] * row['contrast_orders'] * is_24[row['is_24h']] \
            if row['cd_orders'] > 0 else row['store_orders'], axis=1)
    store_orders['store_orders'] = store_orders['store_orders'].round(0)
    """
        将门店数据按照区域ID分组
    """
    by_area = store_orders.groupby('cd_area')
    area_caidian = by_area.agg({'store_orders': 'sum'})
    area_caidian['id'] = area_caidian.index
    # 归并    商圈 < 门店数据
    area_orders = pd_area.merge(area_caidian, how='left', on='id')
    # 商圈总人口 入住率*户数*户均+门店入住率*门店数*5
    area_orders['population'] = area_orders['area_occ_rate'] * area_orders['area_house'] * area_orders['home_peoples'] + \
                                area_orders['stores_occ_rate'] * area_orders['area_stores'] * 5
    # 消费概率 订单/人口
    area_orders['odds'] = area_orders['store_orders'] / area_orders['population']
    area_orders['odds'] = area_orders['odds'].round(2)
    area_orders.fillna(value=0, inplace=True)
    # pd.set_option('display.max_rows', None)               # 最大显示行数 无穷
    # print(area_orders[['store_orders', 'population']])    # 显示指定多列
    # to_dict 参数:records 构建一个列表,每行形成一个字典 参数:dict 默认,返回列字典
    return store_orders.to_dict('records'), area_orders.to_dict('records')
