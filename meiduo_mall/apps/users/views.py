import json
import logging
from libs.captcha.captcha import captcha # 导入验证码
from django.shortcuts import *
from django.http import JsonResponse
from django_redis import get_redis_connection
from django.views import View
from apps.users.models import *
logger = logging.getLogger('django_log')
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
        if not all([username,password,password2,mobile]):
            return JsonResponse({'code':400,'errmsg':'参数不全'})
        try:
            User.objects.create_user(username=username,password=password,mobile=mobile)
            return JsonResponse({'code': 200, 'errmsg': '注册成功'})
        except Exception as e:
            logger.info(e)
            return JsonResponse({'code':400,'errmsg':'注册失败'})
class ImageCountView(View):
    def get(self,request,uuid):
        if uuid is None:
            return HttpResponse('没有获取到uuid')
        txt, image = captcha.generate_captcha()
        redis_conn = get_redis_connection()
        redis_conn.setex(name='img:%s' % uuid,time=300,value=txt)
        return HttpResponse(image, content_type='image/jpeg')
