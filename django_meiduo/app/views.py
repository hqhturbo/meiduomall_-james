from django.http import JsonResponse
from django.views import View
from app.models import User


# Create your views here.
class UsernameCountView(View):
    '''检查⽤户名重复'''
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 200, 'errmsg': 'ok', 'count': 1})
