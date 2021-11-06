from django.urls import path, re_path

from apps.users import views
from apps.users.views import *

urlpatterns = [
    # path('usernames/<username>/count/', UsernameCountView.as_view()), # 检查⽤户名重复
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',UsernameCountView.as_view()), # 检查⽤户名重复（正则表达式格式）
    # re_path('usernames/<username>/count/',UsernameCountView.as_view())# 检查⽤户名重复（正则表达式格式）

    re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$',MobileCountView.as_view()), # 检查⼿机号码重复（正则表达式格式）

    # 注册路由
    path('register', views.RegisterView.as_view()),
    #登录路由
    path('login/', LoginView.as_view()),

    path('logout/', LogoutView.as_view())
]