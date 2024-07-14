from typing import Iterable

import scrapy
from scrapy import Request, FormRequest
import json
from common.DateTimeMath import DateTimeMath
from app_spider.items import OrderFormItem

class OrderformSpider(scrapy.Spider):
    name = "orderform"

    form_text = json.loads('{"startTime":"1716825600000","endTime":"1716903900000","orderIdMatch":"","paymentType":0,"payTypeName":"全部","payType":-1,"startDate":"2024/05/28 00:00","endDate":"2024/05/28 21:45","cashierId":0,"discountType":0,"orderType":0,"offset":0,"limit":20}')
    form_data = {key:str(value) for key, value in form_text.items()}
    last_order_id = '0'
    WDate = DateTimeMath('%Y/%m/%d', '%H:%M')
    """
        WDate 时间戳:   171,954,0933
        url需求时间戳    171,682,5600,000
    """

    def start_requests(self) -> Iterable[Request]:
        end_date = self.WDate.now_date
        start_date = self.WDate.before_day(3)
        self.form_data['startDate'] = start_date[0] + ' 00:00'
        self.form_data['startTime'] = str(start_date[1] * 1000)
        self.form_data['endDate'] = end_date + ' 00:00'
        self.form_data['endTime'] = str(int(self.WDate.str_to_stamp(end_date+' 00:00')) * 1000)
        yield FormRequest(url="https://retailadmin-erp.meituan.com/api/order/queryOrder",
                          method='POST',
                          formdata=self.form_data,
                          meta={'native':1}, callback=self.parse)

    def parse(self, response, *args):
        """
            订单数据结构
            {'orders':[{'orderbase':{}, 'orderItems':[]},...], 'hasNext':True}
        """
        yield_item = OrderFormItem()
        # 先指定store_id
        yield_item['store_id'] = response.request.meta['store_id']
        yield_item['orders_data'] = []
        result_data = json.loads(response.body.decode('utf-8'))
        result_orders = result_data['data']['orders']
        for order in result_orders:
            order_tmp = {}
            order_base = order['orderbase']
            order_item = order['orderItems']
            # 订单 信息
            order_tmp['form_code'] = order_base['localId']
            order_tmp['form_money'] = order_base['receivable'] / 100
            order_tmp['form_money_true'] = order_base['payed'] / 100
            order_tmp['form_date'] = order_base['createdTime'].split(' ')[0]
            order_tmp['form_time'] = order_base['createdTime'].split(' ')[1]
            order_tmp['store_id'] = yield_item['store_id']
            self.last_order_id = order_base['id']   # 订单最后一项的ID值, 作为下一页的起点
            for item in order_item:
                # 订单的每个商品信息
                goods_tmp = {'goods_name': item['skuName'].strip(), 'sku_id': item['skuId'], 'goods_num': item['count'],
                             'goods_money': item['price'] / 100}
                yield_item['orders_data'].append({**order_tmp, **goods_tmp})
                # 确保每个订单的第一个商品有订单费用,其他商品订单费用为0
                order_tmp['form_money'] = 0
                order_tmp['form_money_true'] = 0

        yield yield_item
        if result_data['data']['hasNext']:
            """
                https://retailadmin-erp.meituan.com/api/order/queryOrder?yodaReady=h5&csecplatform=4&csecversion=2.4.0
            """
            self.form_data['lastOrderId'] = self.last_order_id
            print('新page')
            yield FormRequest(url="https://retailadmin-erp.meituan.com/api/order/queryOrder?yodaReady=h5&csecplatform=4&csecversion=2.4.0",
                              method='POST',
                              formdata=self.form_data,
                              meta={'native': 1}, callback=self.parse)

"""
       
    订单数据结构:
    {'orders':[{'orderbase':{}, 'orderItems':}], 'hasNext':True}
        orderbase:{'id': '1794340744501801042', 'localId': '202405282144160000000519', 'status': 300, 'amount': 2400, 'receivable': 2400,
            'payed': 2400, 'oddment': 0, 'autoOddment': 0, 'changeOddment': 0, 'comment': '', 'orderVersion': 0, 'createdTime': '2024-05-28 21:44:20', 'creator': '刘卓林', 'modifyTime': '', 'modifier': None, 'campaignAmount': None, 'onSaleGoodsAmount': None}
        orderItems:
        {'skuId': '1047379420228309019', 'skuName': '红牛维生素功能饮料250ml', 'count': 1, 'unit': '瓶', 'price': 600, 'actualPrice': 600, 'totalPrice': 600}
        {'skuId': '1058286530692583517', 'skuName': '雀巢咖啡原醇香滑香滑浓咖啡饮料210ml', 'count': 2, 'unit': '瓶', 'price': 500, 'actualPrice': 500, 'totalPrice': 1000}
        {'skuId': '1794931150654472214', 'skuName': '娃哈哈饮用纯净水596ml', 'count': 1, 'unit': '瓶', 'price': 200, 'actualPrice': 200, 'totalPrice': 200}
        {'skuId': '1336895765506760713', 'skuName': '东鹏特饮维生素功能饮料500ml', 'count': 1, 'unit': '瓶', 'price': 600, 'actualPrice': 600, 'totalPrice': 600}
        转linkmart数据结构:
        localId:form_code,receivable:form_money,payed:form_money_true,createdTime:form_date/form_time
        skuName:goods_name,skuId:sku_id, count:goods_num, price:goods_money
"""