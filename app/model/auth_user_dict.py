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
*************************************************
"""
__author__ = 'wangkunming'

# 定义一个字典，存储用户的用户名和密码信息
user_dict = {
    'null': {},
    'admin': {
        'id': 1,
        'username': 'admin',
        'password': 'mypassword'
    },
    'test': {
        'id': 2,
        'username': 'test',
        'password': 'password'
    }
}


class User(object):
    """
    用户类
    """
    def __init__(self, username='null'):
        if username not in user_dict.keys():username='null'
        data = user_dict.get(username)
        self.id = data.get('id')
        self.username = data.get('username')
        self.password = data.get('password')

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
        return '<User %r>' % self.username

    @staticmethod
    def query(username):
        if username is None: username = 'null'
        return User(username)

    def get_id(self):
        return str(self.username)
