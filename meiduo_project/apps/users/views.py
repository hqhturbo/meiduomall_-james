from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views import View
from django_redis import get_redis_connection
from apps.users.models import User
import json, re
from django.contrib.auth import authenticate, logout, login
from apps.users.utils import generic_email_verify_token
import logging

logger = logging.getLogger('django')






class UsernameCountView(View):
    '''检查⽤户名重复'''

    def get(self, request, username):  # url路由方式来传递username参数
        """
        :param request: 请求对象
        :param username: ⽤户名
        :return: JSON
        """
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 200, 'errmsg': 'ok', 'count': count})


class MobileCountView(View):
    '''检查⽤户名重复'''
    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param username: ⽤户名
        :return: JSON
        """
        count = User.objects.filter(mobile__exact=mobile).count()
        return JsonResponse({'code': 200, 'errmsg': 'ok', 'count': count})

#注册
class RegisterView(View):
    """⽤户注册"""

    def post(self, request):
        """
        实现⽤户注册
        :type request: object
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
        allow = json_dict.get("allow")
        sms_code_client = json_dict.get('sms_code')
        redis_conn = get_redis_connection('code')
        sms_code_server = redis_conn.get(f'sms:{mobile}')

        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        if not re.match('[a-zA-Z_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规范'})
        if not re.match('^\w{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': '密码格式不正确'})
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次密码不一致'})
        if not re.match('^1[345789]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号码格式不正确'})
        if not sms_code_server:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码失效'})
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码错误'})
        if not allow:
            return JsonResponse({'code': 400, 'errmsg': '必须同意协议'})
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
            return JsonResponse({'code': 200, 'errmsg': '注册成功'})
        except Exception as e:
            logger.info(e)
            return JsonResponse({'code': 400, 'errmsg': '注册失败'})
        # 如何设置session信息
        request.session['user_id'] = user.id
        # login(request, user), 该⽅法会将当前已登录的⽤户写⼊session中，并将sessionid写⼊cookie发送给浏览器
        # 状态保持 -- 登录⽤户的状态保持
        # user 已经登录的⽤户信息
        login(request, user)

#登录
class LoginView(View):

    def post(self, request):
        # 1.接收参数
        dict = json.loads(request.body.decode())  # 获取json⽅式提交的数据
        username = dict.get('username')
        password = dict.get('password')
        remember = dict.get('remember')

        if not all([username,password]):
            return JsonResponse({'code': 400, 'errmsg':'缺少必传参数'})

        import re
        if re.match('^1[3-9]\d{9}$', username):
            # ⼿机号
            User.USERNAME_FIELD = 'mobile'
            user = authenticate(mobile=username, password=password)
        else:
            # account 是⽤户名
            # 根据⽤户名从数据库获取 user 对象返回.
            User.USERNAME_FIELD = 'username'
            user = authenticate(username=username,password=password)

        if user == None:
            return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误'})

        login(request,user)

        if remember != True:
            request.session.set_expiry(0)
        else:
            request.session.set_expiry(None)

        resp =  JsonResponse({'code':0, 'errmsg':'ok'})
        username = json.dumps(user.nick_name)
        resp.set_cookie('username',username)
        return resp

#退出
class LogoutView(View):
    def delete(self,request):
        logout(request)
        response = JsonResponse({"code":200,"errmsg":"退出成功"})
        response.delete_cookie('username')
        return response


from utils.view_extend import *
class UserInfoView(LoginRequiredJsonMixin, View):
    def get(self, request):
        user = request.user
        if user is None:
            return JsonResponse({"code": 400, "errmsg": "未找到该用户信息"})
        else:
            user_info = {
                'username': user.nick_name,
                'mobile': user.mobile,
                'email': user.email,
                'email_active': user.email_active
            }
            return JsonResponse({"code": 200, "errmsg": "ok", "info_data": user_info})


class EmailView(View):
    def put(self, request):
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')
        if not email:
            return JsonResponse({'code': 400, 'errmsg':'缺少email参数'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return JsonResponse({'code': 400, 'errmsg': '参数email有误'})
        try:
            request.user.email =email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '添加邮箱失败'})
        token = generic_email_verify_token(request.user.id)
        from meiduo_project.settings import EMAIL_VERIFY_URL
        verify_url = f"{EMAIL_VERIFY_URL}?token={token}"
        html_message = '<p>尊敬的用户您好</p>' \
                       '<p>感谢你使用美多商城</p>' \
                       '<p>你的邮箱威：%s。请点击此链接激活你的邮箱,</p>' \
                       '<p><a href="%s">%s</a></p>' % (email, verify_url, verify_url)
        from meiduo_project.settings import EMAIL_FROM
        from django.core.mail import send_mail
        send_mail(subject='美多商城激活邮件',message='',from_email=EMAIL_FROM,recipient_list=[email],html_message=html_message)
        return JsonResponse({'code': 0, 'errmsg':'添加邮箱成功'})