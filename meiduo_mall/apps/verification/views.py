from random import random
from venv import logger

from django_redis import get_redis_connection
# from libs.captcha.captcha import captcha
from django.views import View
from django.http import HttpResponse, JsonResponse

from libs.captcha.captcha import captcha
from libs.yuntongxun.sms import CCP


class ImageCodeView(View):
    def get(self, request, uuid):
        # ⽣成图⽚验证码
        text, image = captcha.generate_captcha()
        # 保存图⽚验证码
        # redis_conn = get_redis_connection('code')
        # redis_conn.setex('img_%s' % uuid, 300, text)
        # 响应图⽚验证码
        return HttpResponse(image, content_type='image/jpeg')



class SMSCodeView(View):
    """短信验证码"""

    def get(self, reqeust, send_sms_code=None):
        """
        :param reqeust: 请求对象
        :param mobile: ⼿机号
        :return: JSON
        """
        # 1、获取图片验证码
        mobile = reqeust.GET.get('mobile')
        image_code = reqeust.GET.get('image_code')
        uuid = reqeust.GET.get('uuid')
        # 2、校验参数是否齐全
        if not all([mobile, image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 3、获取redis中的图片验证码信息
        redis_client = get_redis_connection('code')
        redis_imgcode = redis_client.get(f'img:{uuid}')
        # 3-1、判断redis中的图片验证码是否存在
        if redis_imgcode is None:
            return JsonResponse({'code': 400, 'errmsg': '图片验证码过期'})
        # 3-2、有图片验证码，就将原来redis中存入的删掉
        redis_client.delete(f'img:{uuid}')
        # 3-3、比对图片验证码
        if image_code.lower() != redis_imgcode.decode().lower():
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})

        # 4、⽣成短信验证码：⽣成6位数验证码
        # 4-1、检查短信发送标记
        send_flag = redis_client.get(f'send_flag_{mobile}')
        if send_flag:  # 如果发送短信的标记有，那么就返回信息
            return JsonResponse({'code': 400, 'errmsg': '手机号码发送过于频繁'})

        sms_code = '%06d' % random.randint(0, 999999)
        print(sms_code)
        # 5、保存短信验证码
        redis_client.setex(f'sms:{mobile}', 300, sms_code)
        # 6、发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        send_sms_code.delay(mobile, sms_code)  # 异步发送短信
        redis_client.setex(f'send_flag_{mobile}', 60, 1)  # 发送短信后，向redis中添加一个标记
        # 7、响应结果
        return JsonResponse({'code': 0, 'errmsg': '发送短信成功'})
