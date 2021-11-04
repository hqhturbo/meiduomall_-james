from django.urls import path, re_path
from app import views
from app.views import *
urlpatterns = [
    path('usernames/<username>/count/', UsernameCountView.as_view()), # 检查⽤户名重复
    path('mobiles/<mobile>/count/', MobileCountView.as_view()),# 检查⽤户名重复
    path('register/', views.RegisterView.as_view()),

    # re_path(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$',MobileCountView.as_view()), # 检查手机号码重复
    # re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$', UsernameCountView.as_view()) # 检查⽤户名重复（正则表达式格式）
]