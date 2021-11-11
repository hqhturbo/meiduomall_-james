"""
# -*- coding: utf-8 -*-
-------------------------------------------------
# @Project  :meiduo_mall
# @File     :tasks.py
# @Date     :2021/11/10 16:29
# @Author   :turbo
# @Email    :2647387166
# @Software :PyCharm
-------------------------------------------------
"""

import logging
from django.conf import settings
from django.core.mail import send_mail
from celery_tasks.main import celery_app

logger = logging.getLogger('django')

@celery_app.task(name = 'send_verify_email')
def celery_send_email(subject,message,form_email,recipient_list,html_message):
    '''发送邮件'''
    try:
        send_mail(subject=subject,message=message,from_email=form_email,recipient_list=recipient_list,html_message=html_message)
    except Exception as e:
        logger.error(e)