# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
*************************************************
* File Name:     __init__.py
* Description :   flask_auth/app
* Author :       kunming
* Date:         2021/08/23
*************************************************
* flask登录认证
* Change log:
*   20210823 实现实例化Flask的工厂方法 并注册蓝图
*   20210824 新增loginmanager访问控制，新增sqlalchemy连接mysql数据库
*************************************************
"""
from sqlalchemy import exc, MetaData
__author__ = 'wangkunming'
from flask import Flask, jsonify, make_response, session
from werkzeug.exceptions import HTTPException
from flask_compress import Compress
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import QueuePool
from flask_bootstrap import Bootstrap

lm = LoginManager()
lm.session_protection = 'strong'
# 登录的路由视图
lm.login_view = 'auth.login'
# 实例化后端连接实例
db = SQLAlchemy(engine_options={"poolclass": QueuePool, 'pool_size': 200, 'max_overflow': 100, 'pool_recycle': 300})

bootstrap = Bootstrap()

def create_app(cfg):
    """
    工厂函数，实例化app及相关模块
    :param cfg: app配置
    :return: app实例
    """
    app = Flask(__name__, template_folder=cfg.TEMPLATES_PATH, static_url_path='/', static_folder=cfg.STATIC_PATH)
    app.config.from_object(cfg)

    # 初始化压缩
    Compress(app=app)

    # 实例化db
    db.init_app(app)

    # 实例化前端组件
    bootstrap.init_app(app)

    # 注册蓝图
    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    # 实例化访问控制
    lm.init_app(app)

    # 初始化响应
    init_response(app)

    return app

def base_connection_info():
    """
    和数据库连接的基础信息
    :return:
    """
    connection_session = db.session
    db_model = db.Model
    engine_metadata = MetaData(db.engine)
    return connection_session, db_model, engine_metadata

def init_response(app):
    @app.after_request
    def add_security_headers(response):
        # 响应安全头设置
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Sec-Fetch-Dest'] = 'document'
        response.headers['Sec-Fetch-Mode'] = 'navigate'
        response.headers['Sec-Fetch-Site'] = 'same-site'
        response.headers['Upgrade-Insecure-Requests'] = '1'
        # If you want all HTTP converted to HTTPS
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with,content-type'
        return response

    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        # 错误提示信息
        return jsonify({'status': 'error', 'message': exc.description, 'code': exc.code}), exc.code

    @app.errorhandler(404)
    def url_not_found(e):
        return make_response(jsonify({'code': 404, 'message': '请求的url不存在', 'status': 'error'}), 404)

    @app.errorhandler(405)
    def method_is_not_allowed(e):
        return make_response(jsonify({'code': 405, 'message': '请求的方法不存在', 'status': 'error'}), 405)

    @app.errorhandler(500)
    def method_is_not_allowed(e):
        return make_response(jsonify({'code': 500, 'message': '内部错误', 'status': 'error'}), 500)

    @lm.user_loader
    def load_user(name):
        from app.model.auth_user import User
        try:
            user = User.query.filter(User.name==name).first()
        except exc.StatementError:
            user = User.query.get(User.name==name).first()
        return user