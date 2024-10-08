# -- coding: utf-8 -
"""
@project    :
@file       :urls.py
@Author     :wooght
@Date       :2024/6/9 16:20
@Content    :
"""
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=80)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


class BsData(models.Model):
    date = models.DateField()
    cost = models.FloatField()
    turnover = models.FloatField()
    gross_profit = models.FloatField()
    store = models.ForeignKey('StoreList', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bs_data'


class CdArea(models.Model):
    area_name = models.CharField(max_length=32)
    area_house = models.IntegerField()
    area_peoples = models.IntegerField(blank=True, null=True)
    area_occ_rate = models.FloatField(blank=True, null=True)
    area_stores = models.IntegerField(blank=True, null=True)
    stores_occ_rate = models.FloatField(blank=True, null=True)
    area_consumption_rate = models.FloatField(blank=True, null=True)
    area_totle_orders = models.IntegerField(blank=True, null=True)
    area_x = models.FloatField(blank=True, null=True)
    area_y = models.FloatField(blank=True, null=True)
    home_peoples = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cd_area'


class CdData(models.Model):
    cd_store_id = models.IntegerField()
    cd_orders = models.IntegerField()
    contrast_orders = models.IntegerField()
    contrast_total_orders = models.IntegerField()
    home_orders = models.IntegerField(blank=True, null=True)
    business_orders = models.IntegerField(blank=True, null=True)
    apartment_orders = models.IntegerField(blank=True, null=True)
    road_orders = models.IntegerField(blank=True, null=True)
    cd_date = models.DateField(blank=True, null=True)
    cd_stime = models.TimeField(blank=True, null=True)

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
    store_name = models.CharField(max_length=32)
    cd_area = models.IntegerField()
    store_x = models.FloatField()
    store_y = models.FloatField()
    is_24h = models.IntegerField()
    is_smoke = models.IntegerField()
    store_orders = models.IntegerField()
    store_turnover = models.IntegerField()
    contrast_orders = models.IntegerField()
    store_size = models.IntegerField()
    store_waiters = models.IntegerField()
    door_header = models.FloatField()
    cd_label = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cd_store'


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey('LoginUserinfo', models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()
#
#     class Meta:
#         managed = False
#         db_table = 'django_session'


class GoodsData(models.Model):
    name = models.CharField(max_length=64)
    bar_code = models.CharField(max_length=32)
    qgp = models.IntegerField()
    store = models.ForeignKey('StoreList', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'goods_data'


class GoodsList(models.Model):
    name = models.CharField(max_length=64)
    bar_code = models.CharField(max_length=32)
    qgp = models.IntegerField()
    store = models.ForeignKey('StoreList', models.DO_NOTHING)
    classify = models.CharField(max_length=32)
    stock_nums = models.IntegerField()
    cost = models.FloatField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    company = models.CharField(max_length=32, blank=True, null=True)
    place = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'goods_list'


class GoodsQuality(models.Model):
    goods_code = models.CharField(max_length=32)
    stock_nums = models.IntegerField()
    date_nums = models.IntegerField()
    add_date = models.DateField()
    state = models.IntegerField()
    store_id = models.IntegerField()
    goods = models.ForeignKey(GoodsList, models.DO_NOTHING)

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


class LoginUserinfo(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    nid = models.AutoField(primary_key=True)
    admin_type = models.IntegerField()
    phone = models.CharField(max_length=64)
    create_date = models.DateTimeField()
    store_id = models.ForeignKey('StoreList', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'login_userinfo'


# class LoginUserinfoGroups(models.Model):
#     userinfo = models.ForeignKey(LoginUserinfo, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'login_userinfo_groups'
#         unique_together = (('userinfo', 'group'),)


# class LoginUserinfoUserPermissions(models.Model):
#     userinfo = models.ForeignKey(LoginUserinfo, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
#
#     class Meta:
#         managed = False
#         db_table = 'login_userinfo_user_permissions'
#         unique_together = (('userinfo', 'permission'),)


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


class OrderForm(models.Model):
    form_code = models.CharField(max_length=32)
    goods_name = models.CharField(max_length=64)
    goods_code = models.CharField(max_length=64)
    goods_num = models.IntegerField()
    goods_money = models.FloatField()
    form_date = models.DateField()
    form_time = models.TimeField()
    form_money = models.FloatField()
    form_money_true = models.FloatField()
    store_id = models.IntegerField()

    class Meta:
        managed = False
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


class StoreList(models.Model):
    name = models.TextField()
    adds = models.TextField()

    class Meta:
        managed = False
        db_table = 'store_list'
