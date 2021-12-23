from celery_tasks.main import celery_app
from libs.yuntongxun.sms import CCP
import logging
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
        send_ret = CCP().send_template_sms(mobile, [sms_code, 5], 1)
        print(send_ret)
    except Exception as e:
        logger.error(e)