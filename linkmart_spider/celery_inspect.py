# -- coding: utf-8 -
"""
@project    :linkmart_spider
@file       :celery_inspect.py
@Author     :wooght
@Date       :2024/7/19 15:45
@Content    :worker检查
"""
from celery_object import celery_spider
# 获取活跃的worker队列
queques = celery_spider.control.inspect().active_queues()
print(queques)
# {'worker@c2ce03ad8a2c': [{'name': 'celery', 'exchange': {'name': 'celery', 'type': 'direct', 'arguments': None, 'durable': True, 'passive': False, 'auto_delete': False, 'delivery_mode': None, 'no_declare': False}, 'routing_key': 'celery', 'queue_arguments': None, 'binding_arguments': None, 'consumer_arguments': None, 'durable': True, 'exclusive': False, 'auto_delete': False, 'no_ack': False, 'alias': None, 'bindings': [], 'no_declare': None, 'expires': None, 'message_ttl': None, 'max_length': None, 'max_length_bytes': None, 'max_priority': None}]}

worker = celery_spider.control.inspect()
# 注册的task
print(worker.registered())  # {'worker@c2ce03ad8a2c': ['celery_object.before_dawn', 'celery_object.run_goods_spider']}
# 运行的task
print(worker.active())
# 即将运行的task
print(worker.scheduled())
# 队列中的task
print(worker.reserved())