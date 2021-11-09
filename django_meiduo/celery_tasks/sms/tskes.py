from celery_tasks.main import celery_app
from libs.yuntongxun.sms import CCP
import logging

logger = logging.getLogger('django')


# name：异步任务别名
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):



    try:
        send_ret = CCP().send_template_sms(mobile, [sms_code, 5], 1)
    except Exception as e:
        logger.error(e)
