# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
*************************************************
* File Name:     __init__.py
* Description :   flask_auth/app/auth
* Author :       kunming
* Date:         2021/08/23
*************************************************
* flask登录认证
* Change log:
*   20210823 登录认证蓝图
*************************************************
"""
__author__ = 'wangkunming'
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import views
