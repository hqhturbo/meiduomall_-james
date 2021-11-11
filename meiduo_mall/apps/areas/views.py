from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from apps.areas.models import *
from django.core.cache import cache
# Create your views here.
import logging

logger = logging.getLogger('django')
class AreaView(View):
    def get(self,request):
        '''所有省份'''
        # 查询缓存数据
        province_list = cache.get('province')
        if province_list is None:
            try:
                provinces = Area.objects.filter(parent=None)
            except Exception as e:
                logger.error(e)
        # 由于JsonResponse不能将QuerySet对象转换为Json类型，说以需要将其转换为字典
        # 2.将对象转换为字典数据
            province_list = []
            for province in provinces:
                province_list.append({
                    'id':province.id,
                    'name':province.name
                })
            cache.set('province',province_list,24 * 3600)
        return JsonResponse({'code':0,'errmsg':'ok','province_list':province_list})

class SubAreasView(View):
    '''市区数据'''

    def get(self,request,id):
        '''提供省市区数据'''

        # 获取缓存数据
        data_list = cache.get(f'city:{id}')
        if data_list is None:

            # 提供市或区数据
            try:
                parent_model = Area.objects.get(id=id)  # 查询市或区的父级
                sub_model_list = parent_model.subs.all()

                # 序列化市或区数据
                sub_list=[]
                for sub_model in sub_model_list:
                    sub_list.append({'id':sub_model.id,'name':sub_model.name})
                sub_data = {
                    'id':parent_model.id,  #父级pk
                    'name':parent_model.name,  #父级name
                    'subs':sub_list  #父级的子集
                }
                cache.set(f'city:{id}',sub_data,24*3600)
            except Exception as e:
                logger.error(e)
                return JsonResponse({'code':400,'errmsg':'城市或区数据错误'})
        return JsonResponse({'code':0,'errmsg':'ok','sub_data':sub_data})