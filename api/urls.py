from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, BannerViewSet, OrderViewSet
from .views_tags import TagView
from .views_basket import BasketView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'banners', BannerViewSet, basename='banner')
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('catalog/', ProductViewSet.as_view({'get': 'catalog'}), name='product-catalog'),
    path('tags/', TagView.as_view(), name='tags'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('basket', BasketView.as_view(), name='basket-no-slash'),  # Handle without trailing slash
]
