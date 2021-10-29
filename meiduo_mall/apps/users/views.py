from django.shortcuts import *
from django.http import JsonResponse
from django.views import View
from apps.users.models import *
# Create your views here.
class UsernameCountView(View):
    def get(self,request):
        username = request.GET.get('username')
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code':200,'errmsg':'ok','count':count})