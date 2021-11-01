from django.shortcuts import *
from django.http import JsonResponse
from django.views import View
from apps.users.models import *
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