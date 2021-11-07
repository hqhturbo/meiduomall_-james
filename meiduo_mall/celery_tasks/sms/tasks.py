import logging

from celery_tasks.main import celery_app
from libs.yuntongxun.sms import CCP

logger = logging.getLogger('django')


# name：异步任务别名
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, sms_code):
    """
    发送短信异步任务
    :param mobile: ⼿机号
    :param sms_code: 短信验证码
    """
    try:
        CCP().send_template_sms(mobile, [sms_code, 5], 1)
    except Exception as e:
        logger.error(e)
