"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :models.py
# @Date     :2021/11/5 16:24
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""
from django.db import models

class BaseModel(models.Model):
    '''为模型类补充字段'''

    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True,verbose_name='更新时间')

    class Meta:
        abstract=True  # 说明是抽象模型类，用于继承，数据库迁移不会创建BaseModel的表