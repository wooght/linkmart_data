from typing import Iterable

import scrapy
from scrapy import Request, FormRequest
from app_spider.items import ClassifyItem
import json


class ClassifySpider(scrapy.Spider):
    """
        * 商品种类Spider
        * 获取数据结构json ->  [{name,id,..,parentId:[{},{},...]}, {},...]
    """
    name = "classify"
    classify_api = 'https://retailadmin-erp.meituan.com/api/goods/category'

    def start_requests(self) -> Iterable[Request]:
        yield Request(url=self.classify_api, callback=self.parse, errback=self.err_parse, meta={'native':1})

    def parse(self, response, *args, **kwargs):
        """
            处理返回的商品分类数据
        """
        body = response.body.decode('utf-8')
        result = json.loads(body)
        item_data = ClassifyItem()
        item_data['store_id'] = response.request.meta['store_id']
        classify_data = []
        for val in result['data']:
            if 'children' in val.keys():
                for v in val['children']:
                    classify_tmp = {}
                    for index in v.keys():
                        classify_tmp[index] = v[index]
                    classify_tmp['store_id'] = item_data['store_id']
                    classify_data.append(classify_tmp)
                val.pop('children')
            classify_tmp = {}
            for index in val.keys():
                classify_tmp[index] = val[index]
            classify_tmp['store_id'] = item_data['store_id']
            classify_data.append(classify_tmp)
        item_data['classify_data'] = classify_data
        yield item_data

    def err_parse(self, failure):
        print(failure.request.url)
        print(failure.value.__class__.__name__name)