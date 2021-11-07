from django.http import HttpResponse
from django.views import View
from django.views import View
from django_redis import get_redis_connection
from django.http import JsonResponse
from libs.captcha.captcha import captcha  # 导入验证码
import logging
from random import randint
from celery_tasks.sms.tasks import *

from libs.yuntongxun.sms import CCP

logger = logging.getLogger('django')
# Create your views here.
class ImageCodeView(View):
    def get(self, request, uuid):
        if uuid is None:
            return HttpResponse('没有获取到uuid')
        txt, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('code')
        redis_conn.setex(name='img:%s' % uuid, time=300, value=txt)
        return HttpResponse(image, content_type='image/jpeg')


class SMSCodeView(View):
    """短信验证码"""
    def get(self, reqeust,mobile):
        image_code = reqeust.GET.get('image_code')  # 获取验证码
        uuid = reqeust.GET.get('uuid')  # 获取uuid
        # print(image_code)
        # print(uuid)
        # print(mobile)
        # 验证参数
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        # 创建连接到redis的对象
        redis_conn = get_redis_connection('code')
        # 取redis库里面的uuid
        image_code_server = redis_conn.get(f'img:{uuid}')
        # uuid是否为空
        if image_code_server is None:
            return JsonResponse({'code': 400, 'errmsg': '图形验证码失效'})
        try:
            redis_conn.delete(f'img:{uuid}')
        except Exception as e:
            logger.error(e)
        image_code_server = image_code_server.decode()
        if image_code.lower() != image_code_server.lower():
            return JsonResponse({'code': 400, 'errmsg': '输⼊图形验证码有误'})
        send_flag = redis_conn.get(f'send_flag:{mobile}')
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': '发送短信过于频繁'})
        sms_code = '%06d' % randint(0, 999999)
        logger.info(f'短信验证码是：{sms_code}')
        # 创建Redis管道
        pl = redis_conn.pipeline()
        pl.setex('sms:%s' % mobile, 300,sms_code)
        pl.setex(f'send_flag:{mobile}', 60, 1)
        # 执行请求
        pl.execute()
        send_sms_code.delay(mobile, sms_code)
        return JsonResponse({'code': 0, 'errmsg': '发送短信成功'})
