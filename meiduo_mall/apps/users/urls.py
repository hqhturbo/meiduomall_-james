from django.urls import path, re_path
from apps.users import views
from django.urls import path
from apps.users import views
from apps.users.views import *

urlpatterns = [
    path('usernames/<username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mobile>/count/',MobileCountView.as_view()),
    path('imgs/<uuid>/',ImageCountView.as_view()),
    path('register/', views.RegisterView.as_view()),
]
