# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
*************************************************
* File Name:     views.py
* Description :   flask_auth/app/auth
* Author :       kunming
* Date:         2021/08/23
*************************************************
* flask登录认证
* Change log:
*   20210823 登录认证蓝图函数汇总
*   20210824 登录认证使用数据库中数据进行验证，并添加登出及访问控制部分
*   20210825 使用模板渲染返回登录及注册界面
*************************************************
"""
from flask import jsonify, request, session, redirect, url_for, render_template
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash
__author__ = 'wangkunming'
from . import auth
from .forms import RegisterUserForm



@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录
    :return:返回登录成功的用户信息路由或错误信息
    """
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            return jsonify({'code': 1011, 'msg': 'post请求必须提供用户名 username和密码 password字段'})
        from ..model.auth_user import User
        user = User.query.filter(User.name == username,User.is_deleted == 0).first()
        if user:
            if username == user.name and check_password_hash(user.password,password):
                session['is_login'] = True
                session['login_username'] = username
                # 增加loginmanager管理，注册用户信息
                login_user(user=user)
                return redirect(url_for('auth.profile'))
        return jsonify({'code': 1012, 'msg': 'post请求提供的用户名或密码错误'})
    else:
        return render_template('auth_login.html')


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    用户信息
    :return:
    """
    return render_template('auth_profile.html',name=current_user.name)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """
    登出
    :return:返回登录路由
    """
    session.pop('login_username', None)
    session['is_login'] = False
    session.clear()
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册用户
    :return: 用户登录
    """
    form = RegisterUserForm()
    if form.validate_on_submit():
        from ..model.auth_user import User
        user = User().add_user(form)
        if user:
            return redirect(url_for('auth.login'))
        return jsonify({'code': 1013, 'msg': '新增用户失败'})
    else:
        return render_template('auth_register.html',form=form)
