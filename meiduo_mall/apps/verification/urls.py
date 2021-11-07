from django.urls import path, re_path
from django.urls import path
from apps.verification.views import *

urlpatterns = [
    path('imgs/<uuid>/',ImageCodeView.as_view()),
    # path('sms_codes/<mobile>/<image_code>/<uuid>',SMSCodeView.as_view())
    re_path(r'^sms_codes/(?P<mobile>1[3-9]\d{9})/$', SMSCodeView.as_view())
]
