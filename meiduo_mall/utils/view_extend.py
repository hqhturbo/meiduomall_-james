from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin

# class LoginRequiredJsonMixin(AccessMixin):
#     """Verify that the current user is authenticated."""
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return JsonResponse({'code':401,'ermsg':'匿名用户,请登录','next':request.path})
#         return super().dispatch(request, *args, **kwargs)
from django.http import JsonResponse


class LoginRequiredJsonMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        return JsonResponse({'code': 401, 'ermsg': '匿名用户,请登录', 'next': self.request.path})
