from django.shortcuts import render
from django.views import View
from django import http
from django.http import JsonResponse
from QQLoginTool.QQtool import OAuthQQ
from meiduo_mall import settings
from apps.oauth.models import *
from django.contrib.auth import login
import json
from apps.users.models import User
# Create your views here.

# QQ登录
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
    def get(self,request):
        # 1. ⽣成 QQLoginTool 实例对象
        # client_id=None, appid
        # client_secret=None, appsecret
        # redirect_uri=None, ⽤户同意登录之后，跳转的⻚⾯
        # state=None 标记值，⽤于防⽌csrf攻击。这⾥我们可以给个固定值

        qq = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                     client_secret=settings.QQ_CLIENT_SECRET,
                     redirect_uri=settings.QQ_REDIRECT_URI,
                     state=settings.QQ_STATE
                     )
        qq_login_url = qq.get_qq_url()
        print(qq_login_url)
        return JsonResponse({'code':0,'errmsg':'ok','login_url':qq_login_url})

class QQOauthView(View):
    '''用户扫码登录回调处理'''
    def get(self, request):
        '''Oauth2.0认证'''
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseBadRequest('缺少code')