# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :model.py
@Author     :wooght
@Date       :2024/6/17 16:59
@Content    :
"""

from django.db import models

# 营业数据
class BsData(models.Model):
    date = models.DateField()                                       # 日期
    cost = models.FloatField()                                      # 成本
    turnover = models.FloatField()                                  # 营业额
    gross_profit = models.FloatField()                              # 毛利额
    store = models.ForeignKey('StoreList', models.DO_NOTHING)   # 门店

    class Meta:
        managed = False
        db_table = 'bs_data'


class CdArea(models.Model):
    area_name = models.CharField(max_length=32)                         # 区域名称
    area_house = models.IntegerField()                                  # 户数
    area_peoples = models.IntegerField(blank=True, null=True)           # 区域人数
    area_occ_rate = models.FloatField(blank=True, null=True)            # 入住率
    area_stores = models.IntegerField(blank=True, null=True)            # 门店数量
    stores_occ_rate = models.FloatField(blank=True, null=True)          # 门店入住率
    area_consumption_rate = models.FloatField(blank=True, null=True)    # 消费概率
    area_totle_orders = models.IntegerField(blank=True, null=True)      # 订单量
    area_x = models.FloatField(blank=True, null=True)                   # x坐标
    area_y = models.FloatField(blank=True, null=True)                   # y坐标
    home_peoples = models.FloatField(blank=True, null=True)             # 户均人数

    class Meta:
        managed = False
        db_table = 'cd_area'


class CdData(models.Model):
    cd_store_id = models.IntegerField()                             # 门店ID
    cd_orders = models.IntegerField()                               # 该踩点订单量
    contrast_orders = models.IntegerField()                         # 对标门店订单量
    contrast_total_orders = models.IntegerField()                   # 对标门店当天总订单量
    home_orders = models.IntegerField(blank=True, null=True)        # 住宅提供订单量
    business_orders = models.IntegerField(blank=True, null=True)    # 商业订单量
    apartment_orders = models.IntegerField(blank=True, null=True)   # 公寓订单量
    road_orders = models.IntegerField(blank=True, null=True)        # 路人订单量
    cd_date = models.DateField(blank=True, null=True)               # 踩点日期
    cd_stime = models.TimeField(blank=True, null=True)              # 踩点时间

    class Meta:
        managed = False
        db_table = 'cd_data'


class CdLabel(models.Model):
    label_name = models.CharField(max_length=32)
    label_score = models.IntegerField()
    label_notes = models.CharField(max_length=128)
    label_type = models.IntegerField()
    f_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cd_label'


class CdStore(models.Model):
    store_name = models.CharField(max_length=32)                            # 超时名称
    cd_area = models.IntegerField()                                         # 区域ID
    store_x = models.FloatField()                                           # x坐标
    store_y = models.FloatField()                                           # y坐标
    is_24h = models.IntegerField()                                          # 是否24小时
    is_smoke = models.IntegerField()                                        # 是否有烟
    store_orders = models.IntegerField()                                    # 门店订单量
    store_turnover = models.IntegerField()                                  # 预估营业额
    contrast_orders = models.IntegerField()                                 # 对标订单量
    store_size = models.IntegerField()                                      # 门店面积
    store_waiters = models.IntegerField()                                   # 店员数量
    door_header = models.FloatField()                                       # 门头宽度
    cd_label = models.CharField(max_length=32, blank=True, null=True)       # 门店标签

    class Meta:
        managed = False
        db_table = 'cd_store'


# 商品列表
class GoodsData(models.Model):
    name = models.CharField(max_length=64)                          # 名称
    bar_code = models.CharField(max_length=32)                      # 条码
    qgp = models.IntegerField()                                     # 保质期
    store = models.ForeignKey('StoreList', models.DO_NOTHING)   # 门店ID

    class Meta:
        managed = False
        db_table = 'goods_data'


# 商品列表
class GoodsList(models.Model):
    name = models.CharField(max_length=64)                          # 名称
    bar_code = models.CharField(max_length=32)                      # 条码
    sku_id = models.CharField(max_length=32, default=0)                        # 商品美团ID
    qgp = models.IntegerField()                                     # 保质期
    store = models.ForeignKey('StoreList', models.DO_NOTHING, default=1)   # 门店ID
    classify = models.CharField(max_length=32)                      # 分类
    category_id = models.IntegerField(default=0)                             # 分类ID
    stock_nums = models.IntegerField()                              # 库存
    cost = models.FloatField(blank=True, null=True)                 # 成本
    price = models.FloatField(blank=True, null=True)                # 售价
    company = models.CharField(max_length=32, blank=True, null=True)    # 单位
    place = models.CharField(max_length=32, blank=True, null=True)      # 产地

    class Meta:
        managed = True
        db_table = 'goods_list'

# 保质检查单
class GoodsQuality(models.Model):
    goods_code = models.CharField(max_length=32)                # 条码
    stock_nums = models.IntegerField()                          # 数量
    date_nums = models.IntegerField()                           # 剩余天数
    add_date = models.DateField()                               # 添加日期
    state = models.IntegerField()                               # 当前状态
    store_id = models.IntegerField()                            # 门店ID
    goods = models.ForeignKey(GoodsList, models.DO_NOTHING)     # 对应商品

    class Meta:
        managed = False
        db_table = 'goods_quality'


class HuayuBusinessdata(models.Model):
    date = models.DateField()
    cost = models.FloatField()
    turnover = models.FloatField()
    gross_profit = models.FloatField()

    class Meta:
        managed = False
        db_table = 'huayu_businessdata'


class Operate(models.Model):
    store_id = models.IntegerField()
    y_month = models.CharField(max_length=8)
    profit = models.FloatField()
    income = models.FloatField()
    wages = models.FloatField()
    insurance = models.FloatField()
    meituan = models.FloatField()
    rent = models.FloatField()
    hydropower = models.FloatField()
    expenditure = models.FloatField()
    stock = models.FloatField()
    assets = models.FloatField()
    loss = models.FloatField()
    mk_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'operate'


# 订单列表
class OrderForm(models.Model):
    form_code = models.CharField(max_length=32)     # 订单号
    goods_name = models.CharField(max_length=64)    # 商品名称
    goods_code = models.CharField(max_length=64)    # 商品条码
    sku_id = models.CharField(max_length=32, default=0)        # 商品美团ID
    goods_num = models.IntegerField()               # 商品数量
    goods_money = models.FloatField()               # 商品金额
    form_date = models.DateField()                  # 日期
    form_time = models.TimeField()                  # 时间
    form_money = models.FloatField()                # 订单金额
    form_money_true = models.FloatField()           # 实付金额
    store_id = models.IntegerField()                # 门店ID
    # vip = models.SmallIntegerField(default=0)       # 是否VIP

    class Meta:
        managed = True
        db_table = 'order_form'


class StockWidthGoods(models.Model):
    goods_code = models.CharField(max_length=32)
    state = models.IntegerField()
    stock_type = models.IntegerField()
    add_date = models.DateField()
    store_id = models.IntegerField()
    goods = models.ForeignKey(GoodsList, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'stock_width_goods'

# 门店列表
class StoreList(models.Model):
    name = models.TextField()       # 名字
    adds = models.TextField()       # 地址
    mt_number = models.CharField(max_length=32, default='00')     # 美团编号
    mt_user = models.CharField(max_length=32, default='00')       # 美团账号
    mt_password = models.TextField(default='12345678')            # 美团密码

    class Meta:
        managed = True
        db_table = 'store_list'

class GoodsClassify(models.Model):
    store_id = models.IntegerField()            # 门店ID
    name = models.CharField(max_length=32)                   # 名称
    parentId = models.IntegerField()            # 父级ID
    categoryName = models.CharField(max_length=32)           # 名称
    categoryId = models.IntegerField()          # ID
    parentCategoryId = models.IntegerField()    # 父级ID

    class Meta:
        managed = False
        db_table = 'goods_classify'
