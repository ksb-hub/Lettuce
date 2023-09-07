from django.urls import path
from .views import CompareProductsView

urlpatterns = [
    path('compare/', CompareProductsView.as_view(), name='recommend-product'),
]