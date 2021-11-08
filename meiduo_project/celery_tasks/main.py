import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE","meiduo_project.settings")

celery_app = Celery('celery_tasks')

celery_app.config_from_object('django.conf:settings',namespace='CELERY')

celery_app.autodiscover_tasks(['celery_tasks.sms'])