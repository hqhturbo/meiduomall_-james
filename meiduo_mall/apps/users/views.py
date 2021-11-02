from django.shortcuts import *
from django.http import JsonResponse
from django.views import View
from apps.users.models import *
import json,re


# Create your views here.
class UsernameCountView(View):
    def get(self,request,username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code':200,'errmsg':'ok','count':count})


class MobileCountView(View):
    '''检查⽤户名重复'''
    def get(self, request, mobile):
        """
        :param request: 请求对象
        :param username: ⽤户名
        :return: JSON
        """
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': 200, 'errmsg': 'ok','count':count})


# 注册
class RegisterView(View):

    def post(self,request):
        # 1.接收参数：请求体中的JSON数据 request.body
        json_bytes = request.body  # 从请求体中获取原始的JSON数据，bytes类型的
        json_str = json_bytes.decode()  # 将bytes类型的JSON数据，转成JSON字符串
        json_dict = json.loads(json_str)  # 将JSON字符串，转成python的标准字典
        # json_dict = json.loads(request.body.decode())

        # 提取参数
        # 用户名
        username = json_dict.get('username')
        # 密码
        password = json_dict.get('password')
        # 确认密码
        password2 = json_dict.get('password2')
        # 手机号验证
        mobile = json_dict.get('mobile')
        # 图片验证
        allow = json_dict.get('allow')
        # 短信验证
        # sms_code = json_dict.get('sms_code')

        # 3. 验证数据
        # 3.1 ⽤户名，密码，确认密码，⼿机号，是否同意协议 都要有
        # all([xxx,xxx,xxx])
        # all⾥的元素 只要是 None,False
        # all 就返回False，否则返回True
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 3.2 ⽤户名满⾜规则，⽤户名不能重复
        if not re.match('[a-zA-Z_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '⽤户名不满⾜规则'})
        # 3.3 密码满⾜规则
        if not re.match('^\w{8,20}$', password):
            return JsonResponse({'code': 400, 'errmsg': '密码格式不正确'})
        # 3.4 确认密码和密码要⼀致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次密码不⼀致'})
        # 3.5 ⼿机号满⾜规则，⼿机号也不能重复
        if not re.match('^1[345789]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '⼿机号码格式不正确'})
        # 3.6 需要同意协议
        if not allow:
            return JsonResponse({'code': 400, 'errmsg': '必须同意协议'})

        # 4. 数据⼊库

        # user=User(username=username,password=password,moble=mobile)
        # user.save()
        # User.objects.create(username=username,password=password,mobile=mobile)

        # 以上2中⽅式，都是可以数据⼊库的

        # 但是 有⼀个问题 密码没有加密

        # 密码就加密（调⽤django系统模型⾃带⽅法）
        try:
            user = User.objects.create_user(username=username, password=password, mobile=mobile)
            return JsonResponse({'code': 200, 'errmsg': '注册成功!'})
        except Exception as e:
            logger.info(e)
            return JsonResponse({'code': 400, 'errmsg': '注册失败!'})










