
from django.views import View
from django_redis import get_redis_connection
from apps.users.models import User,Address
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

class EmailVerifyView(View):
    """验证邮箱验证码"""

    def put(self, request):
        """验证邮箱的验证码，通过有修改用户邮箱验证状态"""
        # 1. 接收请求
        params = request.GET
        # 2. 获取参数
        token = params.get('token')
        # 3. 验证参数
        if token is None:
            return JsonResponse({'code': 400, 'errmsg': '参数缺失'})
        # 4. 获取user_id
        from apps.users.utils import check_verify_token
        user_id = check_verify_token(token)  # 解析验证邮箱中传递过来的token的值
        if user_id is None:
            return JsonResponse({'code': 400, 'errmsg': '参数错误'})
        # 5. 根据用户id查询数据
        user = User.objects.get(id=user_id)
        # 6. 修改数据
        user.email_active = True  # 当根据解析的token中的用户id和数据库中的用户id一致，那么设置该用户邮箱信息已经绑定
        user.save()
        # 7. 返回响应JSON
        return JsonResponse({'code': 0, 'errmsg': '邮箱信息绑定成功'})

class ChangePasswordView(LoginRequiredJsonMixin, View):
    """修改密码"""

    def put(self, request):
        """实现修改密码逻辑"""
        # 接收参数
        dict = json.loads(request.body.decode())
        old_password = dict.get('old_password')
        new_password = dict.get('new_password')
        new_password2 = dict.get('new_password2')

        # 校验参数
        if not all([old_password, new_password, new_password2]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        # 检查旧密码是否正确
        result = request.user.check_password(old_password)
        if not result:
            return JsonResponse({'code': 400, 'errmsg': '旧密码不正确'})
        # 校验密码是否符合规则
        if not re.match(r'^[0-9A-Za-z]{8,20}$', new_password):
            return JsonResponse({'code': 400, 'errmsg': '密码最少8位,最长20位'})
        # 校验2次密码是否一直
        if new_password != new_password2:
            return JsonResponse({'code': 400, 'errmsg': '两次输入密码不一致'})

        # 修改密码
        try:
            request.user.set_password(new_password)  # 修改密码
            request.user.save()
        except Exception as e:
            return JsonResponse({'code': 400, 'errmsg': '修改密码失败'})

        # 清除用户状态保持信息
        logout(request)

        response = JsonResponse({'code': 0, 'errmsg': 'ok'})

        response.delete_cookie('username') # 删除登录后的用户名信息

        # # 响应密码修改结果：重定向到登录界面
        return response

class AddressView(LoginRequiredJsonMixin, View):
    def get(self, request):
        """获取当前用户下的所有地址信息"""
        # 1.查询指定数据
        user = request.user
        # addresses=user.addresses # 该方法也可以查询出当前用户下的所有地址信息
        addresses = Address.objects.filter(user=user, is_deleted=False)  # 获取当前用户下的所有没有被删除（逻辑）的所有地址信息
        # 2.将对象数据转换为字典数据
        address_list = []
        for address in addresses:
            address_list.append({
                "id": address.id,
                "title": address.title,
                "receiver": address.receiver,
                "province": address.province.name,
                "city": address.city.name,
                "district": address.district.name,
                "place": address.place,
                "mobile": address.mobile,
                "tel": address.tel,
                "email": address.email
            })
        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'addresses': address_list})

    """新增地址"""
    def post(self, request):
        """实现新增地址逻辑"""
        # 判断是否超过地址上限：最多20个
        # Address.objects.filter(user=request.user).count()
        # count = request.user.addresses.count()
        # if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
        #     return JsonResponse({'code': RETCODE.THROTTLINGERR, 'errmsg': '超过地址数量上限'})
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
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return HttpResponseBadRequest('缺少必传参数')
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return HttpResponseBadRequest('参数mobile有误')
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return HttpResponseBadRequest('参数tel有误')
        if email:
            if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
                return HttpResponseBadRequest('参数email有误')

        # 保存地址信息
        try:
            address = Address.objects.create(
                user=request.user,
                title = receiver,
                receiver = receiver,
                province_id = province_id,
                city_id = city_id,
                district_id = district_id,
                place = place,
                mobile = mobile,
                tel = tel,
                email = email
            )
            # 设置默认地址
            if not request.user.default_address:
                request.user.default_address = address
                request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code':400, 'errmsg': '新增地址失败'})

        # 新增地址成功，将新增的地址响应给前端实现局部刷新
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "city": address.city.name,
            "district": address.district.name,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }
        # 响应保存结果
        return JsonResponse({'code': 0, 'errmsg': '新增地址成功', 'address':address_dict})

    def put(self, request, address_id):
        """修改和删除地址"""
        # 1、接收参数
        json_dict = json.loads(request.body.decode())  # 获取前端提交来的json数据
        receiver = json_dict.get('receiver')  # 获取收件人
        province_id = json_dict.get('province_id')  # 获取省份id
        city_id = json_dict.get('city_id')  # 获取城市id
        district_id = json_dict.get('district_id')  # 获取地址id
        place = json_dict.get('place')  # 获取地址信息
        mobile = json_dict.get('mobile')  # 获取手机号信息
        tel = json_dict.get('tel')  # 获取固定电话信息
        email = json_dict.get('email')  # 获取邮箱信息

        # 2、校验参数
        # 2-1、参数不全判断
        if not all([receiver, province_id, city_id, district_id, place, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})
        # 2-2、手机号码判断
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '参数手机号码格式有误'})
        # 2-3、固定号码有的时候需要判断
        if tel:
            if not re.match(r'^(0[0-9]{2,3}-)?([2-9][0-9]{6,7})+(-[0-9]{1,4})?$', tel):
                return JsonResponse({'code': 400, 'errmsg': '参数固定电话格式有误'})
        # 2-4、邮箱有的时候需要判断
        if email:
            if not re.match(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', email):
                return JsonResponse({'code': 400, 'errmsg': '参数email有误'})

        # 3、判断地址是否存在,并更新地址信息
        try:
            Address.objects.filter(id=address_id).update(
                user=request.user,
                title=receiver,
                receiver=receiver,
                province_id=province_id,
                city_id=city_id,
                district_id=district_id,
                place=place,
                mobile=mobile,
                tel=tel,
                email=email
            )
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '更新地址失败'})

        # 4、构造响应数据
        address = Address.objects.get(id=address_id)
        address_dict = {
            "id": address.id,
            "title": address.title,
            "receiver": address.receiver,
            "province": address.province.name,
            "province_id": address.province_id,
            "city": address.city.name,
            "city_id": address.city_id,
            "district": address.district.name,
            "district_id": address.district_id,
            "place": address.place,
            "mobile": address.mobile,
            "tel": address.tel,
            "email": address.email
        }

        # 响应更新地址结果
        return JsonResponse({'code': 0, 'errmsg': '更新地址成功', 'address': address_dict})

    def delete(self, request, address_id):
        """删除地址"""
        try:
            # 1、查询要删除的地址
            address = Address.objects.get(id=address_id)

            # 2、将地址逻辑删除设置为True
            address.is_deleted = True
            address.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '删除地址失败'})

        # 响应删除地址结果
        return JsonResponse({'code': 0, 'errmsg': '删除地址成功'})



class AddressDefaultView(LoginRequiredJsonMixin, View):
    """默认值"""
    def put(self, request, address_id):
        """设置默认地址"""
        try:
            # 接收参数,查询地址
            address = Address.objects.get(id=address_id)

            # 设置地址为默认地址
            request.user.default_address = address  # 设置当前用户的默认地址字段为查询到的当前地址信息
            request.user.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '设置默认地址失败'})
        # 响应设置默认地址结果
        return JsonResponse({'code': 0, 'errmsg': '设置默认地址成功'})




class UpdateTitleAddressView(LoginRequiredJsonMixin, View):
    """设置地址标题"""

    def put(self, request, address_id):
        """设置地址标题"""
        # 接收参数：地址标题
        json_dict = json.loads(request.body.decode())
        title = json_dict.get('title')

        try:
            # 查询地址
            address = Address.objects.get(id=address_id)

            # 设置新的地址标题
            address.title = title
            address.save()
        except Exception as e:
            logger.error(e)
            return JsonResponse({'code': 400, 'errmsg': '设置地址标题失败'})

        # 4.响应删除地址结果
        return JsonResponse({'code': 0, 'errmsg': '设置地址标题成功'})







