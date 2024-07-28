# -- coding: utf-8 -
"""
@project    :linkmart_data
@file       :models.py
@Author     :wooght
@Date       :2024/6/25 18:27
@Content    :模型
"""
from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Float, Date, Time
from sqlalchemy.orm import declarative_base, sessionmaker
from common.SecretCode import Wst


REDIS_HOST = '192.168.101.101'
REDIS_PORT = '6379'

MYSQL_HOST = 'mysql'
MYSQL_PORT = '3306'

"""
    定义表
"""
Base = declarative_base()
class GoodsClassify(Base):
    __tablename__ = 'goods_classify'
    id = Column(Integer, primary_key=True)  # 主键
    store_id = Column(Integer)                                  # 门店ID
    name = Column(String(32), index=True, nullable=False)       # 分类名称 不能为空 索引
    parentId = Column(Integer, default=0)                       # 父级ID
    categoryName = Column(String(32))
    categoryId = Column(Integer)                                # 分类id
    parentCategoryId = Column(Integer, default=0)

class Goods(Base):
    __tablename__ = 'goods_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64))  # 名称
    bar_code = Column(String(32))  # 条码
    sku_id = Column(String(32), default=0)  # 商品美团ID
    qgp = Column(Integer)  # 保质期
    store_id = Column(Integer)
    classify = Column(String(32))  # 分类
    category_id = Column(Integer)  # 分类ID
    stock_nums = Column(Integer)  # 库存
    cost = Column(Float)
    price = Column(Float)
    company = Column(String(32))  # 单位
    place = Column(String(32))  # 产地

class OrderForm(Base):
    __tablename__ = "order_form"
    id = Column(Integer, primary_key=True, autoincrement=True)
    form_code = Column(String(32), nullable=False)
    goods_name = Column(String(32), nullable=False)
    goods_code = Column(String(64), nullable=False)
    goods_num = Column(Integer)
    goods_money = Column(Float)
    form_date = Column(Date)
    form_time = Column(Time)
    form_money = Column(Float)
    form_money_true = Column(Float)
    store_id = Column(Integer)
    sku_id = Column(String(32))

class Turnover(Base):
    __tablename__ = 'bs_data'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date)
    cost = Column(Float)
    turnover = Column(Float)
    gross_profit = Column(Float)
    store_id = Column(Integer)

class StoreList(Base):
    """
        门店表
    """
    __tablename__ = 'store_list'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(32))               # 门店名称
    adds = Column(String(64))               # 门店地址
    mt_number = Column(String(32))          # 门店对应美团编号
    mt_password = Column(String(128))       # 对应美团密码
    mt_user = Column(String)                # 对应美团账号


"""
    连接数据库
"""
host = MYSQL_HOST
port = MYSQL_PORT
database = 'linkmart'
user = 'root'
password = Wst.decryption('.u/fe<qzO|~TrC;13E=z2vpQI#]X_?>[_.F!,T`!B')

engine = create_engine(
    f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8',
    echo=False,         # 打印SQL语句,生成环境关闭
    max_overflow=0,     # 超过连接池大小外最多创建的连接
    pool_size=5,        # 连接池大小
    pool_timeout=10,    # 连接超时时间
    pool_recycle=-1     # 多久后对连接池中的线程进行一次连接回收(重置)
)

Base.metadata.create_all(engine)        # 根据类创建数据库表
# 表结构定义结束/导入结束后 执行connection来执行数据库操作
Session = sessionmaker(bind=engine)  # 根据连接engine绑定会话
db = Session()  # 开启一个会话

def end():
    print('数据库commit')
    db.commit()
    db.close()

if __name__ == '__main__':
    exists_goods = db.query(Goods).filter(Goods.store_id == 1).all()
    goods_tmp = {}
    for goods in exists_goods:
        goods_tmp[goods.bar_code] = goods
    print(goods_tmp.keys())
