from django.urls import path, re_path
from apps.users import views
from django.urls import path
from apps.users import views
from apps.users.views import UsernameCountView

urlpatterns = [
    path('usernames', views.UsernameCountView.as_view()),
    path('mobile',views.MobileCountView.as_view())
]
