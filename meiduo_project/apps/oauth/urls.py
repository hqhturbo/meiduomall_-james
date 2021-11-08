from django.urls import *

# from apps.oauth.views import *
from apps.oauth.views import *

urlpatterns = [
    path('qq/authorization/',QQLoginURLView.as_view()),
    path('oauth_callback/', QQOauthView.as_view())

]