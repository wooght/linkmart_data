# Generated by Django 5.0.4 on 2024-06-26 07:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desktop', '0005_alter_goodslist_options_alter_orderform_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodslist',
            name='category_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='goodslist',
            name='sku_id',
            field=models.CharField(default=0, max_length=32),
        ),
        migrations.AddField(
            model_name='goodslist',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='desktop.storelist'),
        ),
        migrations.AddField(
            model_name='orderform',
            name='sku_id',
            field=models.CharField(default=0, max_length=32),
        ),
    ]
