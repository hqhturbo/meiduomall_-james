"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :view_extend.py
# @Date     :2021/11/5 16:09
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

class LoginrequiredJsonMixin(LoginRequiredMixin):
    '''禁止匿名访问'''
    def handle_no_permission(self):
        return JsonResponse({'code':400,'errmsg':'匿名用户，请登录','next':self.request.path})