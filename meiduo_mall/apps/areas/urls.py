"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :urls.py
# @Date     :2021/11/10 22:05
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""
from django.urls import path
from apps.areas.views import *
urlpatterns = [
    path('areas/',AreaView.as_view()),
    path('areas/<id>/',SubAreasView.as_view()),
]