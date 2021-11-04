import random
from venv import logger

from django.contrib.auth import login
from django.http import JsonResponse
from django.views import View
from django_redis import get_redis_connection

from app.models import User
import json
import re

# Create your views here.
from libs.yuntongxun.sms import CCP


class UsernameCountView(View):
    '''检查⽤户名重复'''
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 200, 'errmsg': 'ok', 'count': count})

class MobileCountView(View):
    '''检查手机号码重复'''
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 200, 'errmsg': 'ok', 'count': count})
class PasswordCountView(View):

    def get(self, request, password):
        count = User.objects.filter(password=password).count()
        return JsonResponse({'code': 200, 'errmsg': 'ok', 'count': count})
class RegisterView(View):
    """⽤户注册"""
    def post(self, request):
        # 1.接收参数：请求体中的JSON数据 request.body
        json_bytes = request.body  # 从请求体中获取原始的JSON数据，bytes类型的
        json_str = json_bytes.decode()  # 将bytes类型的JSON数据，转成JSON字符串
        json_dict = json.loads(json_str)  # 将JSON字符串，转成python的标准字典
       # json_dict = json.loads(request.body.decode())
        # 提取参数
        username = json_dict.get('username')
        password = json_dict.get('password')
        password2 = json_dict.get('password2')
        mobile = json_dict.get('mobile')
        if not all([username,password,password2,mobile]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # ⽤户名不能重复
        try:
            User.objects.create_user(username=username,password=password,mobile=mobile)
            return JsonResponse({'code': 200, 'errmsg': '注册成功!'})
        except Exception as e:
            logger.info(e)
            return JsonResponse({'code': 400, 'errmsg': '注册失败!'})
        login(request, user)
        return JsonResponse({'code':200,'errmsg':json_dict,})


class SMSCodeView(View):


    """短信验证码"""


    def get(self, reqeust):
        mobile = reqeust.GET.get("mobile")
        image_code_client = reqeust.GET.get('image_code')  # 获取验证码
        uuid = reqeust.GET.get('uuid')  # 获取uuid
        # 2、校验参数
        print(mobile)
        print(image_code_client)
        print(uuid)
        if not all([image_code_client, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        # 3、创建连接到redis的对象
        redis_conn = get_redis_connection('code')
        # 3-1、提取图形验证码
        image_code_server = redis_conn.get('img_%s' % uuid)
        # 3-2、判断redis中是否后该图形验证码信息
        if image_code_server is None:
        # 图形验证码过期或者不存在
            return JsonResponse({'code': 400, 'errmsg': '图形验证码失效'})
        # 3-3、如果有图形验证码，那么删除图形验证码，避免恶意测试图形验证码
        try:
            redis_conn.delete(f'img:{uuid}')
        except Exception as e:

            logger.error(e)
        # 3-4、对⽐图形验证码
        image_code_server = image_code_server.decode()  # bytes转字符串
        if image_code_client.lower() != image_code_server.lower():  # 转⼩写后⽐较
            return JsonResponse({'code': 400, 'errmsg': '输⼊图形验证码有误'})
        # 3-5、提取、校验send_flag
        send_flag = redis_conn.get(f'send_flag:{mobile}')
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg': '发送短信过于频繁'})
        # 4、⽣成短信验证码：⽣成6位数验证码
        sms_code = '%06d' % random.randint(0, 999999)
        print(sms_code)
        logger.info(f'短信验证码是：{sms_code}')
        # 5、保存短信验证码
        redis_conn.setex(f'sms:{mobile}', 300, sms_code)
        # 写⼊send_flag
        redis_conn.setex(f'send_flag:{mobile}', 60, 1)
        # 6、发送短信验证码
        CCP().send_template_sms(mobile, [sms_code, 5], 1)
        # 7、响应结果
        return JsonResponse({'code': 200, 'errmsg': '发送短信成功'})
