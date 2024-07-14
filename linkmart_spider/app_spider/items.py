# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AppSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ClassifyItem(scrapy.Item):
    """
        商品类别
    """
    store_id = scrapy.Field()
    classify_data = scrapy.Field()

class GoodsItem(scrapy.Item):
    """
        商品
    """
    store_id = scrapy.Field()
    goods_data = scrapy.Field()

class OrderFormItem(scrapy.Item):
    """
        订单(多订单list)
    """
    store_id = scrapy.Field()
    orders_data = scrapy.Field()

class TurnoverFormItem(scrapy.Item):
    """
        营业额(多日数据list)
    """
    store_id = scrapy.Field()
    turnover_data = scrapy.Field()
