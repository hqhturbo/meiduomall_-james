from django.urls import re_path,path

from app.verification.views import ImageCodeView
from app.views import SMSCodeView

urlpatterns = [
    #path('image_codes/<uuid>',ImageCodeView.as_view())
    re_path(r'^image_codes/(?P<uuid>[\w-]+)/$', ImageCodeView.as_view()),
    re_path('sms_codes', SMSCodeView.as_view())
]
# urlpatterns = [
#     path('image_codes/<uuid>/',ImageCodeView.as_view()),
#     # re_path(r'^usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/$',UsernameCountView.as_view()), # 检查⽤户名重复（正则表达式格式）
#     re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', SMSCodeView.as_view()) #短信验证码路由（正则表达式)
#
# ]


