from django.urls import path, re_path
from apps.users.views import *

urlpatterns = [
    path('usernames/<username>/count/', UsernameCountView.as_view()), # 检查⽤户名重复
    path('mobiles/<mobile>/count/',MobileCountView.as_view()),#检查手机号重复
    path('register/',RegisterView.as_view()),
    path('login/' ,LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('info/',UserInfoView.as_view()),
    path('emails/',EmailView.as_view()),
    path('emails/verification/', EmailVerifyView.as_view()),
    path('password/', ChangePasswordView.as_view()),
    path('addresses/',AddressView.as_view()),
    path('addresses/<address_id>',AddressView.as_view()),
    path('addresses/<address_id>/default/',AddressDefaultView.as_view()),
    path('addresses/<address_id>/title/',UsernameCountView.as_view())

]
