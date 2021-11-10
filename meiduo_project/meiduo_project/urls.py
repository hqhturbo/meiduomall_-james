"""meiduo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import logging
from apps.users.views import *
from apps.oauth.urls import *
def log(request):
    logger = logging.getLogger('django')
    logger.info('用户登录了')
    logger.warning('redis缓存不足')
    logger.error('该记录不存在')
    logger.debug('---------')
    return HttpResponse('log')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('apps.users.urls')),
    path('',include('apps.verification.urls')),
    path('',include('apps.oauth.urls')),
    path('',include('apps.areas.urls'))
]
