"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :urls.py
# @Date     :2021/10/28 17:39
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""
from django.urls import path
from apps.users.views import *

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('info/',UserInfoView.as_view()),
    path('usernames/<username>/count/',UsernameCountView.as_view()),
    path('mobile/<mobile>/count/',MobileCountView.as_view()),
    path('emails/verification/', EmailVerifyView.as_view()),
    path('addresses/', CreateAddressViwe.as_view()),
    path('addresses/<address_id>/',CreateAddressViwe.as_view()),
    path('addresses/<address_id>/default/',AddressDefaultView.as_view()),
    path('addresses/<address_id>/title/',UpdateTitleAddressVier.as_view()),
    path('password/',ChangPasswordView.as_view()),
]
