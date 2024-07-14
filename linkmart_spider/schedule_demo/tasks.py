# -- coding: utf-8 -
"""
@project    :HandBook
@file       :app.py
@Author     :wooght
@Date       :2024/7/2 15:17
@Content    :
"""
from datetime import timedelta
from celery import Celery
from celery.schedules import crontab
import redis
import random

pool = redis.ConnectionPool(host='192.168.101.101', port=6379, db=0, socket_connect_timeout=2)
r = redis.Redis(connection_pool=pool)

backend = 'redis://192.168.101.101:6379/0'      # 存储任务结果及状态,将worker的执行结果返回给调用方
broker = 'redis://192.168.101.101:6379/1'       # 存储消息队列,负责接受任务请求,并转发值worker
app = Celery('app',
             broker=broker,
             broker_connection_retry_on_startup=True)

app.conf.timezone = 'Asia/Shanghai'
app.conf.enable_utc = False
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    print('开始定时任务')
    sender.add_periodic_task(5.0, task_1.s(), name='task_1')
    sender.add_periodic_task(
        crontab(hour='17-23', minute='*/10'),
        task_2.s(),
        name='task_2'
    )

@app.task
def task_1():
    print('被执行')
    r.hset('celery_demo', 'one', str(random.randint(1,100)))

@app.task
def task_2():
    print('2 被执行')
    r.hset('celery_demo', 'two', str(random.randint(1,100)))

# app.conf.beat_schedule = {
#     'every-ten_minutes':{
#         'task': 'tasks.task_1',
#         'schedule': timedelta(seconds=10),
#         'args':(),
#     },
#     'every-'
# }