# syntax=docker/dockerfile:1
# 以上第一句固定格式
FROM python:latest
# 复制当前文件夹到 容器/app下
ADD . /app      
# 工作目录 及 docker exec -it docker_name /bin/bash 进去的默认目录
WORKDIR /app
# 安装python包
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 设置MYSQL环境变量
ENV MYSQL_HOST=mysql
# ENV MYSQL_USER=root
ENV MYSQL_ROOT_PASSWORD=wooght565758
ENV MYSQL_DATABASE=linkmart
# 暴露端口
EXPOSE 80
CMD ["python","manage.py", "runserver","0.0.0.0:80"]