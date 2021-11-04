import json,re
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
# Create your views here.
from django.views import View
from apps.users.models import User
from django_redis import get_redis_connection #导入redis包
from django.contrib.auth import authenticate,login
# 1 导入系统logging
import logging
# 2 创建日志署
logger = logging.getLogger('django')

# 登录
class RegisterView(View):
    def post(self,request):
        body_bytes = request.body
        body_str = body_bytes.decode()
        body_dict = json.loads(body_str)
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        sms_code = body_dict.get('sms_code')
        allow = body_dict.get('allow')
        # print(username,password,password2,mobile)
        if not all([username,password,password2,mobile,sms_code,allow]):
            return JsonResponse({'code':400,'message':'参数不全'})
        if not re.match(r'^[a-zA-Z0-9]{5,10}$',username):
            return JsonResponse({'code': 400, 'message': '用户名不满足规则'})
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return JsonResponse({'code': 400, 'message': '电话号不满足规则'})
        if not re.match(r'^\w{8,20}$',password) or not re.match(r'^\w{8,20}$',password2):
            return JsonResponse({'code': 400, 'message': '密码不满足规则'})
        if password != password2:
            return JsonResponse({'code':400,'message':'两次输入密码不一致'})
        redis_conn = get_redis_connection('code')
        redis_sms_code = redis_conn.get('sms:%s' % mobile)
        if not redis_sms_code:
            return JsonResponse({'code': 400, 'message': '短信验证码失效'})
        if redis_sms_code.decode() != sms_code:
            return JsonResponse({'code': 400, 'message': '短信验证码错误'})
        if not allow:
            return JsonResponse({'code':400,'message':'须同意协议'})
        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code':400,'message':'注册失败'})
        login(request,user)
        return JsonResponse({'code': 0, 'message': '注册成功'})

# 验证用户名唯一
class UsernameCountView(View):
    def get(self,request,username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code':200, 'errmsg':'ok', 'count':count})

# 验证手机号唯一
class MobileCountView(View):
    def get(self,request,mobile):
        count = User.objects.filter(mobile=mobile).count()
        # print(count)
        return JsonResponse({'code':200, 'errmsg':'ok', 'count':count})

# 登录
class LoginView(View):
    def post(self,request):
        # 接受参数
        dict = json.loads(request.body.decode())
        username = dict.get('username')
        password = dict.get('password')
        remember = dict.get('remember')
        print(username,password,remember)
        # 校验参数
        if not all([username,password]):
            return JsonResponse({'code': 400, 'errmsg':'参数不全'})
        # 动态判断用户类型，设置验证信息
        if re.match('^1[3-9]\d9$',username):
            # 手机号
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'
        # 验证是否能登录
        user = authenticate(username=username,password=password)
        # 判断是否为空
        if user is None:
            return JsonResponse({'code':400, 'errmsg':'用户名或密码错误'})
        # 状态保持
        login(request,user)
        # 判断是否记住用户
        if remember != True:
            # 如果没记住关闭失效
            request.session.set_expiry(0)
        else:
            # 如果记住 设置两周
            request.session.set_expiry(None)
        # 返回json
        response = JsonResponse({'code':0,'errmsg':'ok'})
        u = json.dumps(user.nick_name)
        # print(u)
        response.set_cookie('username',u)
        return response