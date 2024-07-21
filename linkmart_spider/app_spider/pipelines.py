# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from typing import Dict, Any

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from app_spider.items import ClassifyItem, GoodsItem, OrderFormItem, TurnoverFormItem
from app_spider import models
from common.DateTimeMath import WDate


class AppSpiderPipeline:
    goods_tmp = {}       # 已经存在商品{code:goods,...}
    exists_code = []         # 已经存在的商品所有[code,....]
    all_orders = []
    exists_turnover = []
    store_id = 0
    classify = {}

    def __init__(self, *args, **kwargs):
        super(AppSpiderPipeline, self).__init__(*args, **kwargs)
        print('pipeline 管道初始化')

    def get_goods(self, is_sku = False):
        """
            获取SKU,并设置exists数据
            goods_tmp: {sku_id:goods}
            exists_code: [sku_id]
            all_orders: [form_code]
        """
        all_goods = models.db.query(models.Goods).filter(models.Goods.store_id == self.store_id).all()
        if is_sku:
            # 返回sku_id 对应的字典    {sku_id:goods,...}
            goods_tmp = {goods.sku_id:goods for goods in all_goods}
            # 进一月的订单
            form_codes = models.db.query(models.OrderForm.form_code).filter(
                models.OrderForm.store_id == self.store_id, models.OrderForm.form_date >= WDate.before_day(30)[0])
            self.all_orders = [form_code.form_code for form_code in form_codes]
        else:
            # 返回bar_code 对应的字典 {bar_code:goods, ...}
            goods_tmp = {goods.bar_code: goods for goods in all_goods}
        exists_code = goods_tmp.keys()
        self.goods_tmp = goods_tmp
        self.exists_code = exists_code


    def set_base_data(self, spider):
        print('spider{}启动成功'.format(spider.name))
        if spider.name == 'goods':
            self.get_goods()
        elif spider.name == 'orderform':
            # 获取已经存在的订单
            self.get_goods(is_sku=True)
        elif spider.name == 'turnover':
            # 获取历史营业额
            turnover_query = models.db.query(models.Turnover).filter(
                models.Turnover.store_id == self.store_id,
                models.Turnover.date >= WDate.before_day(365)[0]
            )
            # isoformat datetime 转换为符合ISO(YYYY-MM-DD)的字符串
            self.exists_turnover = [item.date.isoformat() for item in turnover_query]
        elif spider.name == 'classify':
            # 初始获取商品类别
            goods_classify = models.db.query(models.GoodsClassify).filter_by(store_id=self.store_id).all()
            for item in goods_classify:
                self.classify[item.categoryId] = item.name


    def process_item(self, item, spider):
        if self.store_id == 0:
            self.store_id = item['store_id']
            self.set_base_data(spider)
        if isinstance(item, ClassifyItem):
            """
                商品类别
            """
            classify_keys = self.classify.keys()
            for val in item['classify_data']:
                if int(val['id']) not in classify_keys:
                    models.db.add(models.GoodsClassify(**val))
        elif isinstance(item, GoodsItem):
            """
                商品
            """
            for i in item['goods_data']:
                if i['bar_code'] in self.exists_code:
                    # 修改商品
                    need_update = False
                    for key in {'name', 'price', 'category_id', 'stock_nums'}:
                        if i[key] != getattr(self.goods_tmp[i['bar_code']], key):
                            need_update = True
                            break
                        else:
                            need_update = False
                    if need_update:
                        r = models.db.query(models.Goods).filter_by(store_id=self.store_id, bar_code=i['bar_code']).update(
                            {**i})
                        # print('update: {} goods'.format(r))
                    # else:
                    #     print('goods exists')
                else:
                    # 新增商品
                    # print('add {} goods'.format(i['name']))
                    models.db.add(models.Goods(**i))
                models.db.commit()
        elif isinstance(item, OrderFormItem):
            """
                订单
            """
            sku_ids = self.goods_tmp.keys()
            for order in item['orders_data']:
                # 通过sku_id 查询商品条码
                if order['sku_id'] in sku_ids:
                    order['goods_code'] = self.goods_tmp[order['sku_id']].bar_code
                    if order['form_code'] in self.all_orders:
                        # print('重复订单{}, {}'. format(order['form_code'], order['goods_name']))
                        continue
                    else:
                        # print('执行添加订单')
                        models.db.add(models.OrderForm(**order))
                else:
                    # 商品不存在
                    print(order)
            models.db.commit()
        elif isinstance(item, TurnoverFormItem):
            """
                营业额
            """
            for t_item in item['turnover_data']:
                turnover_date = t_item['date'][0:4] + '-' + t_item['date'][4:6] + '-' + t_item['date'][6:]
                if turnover_date not in self.exists_turnover:
                    models.db.add(models.Turnover(**t_item))
                else:
                    print('已经存在{}'.format(turnover_date))


        else:
            print('item error')


    def close_spider(self, spider):
        print('spider {} 停止'.format(spider.name))
        models.end()

