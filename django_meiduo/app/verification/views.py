
from django_redis import get_redis_connection
from libs.captcha.captcha import captcha
from django.views import View
from django.http import HttpResponse
class ImageCodeView(View):
    def get(self, request, uuid):
        print(uuid)
        # ⽣成图⽚验证码
        text,image = captcha.generate_captcha()
        # 保存图⽚验证码
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s' % uuid, 300, text)
        return HttpResponse(image, content_type='image/jpeg')

