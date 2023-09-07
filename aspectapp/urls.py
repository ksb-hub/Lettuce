# aspectapp/urls.py

from django.urls import path
from .views import AspectProductsView

urlpatterns = [
    path('aspect/', AspectProductsView.as_view(), name='compare-products'),
    # 다른 URL 패턴들을 여기에 추가할 수 있습니다.
]