from typing import Iterable

import scrapy
from scrapy.exceptions import DontCloseSpider
from scrapy import Request
from common.DateTimeMath import DateTimeMath
from app_spider.items import TurnoverFormItem
import json

class TurnoverSpider(scrapy.Spider):
    name = "turnover"
    url_model = ("https://retailadmin-erp.meituan.com/api/report/revenue/trend?begin_datekey={}&"
                 "end_datekey={}&isRT=false&cashier_id=-1&yodaReady=h5&csecplatform=4&csecversion=2.4.0")

    def start_requests(self) -> Iterable[Request]:
        wdate = DateTimeMath(date_model='%Y%m%d')
        # 默认除开今天的最近一个月的数据
        begin_datekey = wdate.before_day(30)[0]
        end_datekey = wdate.before_day(1)[0]
        turnover_url = self.url_model.format(begin_datekey, end_datekey)
        yield Request(url=turnover_url, callback=self.parse, errback=self.err_parse, meta={'native':1})


    def parse(self, response, *args):
        yield_item = TurnoverFormItem()
        yield_item['store_id'] = response.request.meta['store_id']
        result_json = json.loads(response.body.decode('utf-8'))
        yield_item['turnover_data'] = [
            {'date': str(item['statTime']), 'cost': item['skuCostAmt'] / 100, 'turnover': item['busiVolumeAmt'] / 100,
             'gross_profit': item['grossAmt'] / 100, 'store_id': yield_item['store_id']} for item in result_json['data']
        ]
        yield yield_item

    def err_parse(self, failure):
        print('error {} '.format(failure.__class__.__name__))
        print(failure.request.url)

"""
    营业额数据结构:
    {'data':
     [{'grossAmt': 413241, 'skuCostAmt': 1066929, 'statTime': 20240628, 'busiVolumeAmt': 1480170, 'grossRate': '27.92%'},
      {'grossAmt': 435569, 'skuCostAmt': 1072061, 'statTime': 20240627, 'busiVolumeAmt': 1507630, 'grossRate': '28.89%'},
     ...]
"""