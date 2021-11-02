from venv import logger

from django.contrib.auth import login
from django.http import JsonResponse
from django.views import View
from app.models import User
import json
import re

# Create your views here.
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


