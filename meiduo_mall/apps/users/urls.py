from django.urls import path, re_path
from apps.users.views import *

urlpatterns = [
    # path('usernames/<username>/count/', UsernameCountView.as_view()), # 检查⽤户名重复
    re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',UsernameCountView.as_view()), # 检查⽤户名重复（正则表达式格式）
    # re_path('usernames/<username>/count/',UsernameCountView.as_view())# 检查⽤户名重复（正则表达式格式）
]