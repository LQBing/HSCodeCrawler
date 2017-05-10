# -*- coding: utf-8 -*-
from sqlalchemy import Column
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pymysql

pymysql.install_as_MySQLdb()

try:
    from local_settings import SQL_CON
    # SQL_CON example:
    # 'mysql://root:123456@127.0.0.1/hs'
except ImportError:
    SQL_CON = 'mysql://root:123456@127.0.0.1/hs?charset=utf8mb4'
BaseModel = declarative_base()
engine = create_engine(SQL_CON)
DBSession = sessionmaker(bind=engine)
session = DBSession()


class Chapter(BaseModel):
    __tablename__ = 'chapter'  # 表名
    id = Column(TEXT(), primary_key=True)
    name = Column(TEXT())
    url = Column(TEXT())


class HSCode(BaseModel):
    __tablename__ = 'hs_code'  # 表名
    id = Column(CHAR(20), primary_key=True)  # 商品编码
    name = Column(TEXT())  # 商品名称
    declare_elements = Column(TEXT())  # 申报要素
    statutory_first_unit_name = Column(TEXT())  # 法定第一单位
    statutory_second_unit_name = Column(TEXT())  # 法定第二单位
    mfn_rate = Column(TEXT())  # 最惠国( %)
    import_rate = Column(TEXT())  # 进口普通( %)
    export_ad_valorem_tariff_rate = Column(TEXT())  # 出口从价关税率
    vat_rate = Column(TEXT())  # 增值税率
    rebate_rate = Column(TEXT())  # 退税率( %)
    consumption_tax_rate = Column(TEXT())  # 消费税率
    customs_supervision_conditions = Column(TEXT())  # 海关监管条件
    inspection_and_quarantine = Column(TEXT())  # 检验检疫
    product_description = Column(TEXT())  # 商品描述
    en_name = Column(TEXT())  # 英文名称
    tax_number = Column(TEXT())  # 个人行邮(税号)


class HSCodeList(BaseModel):
    __tablename__ = 'hs_code_list'  # HS Code
    id = Column(CHAR(20), primary_key=True)  # HS编码
    name = Column(TEXT())  # 品名
    url = Column(TEXT())  # URL


def init_db():
    """
    初始化数据库
    :return:
    """
    BaseModel.metadata.create_all(engine)


def drop_db():
    """
    删除所有数据表
    :return:
    """
    BaseModel.metadata.drop_all(engine)

# print('drop db')
# drop_db()
# print('init db')
# init_db()
