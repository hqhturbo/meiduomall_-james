
from django.urls import path, re_path

from apps.users import views
from apps.users.views import *

urlpatterns = [
    path('usernames/<username>/count/', UsernameCountView.as_view()),  # 检查用户名重复
    path('mobiles/<mobile>/count/', MobileCountView.as_view()),  # 检查手机号码重复
    path('register/', RegisterView.as_view())
    # re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', UsernameCountView.as_view()),  # 检查用户名重复（正则表达式格式）
]