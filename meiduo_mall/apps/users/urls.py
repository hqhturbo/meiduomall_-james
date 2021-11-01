from django.urls import path, re_path
from apps.users import views
from django.urls import path
from apps.users import views
from apps.users.views import UsernameCountView,MobileCountView

urlpatterns = [
    path('usernames/<username>/count/', views.UsernameCountView.as_view()),
    path('mobiles/<mobile>/count/',MobileCountView.as_view()),#检查手机号重复
]
