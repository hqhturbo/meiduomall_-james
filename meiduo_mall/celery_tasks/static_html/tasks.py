import os
import time
from django.conf import settings
from django.template import loader
from apps.ads.models import ContentCategory
from celery_tasks.main import celery_app
from utils.goods import get_categories
import logging

logging.getLogger('django')


# name：异步任务别名
@celery_app.task
def generate_static_index_html():
    """
    生成静态的主页html文件
    """
    print('%s: 首页静态化生成成功' % time.ctime())

    # 获取商品频道和分类
    categories = get_categories()

    # 广告内容
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')

    # 渲染模板
    context = {
        'categories': categories,
        'contents': contents
    }

    # 获取首页模板文件
    template = loader.get_template('index.html')
    # 渲染首页html字符串
    html_text = template.render(context)
    # 将首页html字符串写入到指定目录，命名'index.html'
    # settings.BASE_DIR 表示当前项目运行目录；os.path.dirname(settings.BASE_DIR) 表示当前项目的上级目录
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'meiduo_front_end_pc/index_test.html')
    print(file_path)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_text)
