# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
*************************************************
* File Name:     flask_auth.py
* Description :   flask_auth
* Author :       kunming
* Date:         2021/08/22
*************************************************
* flask登录认证
* Change log:
*   20210822 最基础的flask app
*   20210823 和配置类结合，通过配置类的参数控制flask app，并且添加请求和响应相关的设置
*   20210823 将实例化Flask的部分提取到 app/__init__.py中做成工厂类
*************************************************
"""
__author__ = 'wangkunming'
from config import config
from app import create_app
from flask_login import login_required

cfg = config['test']
app = create_app(cfg)


@app.route('/')
def hello_world():
    return 'hello_world'


if __name__ == '__main__':
    app.run(host=cfg.APP_HOST, port=cfg.APP_PORT, debug=cfg.APP_DEBUG, threaded=cfg.APP_THREADED)
