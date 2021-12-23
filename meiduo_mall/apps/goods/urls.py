from msilib.schema import ListView
from django.urls import path

from apps.goods.views import HotGoodsView,SkuSearchView

urlpatterns = [
    path('list/<category_id>/skus/', ListView.as_view()),
    path('hot/<category_id>/', HotGoodsView.as_view()),
    path('search/', SkuSearchView()),
]