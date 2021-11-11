import re

from django.shortcuts import render

from django.views import *
from django.http import *
from QQLoginTool.QQtool import OAuthQQ
from django.conf import *
from django_redis import get_redis_connection

from apps.oauth.utils import generate_access_token, check_access_token


class QQLoginURLView(View):
    """
    ⽣成⽤户绑定链接
    前端： 当⽤户点击QQ登录图标的时候，前端应该发送⼀个axios(Ajax)请求
    后端：
    请求
    业务逻辑 调⽤QQLoginTool ⽣成跳转链接
    响应 返回跳转链接 {"code":0,"qq_login_url":"http://xxx"}
    路由 GET qq/authorization/
    步骤
    1. ⽣成 QQLoginTool 实例对象
    2. 调⽤对象的⽅法⽣成跳转链接
    3. 返回响应
    """
    def get(self, request):
        # 1. ⽣成 QQLoginTool 实例对象
        # client_id=None, appid
        # client_secret=None, appsecret
        # redirect_uri=None, ⽤户同意登录之后，跳转的⻚⾯
        # state=None 标记值，⽤于防⽌csrf攻击。这⾥我们可以给个固定值
        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
        client_secret=settings.QQ_CLIENT_SECRET,
        redirect_uri=settings.QQ_REDIRECT_URI,
        state=settings.QQ_STATE)
        # 2. 调⽤对象的⽅法⽣成跳转链接
        qq_login_url = qq.get_qq_url()
        # 3. 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'login_url':qq_login_url})

from apps.oauth.models import OAuthQQUser
from django.contrib.auth import login
import json
from apps.users.models import User
import logging
logger=logging.getLogger('django')
class QQOauthView(View):
    """⽤户扫码登录的回调处理"""
    def get(self, request):
        """Oauth2.0认证"""
        # 接收Authorization Code
        code = request.GET.get('code')
        if not code:
            return JsonResponse({'code':'400','errmsg':'缺少code参数'})
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
            JsonResponse({'code': 400, 'errmsg': 'oauth2.0认证失败, 即获取qq信息失败'})

        try:
            oauth_qquser = OAuthQQUser.objects.get(openid=openid)
            print(oauth_qquser)

        except OAuthQQUser.DoesNotExist:
            # 使⽤加密类加密 openid
            access_token = generate_access_token({'openid': openid})

            response = JsonResponse({'code': 400, 'access_token': access_token})
            return response
        else:
            # # 6. 完成状态保持
            # response = JsonResponse({'code': 0, 'errmsg': '已经绑定的用户直接登录'})
            # login(request, oauth_qquser.user)
            # response.set_cookie('username', json.dumps(oauth_qquser.user.username))
            # return response
            # 如果 openid 已绑定美多商城⽤户
            # 根据 user 外键, 获取对应的 QQ ⽤户(user)
            user = oauth_qquser.user
            # 实现状态保持
            login(request, user)
            # 创建重定向到主⻚的对象
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            # 将⽤户信息写⼊到 cookie 中
            u = json.dumps(user.nick_name)
            response.set_cookie('username', u)
            # 返回响应
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
            user = User.objects.create_user(username=mobile, mobile=mobile,password=password)
        else:
            # ⼿机号存在
            # 4. 查询到⽤户⼿机号已经注册了。判断密码是否正确。密码正确就可以直接保存（绑定） ⽤户和openid信息
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg': '账号或密码错误'})
        # 将⽤户信息和openid进⾏绑定写⼊表中
        openid = openid.get('openid')
        OAuthQQUser.objects.create(user=user, openid=openid)
        # 6. 完成状态保持
        login(request, user)
        # 7. 返回响应
        response = JsonResponse({'code': 0, 'errmsg':'qq和用户信息绑定成功'})
        response.set_cookie('username', json.dumps(user.nick_name))
        return response