import logging
from django.conf import settings
from django.core.mail import send_mail
from celery_tasks.main import celery_app

logger = logging.getLogger('django')

@celery_app.task( name='send_verify_email')
def celery_send_email(subject, message, from_email, recipient_list, html_message):
    """发送邮件"""
    try:
        send_mail(subject=subject, message=message, from_email=from_email, recipient_list=recipient_list,
                  html_message=html_message)
    except Exception as e:
        logger.error(e)
