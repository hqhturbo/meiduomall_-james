from django.urls import path
from apps.verification.views import *

urlpatterns = [
    path('image_codes/<uuid>/',ImageCodeView.as_view())
]
