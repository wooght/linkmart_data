from django.db import models
from django.contrib.auth.models import AbstractUser
from desktop.models import StoreList


# 扩展用户表
class UserInfo(AbstractUser, models.Model):
    nid = models.AutoField(primary_key=True)
    store_id = models.ForeignKey(StoreList, on_delete=models.CASCADE, default=1)  # 所在门店id
    admin_type = models.IntegerField(default=2)  # 管理员类型 1管理员 2普通用户
    phone = models.CharField(max_length=64, blank=True)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'login_userinfo'

