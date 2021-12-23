from django.urls import path
from apps.ads.views import *

urlpatterns = [
    path('index/',IndexView.as_view()),
]