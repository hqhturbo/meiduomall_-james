import json,re
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse,HttpResponseBadRequest
# Create your views here.
from django.views import View


from apps.users.models import User, Address
from django_redis import get_redis_connection #导入redis包
from django.contrib.auth import authenticate,login,logout
from utils.view_extend import LoginrequiredJsonMixin
from apps.users.utils import check_verify_token
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
        response.set_cookie('username', u)
        return response

# 退出
class LogoutView(View):
    def delete(self,request):
        logout(request)
        response = JsonResponse({'code':200,'errmsg':'退出成功'})
        response.delete_cookie('username')
        return response

# 用户中心
class UserInfoView(LoginrequiredJsonMixin,View):
    def get(self,request):
        user = request.user
        if user is None:
            return JsonResponse({'code':400,'errmsg':'用户不存在'})

        user_data = {
            'username':user.username,
            'mobile':user.mobile,
            'email': user.email,
            'email_active':user.email_active,
        }
        return JsonResponse({'code':200,'errmsg':'ok','info_data':user_data})

# 验证邮箱
class EmailVerifyView(View):
    '''验证邮箱验证码'''
    def put(self,request):
        '''验证邮箱验证码，通过修改用户邮箱验证状态'''
        # 接受请求
        params = request.GET
        # 获取参数
        token = params.get('token')
        # 验证参数
        if token is None:
            return JsonResponse({'code': 400, 'errmsg':'参数缺失'})
        user_id = check_verify_token(token)  # 解析验证邮箱中传递过来的token的值
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg':'参数错误'})
        # 根据用户id查询数据
        user = User.objects.get(id=user_id)
        # 修改数据
        user.email_active = True  # 当根据解析的token中的用户id和数据库中的用户id一致，那么设置该用户邮箱信息已经绑定
        user.save()
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg':'邮箱绑定成功'})

class CreateAddressViwe(LoginrequiredJsonMixin,View):
    def get(self,request):
        '''获取当前用户下的所有地址'''
        # 查询指定数据
        user = request.user
        # addresses=user.addresses # 该方法也可以查询出当前用户下的所有地址信息
        addresses = Address.objects.filter(user=user,is_deleted=False)  #获取当前用户下的所有没有删除（逻辑）的所有地址信息
        # 将数据转换为字典
        address_list = []
        for address in addresses:
            address_list.append({
                "id":address.id,
                "title":address.title,
                "receiver":address.receiver,
                "province":address.province.name,
                "city":address.city.name,
                "district":address.district.name,
                "place":address.place,
                "mobile":address.mobile,
                "tel":address.tel,
                "email":address.email,
            })
        # 返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok','addresses':address_list})
    '''新增地址'''
    def post(self,request):
        '''实现新增地址逻辑'''
        # 判断是否超过地址上线：最多20个
        # count = request.user.addresses.count()
        # if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
        #     return JsonResponse({'code':400,'errmsg':'超过地址数量上限'})
        # 接收参数
        json_dict = json.loads(request.body.decode())
        receiver = json_dict.get('receiver')
        province_id = json_dict.get('province_id')
        city_id = json_dict.get('city_id')
        district_id = json_dict.get('district_id')
        place = json_dict.get('place')
        mobile = json_dict.get('mobile')
        tel = json_dict.get('tel')
        email = json_dict.get('email')

        # 校验参数
        if not all([receiver,province_id,city_id,district_id,place,mobile]):
            return HttpResponseBadRequest('缺少必要参数')
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return HttpResponseBadRequest('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$',tel):
                return HttpResponseBadRequest('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return HttpResponseBadRequest('参数email有误')
        # 保存地址信息
        try:
            address = Address.objects.create(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email,
            )
            # 设置默认地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code':400,'errmsg':'新增地址失败'})
        # 新增地址成功，将新增地址响应给前端实现局部刷新
        address_dict = {
            "id":address.id,
            "title":address.title,
            "receiver":address.receiver,
            "province":address.province.name,
            "city":address.city.name,
            "district":address.district.name,
            "place":address.place,
            "mobile":address.mobile,
            "tel":address.tel,
            "email":address.email,
        }
        return JsonResponse({"code": 0, "errmsg":'新增地址成功',"address":address_dict })
