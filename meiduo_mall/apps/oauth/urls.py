"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :urls.py
# @Date     :2021/11/5 16:29
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""

from django.urls import path
from apps.oauth.views import *

urlpatterns = [
    path('qq/authorization/',QQLoginURLView.as_view()),
    path('oauth_callback/',QQOauthView.as_view()),
]