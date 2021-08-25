# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
*************************************************
* File Name:     auth_user.py
* Description :   flask_auth/app/model
* Author :       kunming
* Date:         2021/08/23
*************************************************
* flask登录认证
* Change log:
*   20210823 实现auth这个蓝图的模型类 User
*   20210824 实现和mysql数据库交互
*   20210825 新增增加用户的方法
*************************************************
"""
__author__ = 'wangkunming'
from flask_login import UserMixin
from sqlalchemy import Table
from app import base_connection_info
from werkzeug.security import generate_password_hash

connection_session, db_model, engine_metadata = base_connection_info()


class User(db_model, UserMixin):
    """
    用户类
    """
    __table__ = Table('user', engine_metadata, autoload=True)

    def add_user(self,register_form):
        """
        新增用户
        :param register_form:  注册表单数据
        :return: 用户实例
        """
        user = User(name=register_form.username.data, password=generate_password_hash(password=register_form.password.data, method="pbkdf2:sha256", salt_length=10), real_name=register_form.real_name.data,
                    email=register_form.email.data, password_hint=register_form.password_hint.data)
        connection_session.add(user)
        connection_session.commit()
        return user

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % self.name

    def get_id(self):
        return str(self.name)
