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
*   20210824 注册表单
*************************************************
"""
__author__ = 'wangkunming'
from flask_wtf import FlaskForm  # 表单基础类
from wtforms import StringField, PasswordField, SubmitField  # 导入字符串字段，密码字段，提交字段
from wtforms.validators import DataRequired, ValidationError, Email, Regexp, EqualTo, InputRequired, Length


class RegisterUserForm(FlaskForm):
    """
    注册表单
    """
    username = StringField(label="登录账号*", validators=[DataRequired('请输入登录账号'), Length(6, 64),
                                                      Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, '用户名只能使用字符串、数字和*%等特殊字符组合')],
                           render_kw={"class": 'form-control', "placeholder": "请输入登录账号", "required": 'required'})
    real_name = StringField(label="真实姓名*", validators=[DataRequired('请输入姓名')], render_kw={"class": 'form-control', "placeholder": "请输入姓名", })
    email = StringField(label="邮箱*", validators=[DataRequired('请输入邮箱'), Email('邮箱格式不正确')],
                        render_kw={"class": 'form-control', "placeholder": "请输入正确的邮箱地址以便接收信息", "required": 'required'})
    password = PasswordField(label="密码*", validators=[InputRequired(), EqualTo('password2', message='两次密码不一致')],
                             render_kw={"class": 'form-control', "placeholder": "请输入至少6位密码", "minlength": "6", "required": 'required'})
    password2 = PasswordField(label="确认密码*", validators=[InputRequired()], render_kw={"class": 'form-control', "placeholder": "确认密码", "required": 'required'})
    password_hint = StringField(label="密码提示", render_kw={"class": 'form-control'})
    submit = SubmitField(label="注册", render_kw={"class": "btn btn-primary",'style':'color: #007bff;border:5px solid #007bff;'})

    @staticmethod
    def validate_account(calv):
        from ..model.auth_user import User
        check = User.query.filter_by(account=calv.data).first()
        if check:
            raise ValidationError("账号已经存在")
