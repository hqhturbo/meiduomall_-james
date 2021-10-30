from django.shortcuts import render

from django.http import JsonResponse
from django.views import View
from apps.users.models import User
# Create your views here.
class UsernameCountView(View):
    '''检查⽤户名重复'''
    def get(self, request, username):
        """
            :param request: 请求对象
            :param username: ⽤户名
            :return: JSON
        """
        count = User.objects.filter(username=username).count()
        print(username)
        if count == 0:
            return JsonResponse({'code': 200, 'errmsg': '用户名可以使用'})
        else:
            return JsonResponse({'code': 200, 'errmsg': '用户名重复了'})
