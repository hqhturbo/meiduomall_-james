from django.contrib import admin
from django.urls import path
from apps.users import views
urlpatterns = [
    path('usernames', views.UsernameCountView.as_view())
]