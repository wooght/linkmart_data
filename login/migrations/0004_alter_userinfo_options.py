# Generated by Django 5.0.4 on 2024-06-17 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_userinfo_groups_userinfo_store_id_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'managed': False},
        ),
    ]
