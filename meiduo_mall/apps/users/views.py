from django.contrib.auth import login
from django.shortcuts import render
from django.http import JsonResponse, response
from django.views import View
from apps.users.models import User
import json
import re
import logging
logger = logging.getLogger('django')
from django.contrib.auth import authenticate, login

# Create your views here.
class UsernameCountView(View):
    '''检查⽤户名重复'''
    def get(self, request, username):
        """
            :param request: 请求对象
            :param username: ⽤户名
            :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 200, 'errmsg': '用户名可以使用','count':count})

class MobileCountView(View):
    """判断⼿机号是否重复注册"""
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count() # 说明：mobile__exact=mobile 就等价于mobile=mobile 都是表示相等的含义
        return JsonResponse({'code': 200, 'errmsg': 'ok', 'count': count})

class RegisterView(View):
    """⽤户注册"""
    def post(self, request):
        """
        实现⽤户注册
        :param request: 请求对象
        :return: 注册结果
        """
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
        allow = json_dict.get('allow')
        # sms_code = json_dict.get('sms_code')

        # 4. 数据⼊库
        # user=User(username=username,password=password,moble=mobile)
        # user.save()
        #
        # User.objects.create(username=username, password=password, mobile=mobile)
        # return JsonResponse({'code': 400, 'errmsg': '注册失败!'})
        # 以上2中⽅式，都是可以数据⼊库的
        # 但是 有⼀个问题 密码没有加密
        # 密码就加密（调⽤django系统模型⾃带⽅法）
        # if not all([username, password, password2, mobile, allow]):
        #     return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # # 3.2 ⽤户名满⾜规则，⽤户名不能重复
        # if not re.match('[A-Za-z0-9]{5,11}', username):
        #     return JsonResponse({'code': 400, 'errmsg': '⽤户名不满⾜规则'})
        # # 3.3 密码满⾜规则
        # if not re.match('[a-zA-Z]\w{5,17}$', password):
        #     return JsonResponse({'code': 400, 'errmsg': '密码格式不正确'})
        # # 3.4 确认密码和密码要⼀致
        # if password != password2:
        #     return JsonResponse({'code': 400, 'errmsg': '两次密码不⼀致'})
        # # 3.5 ⼿机号满⾜规则，⼿机号也不能重复
        # if not re.match('^1[345789]\d{9}$', mobile):
        #     return JsonResponse({'code': 400, 'errmsg': '⼿机号码格式不正确'})
        # # 3.6 需要同意协议
        # if not allow:
        #     return JsonResponse({'code': 400, 'errmsg': '必须同意协议'})
        try:
            User.objects.create_user(username=username,password=password, mobile=mobile)
            return JsonResponse({'code': 200, 'errmsg': '注册成功'})
        except Exception as e:
            logger.info(e)
            return JsonResponse({'code': 400, 'errmsg': '注册失败!'})




