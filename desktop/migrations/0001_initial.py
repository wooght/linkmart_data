# Generated by Django 5.0.4 on 2024-06-17 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cost', models.FloatField()),
                ('turnover', models.FloatField()),
                ('gross_profit', models.FloatField()),
            ],
            options={
                'db_table': 'bs_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CdArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area_name', models.CharField(max_length=32)),
                ('area_house', models.IntegerField()),
                ('area_peoples', models.IntegerField(blank=True, null=True)),
                ('area_occ_rate', models.FloatField(blank=True, null=True)),
                ('area_stores', models.IntegerField(blank=True, null=True)),
                ('stores_occ_rate', models.FloatField(blank=True, null=True)),
                ('area_consumption_rate', models.FloatField(blank=True, null=True)),
                ('area_totle_orders', models.IntegerField(blank=True, null=True)),
                ('area_x', models.FloatField(blank=True, null=True)),
                ('area_y', models.FloatField(blank=True, null=True)),
                ('home_peoples', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cd_area',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CdData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cd_store_id', models.IntegerField()),
                ('cd_orders', models.IntegerField()),
                ('contrast_orders', models.IntegerField()),
                ('contrast_total_orders', models.IntegerField()),
                ('home_orders', models.IntegerField(blank=True, null=True)),
                ('business_orders', models.IntegerField(blank=True, null=True)),
                ('apartment_orders', models.IntegerField(blank=True, null=True)),
                ('road_orders', models.IntegerField(blank=True, null=True)),
                ('cd_date', models.DateField(blank=True, null=True)),
                ('cd_stime', models.TimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cd_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CdLabel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label_name', models.CharField(max_length=32)),
                ('label_score', models.IntegerField()),
                ('label_notes', models.CharField(max_length=128)),
                ('label_type', models.IntegerField()),
                ('f_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'db_table': 'cd_label',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='CdStore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=32)),
                ('cd_area', models.IntegerField()),
                ('store_x', models.FloatField()),
                ('store_y', models.FloatField()),
                ('is_24h', models.IntegerField()),
                ('is_smoke', models.IntegerField()),
                ('store_orders', models.IntegerField()),
                ('store_turnover', models.IntegerField()),
                ('contrast_orders', models.IntegerField()),
                ('store_size', models.IntegerField()),
                ('store_waiters', models.IntegerField()),
                ('door_header', models.FloatField()),
                ('cd_label', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'db_table': 'cd_store',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GoodsData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('bar_code', models.CharField(max_length=32)),
                ('qgp', models.IntegerField()),
            ],
            options={
                'db_table': 'goods_data',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GoodsList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('bar_code', models.CharField(max_length=32)),
                ('qgp', models.IntegerField()),
                ('classify', models.CharField(max_length=32)),
                ('stock_nums', models.IntegerField()),
                ('cost', models.FloatField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('company', models.CharField(blank=True, max_length=32, null=True)),
                ('place', models.CharField(blank=True, max_length=32, null=True)),
            ],
            options={
                'db_table': 'goods_list',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GoodsQuality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_code', models.CharField(max_length=32)),
                ('stock_nums', models.IntegerField()),
                ('date_nums', models.IntegerField()),
                ('add_date', models.DateField()),
                ('state', models.IntegerField()),
                ('store_id', models.IntegerField()),
            ],
            options={
                'db_table': 'goods_quality',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HuayuBusinessdata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('cost', models.FloatField()),
                ('turnover', models.FloatField()),
                ('gross_profit', models.FloatField()),
            ],
            options={
                'db_table': 'huayu_businessdata',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Operate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.IntegerField()),
                ('y_month', models.CharField(max_length=8)),
                ('profit', models.FloatField()),
                ('income', models.FloatField()),
                ('wages', models.FloatField()),
                ('insurance', models.FloatField()),
                ('meituan', models.FloatField()),
                ('rent', models.FloatField()),
                ('hydropower', models.FloatField()),
                ('expenditure', models.FloatField()),
                ('stock', models.FloatField()),
                ('assets', models.FloatField()),
                ('loss', models.FloatField()),
                ('mk_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'operate',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='OrderForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_code', models.CharField(max_length=32)),
                ('goods_name', models.CharField(max_length=64)),
                ('goods_code', models.CharField(max_length=64)),
                ('goods_num', models.IntegerField()),
                ('goods_money', models.FloatField()),
                ('form_date', models.DateField()),
                ('form_time', models.TimeField()),
                ('form_money', models.FloatField()),
                ('form_money_true', models.FloatField()),
                ('store_id', models.IntegerField()),
            ],
            options={
                'db_table': 'order_form',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StockWidthGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_code', models.CharField(max_length=32)),
                ('state', models.IntegerField()),
                ('stock_type', models.IntegerField()),
                ('add_date', models.DateField()),
                ('store_id', models.IntegerField()),
            ],
            options={
                'db_table': 'stock_width_goods',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='StoreList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('adds', models.TextField()),
            ],
            options={
                'db_table': 'store_list',
                'managed': False,
            },
        ),
    ]
