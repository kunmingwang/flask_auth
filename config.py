# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
*************************************************
* File Name:     config.py
* Description :   flask_auth
* Author :       kunming
* Date:         2021/08/22
*************************************************
* flask登录认证
* Change log:
*   20210822 实现基础配置及测试和生产配置类，并初始化config对象为测试类对象
*   20210824 新增数据库连接信息
*************************************************
"""
__author__ = 'wangkunming'
import datetime
import logging
import os


class BaseConfig(object):
    # 安全和session
    SECRET_KEY = os.environ.get('APP_SECRET_KEY') or "miyao=1234567890"  # flask app运行要用到的秘钥
    SESSION_TYPE = 'null'
    SESSION_KEY_PREFIX = "session:"
    SESSION_PERMANENT = False
    CSRF_ENABLED = True
    REMEMBER_COOKIE_DURATION = datetime.timedelta(days=3)
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=3)
    APP_SALT = os.environ.get('APP_SALT') or 'secure_key'
    WTF_CSRF_SECRET_KEY = SECRET_KEY
    JSON_AS_ASCII = False
    # 定义静态目录的位置
    BASE_PATH = os.path.abspath(os.path.dirname(__file__))
    STATIC_PATH = os.path.join(BASE_PATH, 'static')
    TEMPLATES_PATH = os.path.join(BASE_PATH, 'templates')
    EXPORT_PATH = os.path.join(BASE_PATH, 'export')
    SEND_FILE_MAX_AGE_DEFAULT = datetime.timedelta(minutes=1)  # 文件的静态文件缓存
    # 静态文件压缩相关
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'text/plain', 'text/javascript',
                          'application/json', 'application/x-javascript', 'application/javascript',
                          'image/jpeg', 'image/png']
    COMPRESS_LEVEL = 9
    COMPRESS_BR_LEVEL = 9
    COMPRESS_MIN_SIZE = 600
    COMPRESS_DEFLATE_LEVEL = 9
    # 绑定信息
    APP_NAME = 'flask_auth'
    APP_HOST = '0.0.0.0'  # app 运行绑定的ip
    APP_PORT = 5000  # app 运行绑定的端口
    APP_DEBUG = True  # 开启debug模式
    APP_THREADED = True  # 启用多线程模式
    LOG_LEVEL = logging.INFO
    LOG_PATH = os.path.join(os.path.dirname(BASE_PATH), 'logs/')
    PID_PATH = os.path.join(BASE_PATH + "{}_{}.pid".format(APP_NAME, APP_PORT))
    LOG_NAME = "{}_{}.log".format(APP_NAME, APP_PORT)
    # 后端存储设置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask_auth:**password**@10.231.3.82:3306/flask_auth?charset=UTF8MB4&autocommit=true'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


    @staticmethod
    def init_app(app):
        pass


class TestConfig(BaseConfig):
    """
    测试环境 默认
    """
    APP_NAME = 'flask_auth_test'
    APP_HOST = '127.0.0.1'
    APP_PORT = 5000
    PID_PATH = os.path.join(BaseConfig.BASE_PATH + "{}_{}.pid".format(APP_NAME, APP_PORT))
    LOG_NAME = "{}_{}_test.log".format(APP_NAME, APP_PORT)


class ProductionConfig(BaseConfig):
    """
    线上环境
    """
    APP_NAME = 'flask_auth'
    APP_HOST = '0.0.0.0'
    APP_PORT = 8000
    PID_PATH = os.path.join(BaseConfig.BASE_PATH + "{}_{}.pid".format(APP_NAME, APP_PORT))
    LOG_NAME = "{}_{}.log".format(APP_NAME, APP_PORT)
    # 后端存储设置 随便写的ip演示用，没这个数据库实例
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://flask_auth:flask_auth@10.0.0.66:3306/flask_auth?charset=UTF8MB4&autocommit=true'


config = {
    'test': TestConfig,
    'production': ProductionConfig,
    'default': TestConfig
}
