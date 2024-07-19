#!/bin/sh
case $1 in
   start) cd //app/linkmart_spider/ && celery -A celery_object beat -l info >  out.file  2>&1  & ;;# 停止方法( kill -9 pid) 用  (ps -ef)查看pid
esac