"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :urls.py
# @Date     :2021/11/2 16:21
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""

from django.urls import path,re_path
from apps.verification.views import *

urlpatterns = [
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$', ImageCodeView.as_view()),
    re_path(r'^smscode/(?P<mobile>1[3-9]\d{9})/$', SmscodeView.as_view()),
]
