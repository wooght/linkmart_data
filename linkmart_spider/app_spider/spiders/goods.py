# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :goods.py
@Author     :wooght
@Date       :2024/6/25 17:18
@Content    :商品spider
"""
from typing import Iterable

import scrapy
from scrapy.http import Request
from app_spider.items import GoodsItem
from scrapy.utils.project import get_project_settings
import json


class GoodsSpider(scrapy.Spider):
    name = "goods"
    # 类别请求API模型
    url_template = 'https://retailadminapi-erp.meituan.com/api/v2/goods?pageNo={}&pageSize={}&categoryId={}&yodaReady=h5&csecplatform=4&csecversion=2.4.0'
    # 无类别请求API模型
    no_category_template = 'https://retailadminapi-erp.meituan.com/api/v2/goods?pageNo={}&pageSize={}&yodaReady=h5&csecplatform=4&csecversion=2.4.0'
    current_url = ''    # 当前运行url模版 上方二选一
    start_page = 1      # 开始页码
    pagesize = 40       # 单页显示条数

    def __init__(self, category_id, *args, **kwargs):
        """
            params: category_id 类别ID
            判断爬取目的:获取全部/最新第一页
            判断爬取类别:默认最新一页/某个类别全部
        """
        super().__init__(*args, **kwargs)
        self.last_goods = get_project_settings().get('LAST_GOODS')       # 1 获取全部 0 只获取第一页
        self.category_id = category_id
        # 是否查询单独某个类判断 为0则不需要分类查询
        if int(self.category_id) != 0:
            self.last_goods = 1                     # 分类查询 需要全部查询
            self.current_url = self.url_template
        else:
            self.current_url = self.no_category_template

    def make_url(self, page):
        """
            生成新的请求地址
            params: page 页码
            return: 新地址
        """
        args = (page, self.pagesize, self.category_id) if int(self.category_id) != 0 else (page, self.pagesize)
        return self.current_url.format(*args)

    def start_requests(self) -> Iterable[Request]:
        """
            开始请求
        """
        print('goods起始页面:'+self.make_url(1))
        yield Request(
            url=self.make_url(1),
            callback=self.parse, meta={'native': 1})

    def parse(self, response, *args):
        """
            数据处理
            goods数据结构:{'bar_coe':str, 'name':str, ...}
        """
        # GoodsItem 数据结构: {store_id:int, goods_data:[{},{},...]}
        item = GoodsItem()
        item['store_id'] = response.request.meta['store_id']
        item['goods_data'] = []
        result_data = json.loads(response.body.decode('utf-8'))
        # 当前页码
        result_page = result_data['data']['page']
        # 请求响应的所有goods
        goods_original = result_data['data']['goodsList']
        for g in goods_original:
            # goods数据转换,组装
            item['goods_data'].append({'bar_code': g['barcode'], 'name': g['name'], 'cost': g['costPrice'] / 100,
                                       'price': g['sellingPrice'] / 100, 'stock_nums': int(g['stock']),
                                       'place': g['origin'] if 'origin' in g.keys() else '',
                                       'company': g['unitName'] if int(g['unitId']) > 0 else '',
                                       'category_id': int(g['categoryId']), 'store_id': item['store_id'],
                                       'classify': g['categoryId'], 'qgp': 0, 'sku_id': g['id']})
        yield item
        # 下一页判断
        if result_page['pageNo'] * result_page['pageSize'] < result_page['totalCount'] and self.last_goods > 0:
            yield Request(
                url=self.make_url(result_page['pageNo'] + 1),
                callback=self.parse, meta={'native': 1}
            )




"""
    商品数据结构:
    {'barcode': '6914782201149', 'canWeigh': False, 'categoryId': '10463644', 'costPrice': 0, 'costPriceStr': '0', 'createdTime': 1719382225000, 
    'createdTimeStr': '1719382225000', 'id': '1805786533233160249', 'imgUrl': '', 'ingredient': '', 'lastModifiedTime': 1719382224948,
     'lastModifiedTimeStr': '1719382224948', 'memberPrice': -1, 'name': '徐福记草莓酥184g', 'origin': '广东', 'pinyinInitials': 'xfjcms184g',
      'sellingPrice': 1400, 'shelfLife': '', 'specification': '', 'stock': 0.0, 'stockTotalAmount': '0.00', 'unitId': '51829112',
       'unitName': '包', 'useBarcodeScale': False}
        转linkmart数据结构:
            barcode:bar_code,name:name,costPrice/100:cost,sellingPrice/100:price, int(stock):stock_nums, origin:place,
             unitName:company, categoryId:categoryId, store_id:store_id, id:sku_id
"""