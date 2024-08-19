# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :orders_analysis.py
@Author     :wooght
@Date       :2024/7/3 23:25
@Content    :订单数据分析
"""
from .BaseAnalysis import BaseAnalysis, np, pd
from django_pandas.io import read_frame

class OrdersAnalysis(BaseAnalysis):
    goods = pd.DataFrame()              # SKU数据
    orders = pd.DataFrame()             # 筛选SKU后的原始订单数据
    charts_data = pd.DataFrame()        # 订单图表数据 进行筛选后的isin goods bar_code后,by date后的数据
    just_chart_data = False             # 仅运行图表类
    just_orders = pd.DataFrame()        # 只有有订单价格的行

    def __init__(self, orders, start_date, end_date):
        # orders 所有订单
        self.orders = read_frame(orders)
        # 重命名,使其各数据有相同字段名
        self.orders.rename(columns={'goods_code':'bar_code','form_date':'date'}, inplace=True)
        # 时间序列 DataFrameIndex类型 freq=D 频率为天
        self.date_list = pd.date_range(start_date, end_date, freq='D')

    def order_in_goods(self, goods):
        """
            筛选属于SKU的订单
        """
        goods.drop_duplicates(['bar_code'], keep='last', inplace=True)          # 删除重复行,保留最后一项
        # 筛选属于SKU的orders
        self.orders = self.orders[self.orders['bar_code'].isin(goods['bar_code'])]
        self.goods = goods

    def check_classify(self,classify, goods):
        """
            根据类别查找订单
            params: classify_query  goods_query
            return: {chart_data:[dict]], goods_data:[dict]}
                    char_data:[{date, goods_num, rolling_30, month_mean},...]
        """
        # pandas 读取数据
        classify = read_frame(classify)
        goods = read_frame(goods)
        # 数据筛选 过滤 保留在Classify中的SKU,保留在SKU中的orders
        classify.rename(columns={'categoryId': 'category_id'}, inplace=True)
        # 筛选属于Classify的SKU
        goods = goods[goods['category_id'].isin(classify['category_id'])]       # isin 判断是否存在 参数可以是pandas/list
        self.order_in_goods(goods)
        return self.goods_pack()

    def check_goods(self, goods):
        """
            根据SKU查询订单
            params: goods_query
            return: 同上
        """
        goods = read_frame(goods)
        self.order_in_goods(goods)
        return self.goods_pack()

    def goods_pack(self):
        """
            进行订单商品数据封装
            params: orders_DataFrame
            return: {chart_data:[dict]], goods_data:[dict]}
                char_data:[{date, goods_num, rolling_30, month_mean},...]
        """
        # 按日期分组 聚合
        by_date_orders = self.orders.groupby('date')
        charts_data = by_date_orders.agg({'goods_num':'sum', 'form_money_true':'sum', 'form_money':'count'})
        # 商品平均单价
        charts_data['goods_price'] = charts_data['form_money_true'] / charts_data['goods_num']
        # 归并到时间序列上
        charts_data = pd.DataFrame(charts_data, index=self.date_list)     # 默认会根据日期类型一一对应,空值NaN填充
        charts_data['date'] = charts_data.index
        charts_data.fillna(0, inplace=True)  # NaN值替换
        # pd.set_option('display.max_rows', None)   # display.max_rows 最大显示行 None为无限制
        # 移动平均值 从第一天开始计算
        charts_data['rolling_30'] = charts_data['goods_num'].rolling(window=30, min_periods=1).mean()

        # 组装年月
        # charts_data['month'] = charts_data['date'].apply(lambda x:str(x.year)+str('%02d' % x.month))
        # charts_data['month'] = pd.Series((str(x.year)+'-'+str(x.month) for x in charts_data['date']), index=charts_data['date']))

        charts_data['month'] = charts_data['date'].dt.strftime('%Y-%m')
        # 按月求平均值 并广播到数据源
        charts_data['month_mean'] = charts_data.groupby('month')['goods_num'].transform('mean')
        # 调整小数位数
        charts_data = charts_data.round(2)
        # 调整日期格式
        charts_data['date'] = charts_data['date'].dt.strftime('%y-%m-%d')     # 最终chart_date 数据
        self.charts_data = charts_data
        if not self.just_chart_data:
            # 同比环比
            contrast_data = self.to_contrast(field='goods_num', data=charts_data)
            # SKU列表
            goods_data = self.by_goods_sale()
        else:
            contrast_data = None
            goods_data = None
        return {'chart_data':charts_data.to_dict('records'),
                'goods_data':goods_data,
                'contrast_data': contrast_data}    # records 返回行列表列字典

    def get_just_orders(self):
        """
            订单筛选,只保留有订单价格的行
        """
        self.just_orders = self.orders[self.orders['form_money_true'] > 0]
        if not isinstance(self.just_orders['date'].dtype, np.datetime64):
            self.just_orders['date'] = pd.to_datetime(self.just_orders['date'])


    def orders_pack(self):
        """
            订单数据封装
            return [{date,from_money,month,price,...},{},{},...]
        """
        # 订单筛选 只保留有订单价格的行
        just_money_data = self.just_orders.copy()
        by_date = just_money_data.groupby('date').agg({'form_money':'count', 'form_money_true':'sum'})
        by_date['price'] = by_date['form_money_true'] / by_date['form_money']
        chart_data = pd.DataFrame(by_date, index=self.date_list)    # 到这一步,就没有date字段了
        chart_data['date'] = chart_data.index
        chart_data['month'] = chart_data['date'].dt.strftime('%Y-%m')
        chart_data['date'] = chart_data['date'].dt.strftime('%Y-%m-%d')
        # 平均值
        # month_mean = chart_data.groupby('month').agg({
        #     'form_money':'mean',
        #     'form_money_true':'mean'
        # })
        # # 数据广播
        # chart_data = chart_data.merge(month_mean, on='month', how='left')
        # 广播方法时间相当
        chart_data['orders_mean'] = chart_data.groupby('month')['form_money'].transform('mean')
        chart_data['price_mean'] = chart_data.groupby('month')['price'].transform('mean')
        chart_data.fillna(0, inplace=True)
        orders_contrast = self.to_contrast(data=chart_data, field='orders_mean')
        price_contrast = self.to_contrast(data=chart_data, field='price_mean')
        return [chart_data.to_dict('records'), orders_contrast, price_contrast]

    def orders_hour(self):
        """
            订单小时数据
            params orders DataFrame
            return orders_hour:{}
        """
        orders = self.just_orders.copy()
        # to_datetime() 默认仅支持datetime 如果要支持仅有时间 必须加上format
        orders['form_time'] = pd.to_datetime(orders['form_time'], format='%H:%M:%S')
        orders['hour'] = orders['form_time'].dt.strftime('%H')
        orders['month'] = orders['date'].dt.strftime('%Y-%m')
        # 获取同比,环比月份
        need_month = self.Wdt.contrast_list()
        need_orders = orders[orders['month'].isin(need_month.keys())]
        # 筛选订单
        need_orders = need_orders[need_orders['form_money_true'] > 0]
        # 求每月有多少天数据
        by_date = need_orders.groupby('date').agg({'form_money':'count', 'month':'first'})
        by_month = by_date.groupby('month').agg({'form_money':'count'})     # 得到每月多少天数据
        # 透视图表
        need_orders = need_orders.pivot_table(values='form_money_true', index=['month'], columns=['hour'], aggfunc='count')
        need_orders = need_orders.astype('float')
        # 月时总量/天数=平均值
        for key, row in need_orders.iterrows():
            need_orders.loc[key]=need_orders.loc[key] / by_month.loc[key, 'form_money']
        need_orders.fillna(0, inplace=True)
        need_orders.columns = need_orders.columns.astype(int)
        return need_orders.to_dict('records')

    def week_7_24(self):
        """
            一周7*24小时订单分布热力图
            return week_hour:[{week_day:{0:int, 1:int,...},...},...]
        """
        orders = self.just_orders.copy()
        # 28(4周)天前日期, 这里会得到29天前数据,但因为今天不算,所以还是28天
        date_28 = self.Wdt.before_date(28)
        orders = orders[orders['date'] > date_28]
        orders['week'] = orders['date'].dt.weekday
        orders['form_time'] = pd.to_datetime(orders['form_time'], format='%H:%M:%S')
        orders['hour'] = orders['form_time'].dt.strftime('%H')
        orders['hour'] = orders['hour'].astype('int')
        # 计算周几在订单中出现了几天(避免没有数据导致平均值不准的情况)
        by_date = orders.groupby('date').agg({'goods_num':'sum', 'week':'first'})
        by_week = by_date.groupby('week').agg({'goods_num':'count'})
        by_week = pd.DataFrame(by_week, index=self.week_index)
        # week,hour生成透视表
        week_hours = orders.pivot_table(values='form_money', index='week', columns='hour', aggfunc='count')
        week_hours = pd.DataFrame(week_hours, index=self.week_index, dtype=np.float32)
        # 周时总量/天数=时平均值
        for key, row in week_hours.iterrows():
            week_hours.loc[key] = week_hours.loc[key] / by_week.loc[key, 'goods_num']
        week_hours.fillna(0, inplace=True)
        return week_hours.to_dict('records')


    def by_goods_sale(self):
        """
            按SKU分组销量
            params: orders_DataFrame    goods_DataFrame
            return: goods_dict[{sum, mean_30, sum_30, bar_code, name,...},...]
        """
        # 根据bar_code 分组
        by_bar_code = self.orders.groupby('bar_code')['goods_num'].sum()
        # 按date, bar_code 透视  得到每天每个SKU的SUM
        pivot_table = self.orders.pivot_table(values='goods_num', index=['date'], columns=['bar_code'], aggfunc='sum')
        # 组装时间序列,避免无数据不记录的情况
        pivot_table = pd.DataFrame(pivot_table, index=self.date_list)
        pivot_table.fillna(0, inplace=True)
        # 转轴(一行为一个SKU数据) 为每行求sum做准备
        pivot_table = pivot_table.transpose()
        # 拷贝得到新数据,因为sum,mean操作会新增行/列,下一步操作会多一个数据
        pivot_table_copy = pivot_table.copy()
        # 每个SKU求总SUM
        pivot_table['sum'] = pivot_table_copy.sum(axis=1)
        # 每个SKU求近30日mean,sum
        last_30 = pivot_table_copy.iloc[::,-30::]
        pivot_table['mean_30'] = last_30.mean(axis=1)
        pivot_table['sum_30'] = last_30.sum(axis=1)
        # 和goods归并,得到完整的SKU信息[销量信息,商品属性]
        goods_sale_data = pivot_table[['sum','mean_30', 'sum_30']].merge(self.goods, on='bar_code', how='left')
        return goods_sale_data.to_dict('records')


    def get_quality(self, quality=None):
        """
            保质单后销售
        """
        goods_list = []
        # quality_queryset 转goods_DataFrame
        for value in quality:
            # 字典拼接/合并
            tmp_dict = {**value['quality_goods'], **{
                'quality_id': value['id'],
                'add_date': value['add_date'],
                'date_nums': value['date_nums'],
                'then_nums': value['stock_nums'],
            }}
            goods_list.append(tmp_dict)
        quality_goods = pd.DataFrame(goods_list)
        quality_goods.drop_duplicates(['bar_code'], keep='last', inplace=True)
        orders = self.orders[self.orders['bar_code'].isin(quality_goods['bar_code'])]
        orders['date'] = pd.to_datetime(orders['date'])
        # 添加保质后销量
        quality_goods['sale_nums'] = 0
        # 通过bar_code 能找到对应的quality_goods的添加日期
        quality_goods.index = quality_goods['bar_code']
        # quality_goods.set_index('bar_code', inplace=True)     # 和上面方法一样,但会删除bar_code
        quality_goods['add_date'] = pd.to_datetime(quality_goods['add_date'])
        # 遍历订单行 iterrows() 返回的是可迭代的元祖组成的列表[(key,row),(),..]
        for index, row in orders.iterrows():
            if row.date > quality_goods.loc[row.bar_code].add_date:
                # loc 时视图引用,不能赋值 iloc,at可以赋值
                quality_goods.at[row.bar_code, 'sale_nums'] += row.goods_num

        # now_date = datetime.date.today()
        # 报错:TypeError: unsupported operand type(s) for -: 'datetime.date' and 'Timestamp'
        # 已经过了多少天
        quality_goods['spend_day'] = quality_goods['add_date'].apply(lambda x:(self.Wdt.today - x).days)
        # 保质期还剩下多少天
        quality_goods['left_day'] = quality_goods['date_nums'] - quality_goods['spend_day']
        quality_goods['add_date'] = quality_goods['add_date'].dt.strftime('%Y-%m-%d')
        return quality_goods.to_dict('records')

