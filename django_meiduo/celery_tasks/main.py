from celery import Celery

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","django_meiduo.settings")

celery_app = Celery('celery_tasks')

celery_app.config_from_object('django.conf:settings',namespace='Celery')

celery_app.autodiscover_tasks('celery_tasks.sms')