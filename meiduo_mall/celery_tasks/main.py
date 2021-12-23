# import django

from celery import Celery
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE","meiduo_mall.settings")

celery_app = Celery('celery_tasks')

celery_app.config_from_object('django.conf:settings',namespace = 'CELERY')

celery_app.autodiscover_tasks(['celery_tasks.sms','celery_tasks.email','celery_tasks.static_html'])
# django.setup()