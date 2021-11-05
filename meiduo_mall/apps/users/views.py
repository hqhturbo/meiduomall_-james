import json,re

from django.http import JsonResponse
from django.views import View

from meiduo_mall.urls import logger
from apps.users.models import *
# Create your views here.

class UsernameCountView(View):
    '''检查⽤户名重复'''
    def get(self, request, username):#url路由方式来传递username参数
        """
        :param request: 请求对象
        :param username: ⽤户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 200, 'errmsg': 'ok','count':count})


class MobileCountView(View):
    '''检查⽤户名重复'''
    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param username: ⽤户名
        :return: JSON
        """
        count = User.objects.filter(mobile__exact=mobile).count()
        return JsonResponse({'code': 200, 'errmsg': 'ok','count':count})



class RegisterView(View):
    """⽤户注册"""
    def post(self, request):
        """
        实现⽤户注册
        :param request: 请求对象
        :return: 注册结果
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        json_dict = json.loads(json_str)

        username = json_dict.get("username")
        password = json_dict.get("password")
        password2 = json_dict.get("password2")
        mobile = json_dict.get("mobile")
        # allow = json_dict.get("allow")
        # sms_code = json_dict.get("sms_code")
        if not all([username,password,password2,mobile]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        if not re.match('[a-zA-Z_-]{5,20}',username):
            return JsonResponse({'code':400,'errmsg':'用户名不满足规范'})
        if not re.match('^\w{8,20}$',password):
            return JsonResponse({'code': 400, 'errmsg': '密码格式不正确'})
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次密码不一致'})
        if not re.match('^1[345789]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号码格式不正确'})
        # if not allow:
        #     return JsonResponse({'code': 400, 'errmsg': '必须同意协议'})
        try:
            User.objects.create_user(username=username,password=password, mobile=mobile)
            return JsonResponse({'code': 200, 'errmsg': '注册成功'})
        except Exception as e:
            logger.info(e)
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})