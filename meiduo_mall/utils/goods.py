# -*- coding:utf-8 -*-
from collections import OrderedDict
from apps.goods.models import GoodsCategory
from apps.goods.models import GoodsChannel

"""
分类数据
"""


def get_categories():

    # 定义一个有序字典对象
    categories = OrderedDict()

    # 对 GoodsChannel 进行 group_id 和 sequence 排序, 获取排序后的结果:
    channels = GoodsChannel.objects.order_by('group_id',
                                             'sequence')

    # 遍历排序后的结果: 得到所有的一级菜单( 即,频道 )
    for channel in channels:
        # 从频道中得到当前的 组id
        group_id = channel.group_id

        # 判断: 如果当前 组id 不在我们的有序字典中:
        if group_id not in categories:
            # 我们就把 组id 添加到 有序字典中
            # 并且作为 key值, value值 是 {'channels': [], 'sub_cats': []}
            categories[group_id] =  {
                                     'channels': [],
                                     'sub_cats': []
                                    }

        # 获取当前频道的分类名称
        cat1 = channel.category

        # 给刚刚创建的字典中, 追加具体信息:
        # 即, 给'channels' 后面的 [] 里面添加如下的信息:
        categories[group_id]['channels'].append({
            'id':   cat1.id,
            'name': cat1.name,
            'url':  channel.url
        })

        # 根据 cat1 的外键反向, 获取下一级(二级菜单)的所有分类数据, 并遍历:
        cat2s = GoodsCategory.objects.filter(parent=cat1)
        # cat1.goodscategory_set.all()
        for cat2 in cat2s:
            # 创建一个新的列表:
            cat2.sub_cats = []
            cat3s = GoodsCategory.objects.filter(parent=cat2)
            # 根据 cat2 的外键反向, 获取下一级(三级菜单)的所有分类数据, 并遍历:
            for cat3 in cat3s:
                # 拼接新的列表: key: 二级菜单名称, value: 三级菜单组成的列表
                cat2.sub_cats.append(cat3)
            # 所有内容在增加到 一级菜单生成的 有序字典中去:
            categories[group_id]['sub_cats'].append(cat2)

    return categories

    """
    面包屑
    """

def get_breadcrumb(category):
    '''接收最低级别的类别, 获取各个类别的名称, 返回'''

    dict = {
        'cat1': '',
        'cat2': '',
        'cat3': '',
    }

    if category.parent is None:
        dict['cat1'] = category.name
    elif category.parent.parent is None:
        dict['cat2'] = category.name
        dict['cat1'] = category.parent.name
    else:
        dict['cat3'] = category.name
        dict['cat2'] = category.parent.name
        dict['cat1'] = category.parent.parent.name

    return dict

