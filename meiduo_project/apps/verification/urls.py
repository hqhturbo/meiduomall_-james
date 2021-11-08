from django.urls import path, re_path
from apps.verification.views import *
import re
urlpatterns = [
    path('image_codes/<uuid>/',ImageCodeView.as_view()),
    path('sms_codes/',SMSCodeView.as_view())
]
