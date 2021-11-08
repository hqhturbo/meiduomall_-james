import json

from QQLoginTool.QQtool import OAuthQQ
from django.http import JsonResponse, HttpResponseBadRequest
from django.middleware import http
from django.views import View

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
            http.JsonResponse({'code': 400, 'errmsg': 'oauth2.0认证失败, 即获取 qq信息失败'})
            pass


# def post(self, request):
#     """美多商城⽤户绑定到openid"""
#     # 1. 接收请求
#     data = json.loads(request.body.decode())
#
#     # 2. 获取请求参数 openid
#     mobile = data.get('mobile')
#     password = data.get('password')
#     sms_code = data.get('sms_code')
#     access_token = data.get('access_token')
#
#     # 判断⼿机号是否合法
#     if not re.match(r'^1[3-9]\d{9}$', mobile):
#         return JsonResponse({'code': 400, 'errmsg': '请输⼊正确的⼿机号码'})









