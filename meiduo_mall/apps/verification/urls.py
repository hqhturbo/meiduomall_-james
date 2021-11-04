from django.urls import re_path

from apps.verification.views import ImageCodeView, SMSCodeView

urlpatterns = [
    re_path(r'^images_codes/(?P<uuid>[\w-]+)/$',ImageCodeView.as_view()),
    re_path('sms_codes/',SMSCodeView.as_view())
]
