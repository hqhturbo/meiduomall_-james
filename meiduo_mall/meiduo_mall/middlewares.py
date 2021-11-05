"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :middlewares.py
# @Date     :2021/11/5 14:38
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""

# 当前文件路径 -> 项目名称/项目名称/middlewares.py  (和setting.py设置文件相同目录中)
# 用于解决跨域请求问题
from django.utils.deprecation import MiddlewareMixin

class kuayu(MiddlewareMixin):

    def process_response(self, request, response):
        # 允许跨域请求的地址 (*代表所有地址)
        response['Access-Control-Allow-Origin'] = "http://127.0.0.1:8080"
        # 允许跨域请求的类型
        response['Access-Control-Allow-Headers'] = "X-Requested-With,Content-Type"
        # 允许跨域请求的方式
        response['Access-Control-Allow-Methods'] = "PUT,POST,GET,DELETE,OPTIONS"
        # 允许跨域请求携带cookie
        response['Access-Control-Allow-Credentials'] = "true"

        return response
