"""django_meiduo URL Configuration

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
from django.urls import path
import logging
from django.contrib import admin
from django.urls import path, include

# # 创建⽇志记录器
# logger = logging.getLogger('django')
# # 输出⽇志
# logger.debug('测试logging模块debug')
# logger.info('测试logging模块info')
# logger.error('测试logging模块error')
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),

]
