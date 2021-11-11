from django.shortcuts import render
from django.views import View
from random import randint
from django.http import JsonResponse, HttpResponse
from libs.captcha.captcha import captcha  #导入图片验证码库
from django_redis import get_redis_connection #导入redis包
from celery_tasks.sms.tasks import send_sms_code
import json,re
from celery_tasks.email.tasks import send_mail
from apps.users.utils import generic_email_verify_token
# from libs.yuntongxun.sms import CCP
# Create your views here.

# 1 导入系统logging
import logging
# 2 创建日志署
from meiduo_mall.settings import EMAIL_FROM, EMAIL_VERIFY_URL

logger = logging.getLogger('django')

# 图片验证码
class ImageCodeView(View):
    def get(self,request,uuid):
        if uuid is None:
            # print('uuid无')
            return JsonResponse({'code': 200, 'errmsg': 'ok'})
        else:
            # print(image_code_id)
            text ,image = captcha.generate_captcha()
            redis_conn = get_redis_connection('code')
            redis_conn.setex(name='img:%s' % uuid, time=300, value=text)
            return HttpResponse(image,content_type='image/jpeg')

# 短信验证码
class SmscodeView(View):
    def get(self,request,mobile):
        # 获取前端传回的值
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 对传输的值进行判断
        if not all([mobile,image_code,uuid]):
            return JsonResponse({'code':400,'errmsg':'参数不齐全'})
        # 图片验证码验证
        redis_conn = get_redis_connection('code')
        image_code_redis = redis_conn.get('img:%s' % uuid)
        if image_code_redis is None:
            return JsonResponse({'code':400,'errmsg':'图片验证码不存在'})
        try:
            redis_conn.delete('img:%s' % uuid)
        except Exception as e:
            logger.error(e)
        if image_code.lower() != image_code_redis.decode().lower():
            return JsonResponse({'code':400,'errmsg':'图片验证码输入错误'})
        # 获取redis中已存在的标记是否已经存在
        send_flag = redis_conn.get('send_flag:%s' % mobile)
        if send_flag:
            return JsonResponse({'code': 400, 'errmsg':'发送短信过于频繁请稍后'})
        sms_code = '%06d' % randint(0,999999)
        print('你的验证码是',sms_code)
        # 保存短信验证码和电话号码标记
        pl = redis_conn.pipeline()
        pl.setex('sms:%s' % mobile, 300, sms_code)
        pl.setex('send_flag:%s' % mobile,60,1)
        pl.execute()
        # CCP().send_template_sms('17691149837', [sms_code, 5], 1)
        # 调用发送短信验证码函数
        send_sms_code.delay(mobile, sms_code)
        return JsonResponse({'code':200,'errmsg':'验证码发送成功'})

class EmailView(View):
    '''添加邮箱'''
    def put(self,request):
        # 接收参数
        json_dict = json.loads(request.body.decode())
        email = json_dict.get('email')
        if not email:
            return JsonResponse({'code': 400, 'errmsg':'缺少email参数'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$',email):
            return JsonResponse({'code': 400, 'errmsg':'参数email有误'})

        # 赋值email字段
        try:
            request.user.email = email
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg':'添加邮箱失败'})
        token = generic_email_verify_token(request.user.id) # 生成邮箱验证token
        verif_url = f"{EMAIL_VERIFY_URL}?token={token}"   # 拼接验证邮箱地址
        html_message = '<p>尊敬的用户您好！</p>' \
                       '<p>感谢您使用美多商城，</p>' \
                       '<p>您的邮箱为 %s ，请点击此链接激活您的邮箱，</p>' \
                       '<p><a href="%s">%s<a></p>' % (email,verif_url,verif_url)
            # 响应添加邮箱结果
        send_mail(subject='美多商城激活邮件',message='',from_email=EMAIL_FROM,recipient_list=[email],html_message=html_message)
        return JsonResponse({'code':0, 'errmsg':'添加邮箱成功'})
