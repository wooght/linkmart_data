from django.contrib import admin
from login import models
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'store_id', 'last_login']

admin.site.register(models.UserInfo, UserAdmin)