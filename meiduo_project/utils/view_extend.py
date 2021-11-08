from django.contrib.auth.mixins import LoginRequiredMixin,AccessMixin

from django.http import JsonResponse




class LoginRequiredJsonMixin(AccessMixin):
    def dispatch(self,request,*arge,**kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'code':401,'errmsg':'匿名用户，请登录','next':request.path})
        return super().dispatch(request, * arge, ** kwargs)


