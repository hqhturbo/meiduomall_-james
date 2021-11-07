from django.urls import path, re_path
from apps.users import views
from django.urls import path
from apps.users import views
from apps.users.views import *

urlpatterns = [
    path('usernames/<username>/count/', UsernameCountView.as_view()),
    path('mobiles/<mobile>/count/',MobileCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
]
