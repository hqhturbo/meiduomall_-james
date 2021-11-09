from django.contrib.auth.mixins import AccessMixin
from django.http import JsonResponse


class LoginRequiredJsonMixin(AccessMixin):
    """Verify that the current user is authenticated."""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'code':401,'errmsg':'匿名用户禁止登陆','next':request.path})
        return super().dispatch(request, *args, **kwargs)