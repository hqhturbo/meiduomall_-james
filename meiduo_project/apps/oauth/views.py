import json
import re
from django.contrib.auth import login
from QQLoginTool.QQtool import OAuthQQ
from django.http import JsonResponse, HttpResponseBadRequest
from django.middleware import http
from django.views import View
from django_redis import get_redis_connection
from apps.oauth.utils import *
from .models import OAuthQQUser
from apps.users.models import User
from apps.users.views import logger
from meiduo_project import settings


class QQLoginURLView(View):
    def get(self, request):
        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                     client_secret=settings.QQ_CLIENT_SECRET,
                     redirect_uri=settings.QQ_REDIRECT_URI,
                     state=settings.QQ_STATE)
        # 2. 调⽤对象的⽅法⽣成跳转链接
        qq_login_url = qq.get_qq_url()
        # 3. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'login_url': qq_login_url})

class QQOauthView(View):
    """⽤户扫码登录的回调处理"""

    def get(self, request):
        """Oauth2.0认证"""
        # 接收Authorization Code
        # 提取code请求参数
        code = request.GET.get('code')
        if not code:
            return HttpResponseBadRequest('缺少code')
        # 创建⼯具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret=settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            # 使⽤code向QQ服务器请求access_token
            access_token = oauth.get_access_token(code)
            # 使⽤access_token向QQ服务器请求openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': 'oauth2.0认证失败, 即获取 qq信息失败'})
        try:
            # 查看是否有 openid 对应的⽤户
            oauth_qq = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果 openid 没绑定美多商城⽤户,进⼊这⾥:
            # 使⽤加密类加密 openid
            access_token = generate_access_token(openid)
            # 注意: 这⾥⼀定不能返回 0 的状态码. 否则不能进⾏绑定⻚⾯
            response = JsonResponse({'code': 400, 'access_token': access_token})
            return response
        else:
            # 如果 openid 已绑定美多商城⽤户
            # 根据 user 外键, 获取对应的 QQ ⽤户(user)
            user = oauth_qq.user
            # 实现状态保持
            login(request, user)
            # 6.2 设置cookie
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            u = json.dumps(user.nick_name)  # 用户名进行序列化
            response.set_cookie('username', u)
            return response



    def post(self, request):
        """美多商城⽤户绑定到openid"""

        # 1. 接收请求
        data = json.loads(request.body.decode())
        # 2. 获取请求参数 openid
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        access_token = data.get('access_token')
        print(access_token)
        # 判断⼿机号是否合法
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '请输⼊正确的⼿机号码'})
        # 判断密码是否合格
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': '请输⼊8-20位的密码'})
        # 判断短信验证码是否⼀致
        # 创建 redis 链接对象:
        redis_conn = get_redis_connection('code')
        # 从 redis 中获取 sms_code 值:
        sms_code_server = redis_conn.get(f'sms:{mobile}')
        # 判断获取出来的有没有:
        if sms_code_server is None:
            # 如果没有, 直接返回:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码失效'})
        # 如果有,对⽐⽤户输⼊的和服务端存储的短信验证码是否⼀致 则进⾏判断:
        if sms_code != sms_code_server.decode():
            # 如果不匹配, 则直接返回:
            return JsonResponse({'code': 400, 'errmsg': '输⼊的验证码有误'})
        # 添加对 access-token 解密
        openid = check_access_token(access_token)
        if openid is None:
            return JsonResponse({'code': 400, 'errmsg': 'access_token参数缺失'})
            # 3. 根据⼿机号进⾏⽤户信息的查询
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # ⼿机号不存在
            # 5. 查询到⽤户⼿机号没有注册。我们就创建⼀个user信息。然后再绑定
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)
        else:
            # ⼿机号存在
            # 4. 查询到⽤户⼿机号已经注册了。判断密码是否正确。密码正确就可以直接保存（绑定） ⽤户和openid信息
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})
        # 将⽤户信息和openid进⾏绑定写⼊表中
        # oid = openid.get('openid')
        OAuthQQUser.objects.create(user=user, openid=openid)
        # 6. 完成状态保持
        login(request, user)
        # 7. 返回响应
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', json.dumps(user.username))
        return response