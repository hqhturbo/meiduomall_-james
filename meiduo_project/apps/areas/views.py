from django.http import JsonResponse
from django.shortcuts import render
from django.core.cache import cache
# Create your views here.
from django.views import View

from apps.areas.models import Area
from apps.users.views import logger

class AreaView(View):

    def get(self, request):
        """所有省份"""
        # 先查询缓存数据
        province_list = cache.get('province')
        # 如果没有缓存，则查询数据库，并缓存数据
        if province_list is None:
            # 1.查询省份信息
            try:
                provinces = Area.objects.filter(parent=None)
            except Exception as e:
                logger.error(e)

            # 由于JsonResponse不能将QuerySet对象转换为Json类型，说以需要将其转换为字典
            # 2.将对象转换为字典数据
            province_list = []
            for province in provinces:
                province_list.append({
                    'id': province.id,
                    'name': province.name
                })

            # 保存缓存数据
            # cache.set(key,value,expire)
            cache.set('province', province_list, 24 * 3600)
        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})

class SubAreaView(View):

    def get(self, request, id):
        """所有市或区"""
        # 先获取缓存数据
        data_list = cache.get(f'city:{id}')

        if data_list is None:  # 缓存中没有数据
            # 1.获取省份id、市的id,查询信息
            # Area.objects.filter(parent_id=id)
            # Area.objects.filter(parent=id)

            up_level = Area.objects.get(id=id)  # 根据id查找 省或市
            down_level = up_level.subs.all()  # 自定义的外键字段（省或市对应下的 市或区）
            # 2.将对象转换为字典数据
            data_list = []
            for item in down_level:
                data_list.append({
                    'id': item.id,
                    'name': item.name
                })

            # 缓存数据
            cache.set(f'city:{id}', data_list, 24 * 3600)

        # 3.返回响应
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': data_list}})

