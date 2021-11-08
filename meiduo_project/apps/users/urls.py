from django.urls import path, re_path
from apps.users.views import *

urlpatterns = [
    path('usernames/<username>/count/', UsernameCountView.as_view()), # 检查⽤户名重复
    path('mobiles/<mobile>/count/',MobileCountView.as_view()),#检查手机号重复
    path('register/',RegisterView.as_view()),
    path('login/' ,LoginView.as_view()),
    path('logout/',LogoutView.as_view())
]
