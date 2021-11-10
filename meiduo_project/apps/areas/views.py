# from django.http import JsonResponse
# from django.shortcuts import render
#
# # Create your views here.
# from django.views import View
#
# from apps.areas.models import Area
# from apps.users.views import logger
#
#
# class AreaView(View):
#
#     def get(self, request):
#         try:
#             provinces = Area.objects.filter(parent=None)
#         except Exception as e:
#             logger.error(e)
#         # 由于JsonResponse不能将QuerySet对象转换为Json类型，说以需要将其转换为字典
#         # 2.将对象转换为字典数据
#         province_list = []
#         for province in provinces:
#             province_list.append({
#                 'id': province.id,
#                 'name': province.name
#             })
#         # 3.返回响应
#         return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})
#
# class SubAreasView(View):
#     """市区数据"""
#
#     def get(self, request, pk):
#         """提供省市区数据"""
#
#         # 提供市或区数据
#         try:
#             parent_model = Area.objects.get(id=pk)  # 查询市或区的父级
#             sub_model_list = parent_model.subs.all()
#
#             # 序列化市或区数据
#             sub_list = []
#             for sub_model in sub_model_list:
#                 sub_list.append({'id': sub_model.id, 'name': sub_model.name})
#
#             sub_data = {
#                 'id': parent_model.id,  # 父级pk
#                 'name': parent_model.name,  # 父级name
#                 'subs': sub_list  # 父级的子集
#             }
#         except Exception as e:
#             logger.error(e)
#             return JsonResponse({'code': 400, 'errmsg': '城市或区数据错误'})
#
#         # 响应市或区数据
#         return JsonResponse({'code': 0, 'errmsg': 'OK', 'sub_data': sub_data})
#
#
#
