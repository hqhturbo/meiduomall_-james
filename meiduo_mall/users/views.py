from django.shortcuts import render
from django.http import JsonResponse


# Create your views here.

def check_name(request):
    name=request.GET.get('name')

    return JsonResponse({'code': 0, 'errmsg': name})
