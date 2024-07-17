# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :ClassifyAnalysis.py
@Author     :wooght
@Date       :2024/7/12 18:52
@Content    :类别数据分析
"""
from .BaseAnalysis import BaseAnalysis,pd,np
from django_pandas.io import read_frame
from .DateTimeMath import WDateTime
class ClassifyAnalysis(BaseAnalysis):
    def __init__(self, orders, classify, sku):
        """
            数据初始化
            params: orders_queryset classify_queryset, goods_queryset
            process: classify 归并到 goods, goods 归并到orders
        """
        """ 数据预处理 """
        self.orders = read_frame(orders)
        self.orders.rename(columns={'form_date':'date'}, inplace=True)  # 统一column name
        self.orders['date'] = pd.to_datetime(self.orders['date'])       # datetime
        self.sku = read_frame(sku)
        # sku 去重
        self.sku.drop_duplicates(['bar_code'], keep='last', inplace=True)
        # classify 设置categoryId为索引,方便后面通过id查询名称
        classify = read_frame(classify)
        classify.set_index('categoryId', inplace=True)
        classify['parentName'] = ''

        """ 数据组装 """
        # 修改parentID缺省值
        # print(classify.parentId.dtype)
        for key, row in classify.iterrows():
            if row['parentId'] == 0:
                # 等于自己的id和名称
                classify.at[key, 'parentId'] = row.id
                classify.at[key, 'parentName'] = classify.loc[key, 'name']
            else:
                # 等于父类的名称
                classify.at[key, 'parentName'] = classify.loc[row['parentId'], 'name']
        self.classify = classify
        # classify 归并到 goods 上
        self.sku.rename(columns={'category_id':'categoryId'}, inplace=True)
        self.sku = self.sku.merge(self.classify, on='categoryId', how='left')

        # sku 归并到 orders 上
        self.orders.rename(columns={'goods_code':'bar_code'}, inplace=True)
        self.orders = self.orders.merge(self.sku, on='bar_code', how='left')    # 带classify, goods的完整orders

    def top_classify_pack(self):
        """
            一级分类数据封装
            params: self.orders
            process: 组装month key,按month分组,透视,得到contrasted三个月的分classify goods_nums
            return: {top_classify, children_classify}
                    top_classify:[{same_month_data}, {last_month_data}, {current_month_data}]
                    children_classify:[{classify_name:goods_num},...]
        """
        orders = self.orders.copy()
        orders['month'] = orders['date'].dt.strftime('%Y-%m')
        # 获取同比,环比月份
        need_month = self.Wdt.contrast_list()
        need_orders = orders[orders['month'].isin(need_month.keys())]
        # 每月多少天数据
        days = need_orders.groupby('date').agg({'goods_num':'sum', 'month':'first'})    # 一天一条
        days_of_month = days.groupby('month').agg({'goods_num':'count'})                # 按月分组,count 得到每月天数
        # orders.goods_num 进行month,parentId 进行 透视
        pivot_orders = need_orders.pivot_table(values='goods_num', index='month', columns='parentName', aggfunc='sum')
        # 求平均值
        for key, row in pivot_orders.iterrows():
            pivot_orders.loc[key] = pivot_orders.loc[key] / days_of_month.loc[key, 'goods_num']
        pivot_orders.fillna(0, inplace=True)

        # 当前月的key值
        current_month = list(need_month.keys())[-1]
        # 对销量进行排序 倒序 columns 也可以进行排序
        pivot_orders = pivot_orders.transpose(copy=False)
        print(pivot_orders)
        pivot_orders = pivot_orders.sort_values(by=current_month, ascending=False)
        pivot_orders = pivot_orders.transpose()
        # 对当前月类别进行分组,供通过父类名称查询使用
        last_month_orders = orders[orders['month']==current_month]
        by_classify = last_month_orders.groupby('categoryName').agg({'goods_num':'sum', 'parentName':'first'})

        # 重写设置索引,让现在的索引变成一列
        by_classify.reset_index(inplace=True)
        by_classify.fillna(0, inplace=True)
        return {'top_classify':pivot_orders.to_dict('records'), 'children_classify':by_classify.to_dict('records')}

    def turnover_corr(self, turnover):
        """
            类别相关性
        """
        turnover = read_frame(turnover)
        turnover['date'] = pd.to_datetime(turnover['date'])
        turnover.drop(columns=['store'], inplace=True)
        # orders 数据分组
        orders = self.orders.copy()
        # 按date,categoryName 对goods_num进行sum透视
        orders = orders.pivot_table(values='goods_num', index='date', columns='categoryName', aggfunc='sum')
        # 将turnover 归并到 orders
        orders = orders.merge(turnover, on='date', how='left')
        orders.fillna(0, inplace=True)
        # 不进行corr的column
        dont_corr = ['id', 'date', 'turnover', 'gross_profit', 'cost']
        # 进行相关性计算
        classify_corr = pd.DataFrame()
        for column_name in orders.columns.values:
            if column_name not in dont_corr:
                classify_corr[column_name] = [orders[column_name].corr(orders['turnover'])]

        # 近一个季度相关性计算
        w_date = WDateTime()
        start_date = w_date.before_date(90)
        quarter_orders = orders[orders['date'] > start_date]
        quarter_corr = pd.DataFrame()
        for column_name in quarter_orders.columns.values:
            if column_name not in dont_corr:
                quarter_corr[column_name] = [quarter_orders[column_name].corr(quarter_orders['turnover'])]
        classify_corr.fillna(0, inplace=True)
        quarter_corr.fillna(0, inplace=True)
        return [classify_corr.to_dict('records'), quarter_corr.to_dict('records')]













