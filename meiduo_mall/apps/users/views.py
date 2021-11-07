import json
import logging
import re
from django.contrib.auth import authenticate, login, logout
from libs.captcha.captcha import captcha # 导入验证码
from django.shortcuts import *
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.views import View
from apps.users.models import *
logger = logging.getLogger('django')
# Create your views here.
class UsernameCountView(View):
    def get(self,request,username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code':200,'errmsg':'ok','count':count})
class MobileCountView(View):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code':200,'errmsg':'ok','count':count})
class RegisterView(View):
    def post(self, request):
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        sms_code_client = body_dict.get('sms_code')
        redis_conn = get_redis_connection('code')
        sms_code_server = redis_conn.get(f'sms:{mobile}')
        if not all([username,password,password2,mobile,sms_code_client]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        if not sms_code_server:
            return JsonResponse({'code':400,'errmsg':'短信验证码失效'})
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code':400,'errmsg':'短信验证码有误'})
        try:
            User.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            logger.info(e)
            return JsonResponse({'code':400,'errmsg':'注册失败'})
        return JsonResponse({'code': 200, 'errmsg': '注册成功'})


class LoginView(View):
    def post(self,request):
        dict = json.loads(request.body.decode()) #获取json方式提交的数据
        username = dict.get('username')
        password = dict.get('password')
        remembered = dict.get('remembered')
        if re.match('^1[3-9]\d{9}$',username):
            User.USERNAME_FIELD = 'mobile'
            user = authenticate(mobile=username, password=password)
        else:
            user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code':400,'errmsg':'用户名或者密码错误'})
        login(request,user)
        if remembered != True:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)
        # 8返回json
        response = JsonResponse({'code':0,'errmsg':'ok'})
        u = json.dumps(user.nick_name) #用户名进行序列化
        response.set_cookie("username",u) # 讲用户名写入的cookie
        return response

class LogoutView(View):
    def delete(self,request):
        logout(request) #退出⽤户，本质就是删除了sessionid
        response = JsonResponse({"code":200,"errmsg":"退出成功"})
        response.delete_cookie('username')#清除用户信息
        return response