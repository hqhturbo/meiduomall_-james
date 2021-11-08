import random
import logging
from django_redis import get_redis_connection
from libs.captcha.captcha import captcha
from django.views import View
from libs.yuntongxun.sms import CCP
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
logger = logging.getLogger('django')
from celery_tasks.sms.tasks import *

class ImageCodeView(View):
    def get(self, request, uuid):
        # ⽣成图⽚验证码
        text, image = captcha.generate_captcha()
        # 保存图⽚验证码
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s' % uuid, 300, text)
        # 响应图⽚验证码
        return HttpResponse(image, content_type='image/jpeg')



class SMSCodeView(View):
    """短信验证码"""
    def get(self, reqeust):
        """
        :param reqeust: 请求对象
        :param mobile: ⼿机号
        :return: JSON
        """
        # 1、接收参数
        mobile = reqeust.GET.get('mobile')
        image_code_client = reqeust.GET.get('image_code')  # 获取验证码
        uuid = reqeust.GET.get('uuid')  # 获取uuid
        # 2、校验参数
        if not all([mobile,image_code_client, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        # 3、创建连接到redis的对象
        redis_conn = get_redis_connection('code')
        # 3-1、提取图形验证码
        # image_code_server = redis_conn.get(f'img:{uuid}')
        image_code_server = redis_conn.get('img_%s' % uuid)
        # 3-2、判断redis中是否后该图形验证码信息
        if image_code_server is None:
            # 图形验证码过期或者不存在
            return JsonResponse({'code': 400, 'errmsg': '图片验证码过期或不存在'})
        # 3-3、如果有图形验证码，那么删除图形验证码，避免恶意测试图形验证码
        try:
            redis_conn.delete(f'img:{uuid}')
        except Exception as e:
            logger.error(e)
        # 3-4、对⽐图形验证码
        image_code_server = image_code_server.decode()  # bytes转字符串
        if image_code_client.lower() != image_code_server.lower():  # 转⼩写后⽐较
            return JsonResponse({'code': 400, 'errmsg': '图片验证码有误请重新输入'})
        # 3-5、提取、校验send_flag
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': '发送短信过于频繁'})
        # 4、⽣成短信验证码：⽣成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)
        logger.info(f'短信验证码是：{sms_code}')
        # 5、保存短信验证码
        redis_conn.setex(f'sms:{mobile}', 300, sms_code)
        # 6、发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        send_sms_code.delay(mobile,sms_code)
        redis_conn.setex('send_flag_%s' % mobile, 60, 1)
        # 7、响应结果
        return JsonResponse({'code': 0, 'errmsg': '发送短信成功'})
