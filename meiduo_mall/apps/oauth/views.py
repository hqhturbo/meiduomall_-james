from django.views import View
from django import http
from django_redis import get_redis_connection
from django.http import JsonResponse
from QQLoginTool.QQtool import OAuthQQ
from meiduo_mall import settings
from apps.oauth.models import *
from django.contrib.auth import login
from apps.oauth.utils import *
import json,re
from apps.users.models import User
# 1 导入系统logging
import logging
# 2 创建日志署
logger = logging.getLogger('django')
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
        # print(qq_login_url)
        return JsonResponse({'code':0,'errmsg':'ok','login_url':qq_login_url})

class QQOauthView(View):
    '''用户扫码登录回调处理'''
    def get(self, request):
        '''Oauth2.0认证'''
        code = request.GET.get('code')
        if not code:
            return http.HttpResponseBadRequest('缺少code')

        # 创建工具对象
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,
                        client_secret = settings.QQ_CLIENT_SECRET,
                        redirect_uri=settings.QQ_REDIRECT_URI,
                        state=settings.QQ_STATE)
        # print(oauth)
        try:
            # 使用code向QQ服务器发送access_token
            access_token = oauth.get_access_token(code)
            # print(access_token)
            # 使用access_token向QQ服务器请求openid
            openid = oauth.get_open_id(access_token)
        except Exception as e:
            logging.error(e)
            http.JsonResponse({'code':400, 'errmsg':'oauth2.0认证失败, 即获取qq信息失败'})
        try:
            # 参看是否有openid对应的用户
            oauth_qq = OAuthQQUser.objects.get(openid=openid)
        except OAuthQQUser.DoesNotExist:
            # 如果openid没有绑定用户则：
            #使用加密类加密openid
            access_token = generate_access_token({'openid':openid})
            resp = JsonResponse({'code':400, 'access_token':access_token})
            return resp
        else:
            # 如果openid已绑定
            # 根据user外键获取对应的QQ用户
            user = oauth_qq.user

            # 状态保持
            login(request, user)

            # 创建重定向到首页的对象
            resp = JsonResponse({'code':0, 'errmsg':'ok'})
            u = json.dumps(user.nick_name)
            resp.set_cookie('username',u)
            return resp
    def post(self,request):
        '''美多商城用户绑定到openid'''
        # 1、接受请求
        data = json.loads(request.body.decode())
        # 2、获取请求参数  openid
        mobile = data.get('mobile')
        password = data.get('password')
        sms_code = data.get('sms_code')
        access_token = data.get('access_token')

        # print(mobile,password,sms_code,access_token)
        # 判断手机号是否合法
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return JsonResponse({'code':400,'errmsg':'手机号码格式错误'})
        # 判断密码是否合法
        if not re.match(r'^[a-zA-z0-9]{8,20}$',password):
            return JsonResponse({'code':400,'errmsg':'请输入8-20位数字或字母'})

        # 判断短信验证码是否一致
        # 创建redis对象
        redis_conn = get_redis_connection('code')

        # 从redis中获取sms_code的值
        sms_code_server = redis_conn.get('sms:%s' % mobile)

        # 判断获取出来的有没有
        if sms_code_server is None:
            # 如果没有，直接返回
            return JsonResponse({'code':400, 'errmsg':'短信验证码失效'})

        # 如果存在，对比输入的是否一致
        if sms_code != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg':'输入验证码有误'})

        # 添加access_token解密
        openid = check_access_token(access_token)
        if openid is None:
            return JsonResponse({'code': 400, 'errmsg':'access_token参数缺失'})

        # 根据手机号进行用户信息查询
        try:
            user = User.objects.get(mobile=mobile)
        except User.DoesNotExist:
            # 手机号不存在 创建一个user信息进行绑定
            user = User.objects.create_user(username=mobile,password=password,mobile=mobile)
        else:
            # 手机号存在 判断密码是否正确，密码正确直接保存（绑定）用户和openid信息
            if not user.check_password(password):
                return JsonResponse({'code': 400, 'errmsg':'账号或密码错误'})
        # 将用户信息和openid进行绑定写入表中
        openid = openid.get('openid')
        OAuthQQUser.objects.create(user=user, openid=openid)

        #状态保持
        login(request,user)
        # 返回响应
        resp = JsonResponse({'code':0, 'errmsg':'ok'})
        resp.set_cookie('username', json.dumps(user.username))

        return resp


