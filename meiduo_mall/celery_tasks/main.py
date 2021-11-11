"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :main.py
# @Date     :2021/11/3 20:14
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""

"""
celery 启动文件
"""
from celery import Celery

# 为celery使用django配置文件进行设置
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings")

# 创建celery实例
celery_app = Celery('celery_tasks')

# 加载配置信息
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email'])