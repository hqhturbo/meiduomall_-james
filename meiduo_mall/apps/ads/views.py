from django.shortcuts import render
from django.views import View
# Create your views here.
from apps.ads.models import ContentCategory


class IndexView(View):
    """首页广告"""

    def get(self, request):
        """提供首页广告界面"""
        # 查询商品频道和分类
        # 广告数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

        # 渲染模板的上下文
        context = {
            # 'categories': categories,
            'contents': contents,
        }
        return render(request, 'index.html', context)

# class IndexView(View):
#
#     def get(self,request):
#
#         """
#         首页的数据分为2部分
#         1部分是 商品分类数据
#         2部分是 广告数据
#
#         """
#         # 1.商品分类数据
#         categories=get_categories()
#         # 2.广告数据
#         contents = {}
#         content_categories = ContentCategory.objects.all()
#         for cat in content_categories:
#             contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
#
#         # 我们的首页 后边会讲解页面静态化
#         # 我们把数据 传递 给 模板
#         context = {
#             'categories': categories,
#             'contents': contents,
#         }
#         # 模板使用比较少，以后大家到公司 自然就会了
#         return render(request,'index.html',context)
