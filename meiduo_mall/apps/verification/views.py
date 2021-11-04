from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
# Create your views here.
from django.views import View
from libs.captcha.captcha import *
from django_redis import *
from django_redis import *
from celery_tasks.sms.tasks import *
import logging

from libs.yuntongxun.sms import CCP

logger=logging.getLogger('django')

class ImageCodeView(View):
    """图形验证码"""
    def get(self,request,uuid):
        """
        :param request: 请求对象
        :param uuid: 唯⼀标识图形验证码所属于的⽤户
        :return: image/jpeg
        """
        txt,image = captcha.generate_captcha()

        redis_conn = get_redis_connection("code")
        redis_conn.setex(name=f'img:{uuid}', time=60, value=txt)

        return HttpResponse(image, content_type='image/jpeg')

class SMSCodeView(View):
    """短信验证码"""
    def get(self, reqeust):
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
        #4-1 获取redis中当前号码是否已经存在
        send_flag = redis_client.get(f'send_flag_{mobile}')
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': '手机号过于频繁发送验证码'})
        sms_code = '%06d' % random.randint(0, 999999)
        print(sms_code)
        # 5、保存短信验证码
        pl = redis_client.pipeline()#创建redis管道
        #将redis请求添加到队列之中
        pl.setex(f'sms:{mobile}',300,sms_code)
        # 6、发送短信验证码
        # CCP().send_template_sms(mobile, [sms_code, 5], 1)
        send_sms_code.delay(mobile, sms_code)
        pl.setex(f'send_flag_{mobile}',60,1)#短信发送后该手机号被标签
        pl.execute()
        # 7、响应结果
        return JsonResponse({'code': 0, 'errmsg': '发送短信成功'})