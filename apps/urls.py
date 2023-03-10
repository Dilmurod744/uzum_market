from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.ecommerce.views import CategoryModelViewSet, ShopModelViewSet, ProductModelViewSet, CartModelViewSet, \
    WishlistModelViewSet, OrderModelViewSet
from apps.user.views import ClientModelViewSet, MerchantModelViewSet, UserViewSet

router = DefaultRouter()
router.register('category', CategoryModelViewSet, 'category')
router.register('shop', ShopModelViewSet, 'shop')
router.register('product', ProductModelViewSet, 'product')
router.register('cart', CartModelViewSet, 'cart')
router.register('wishlist', WishlistModelViewSet, 'wishlist')
router.register('order', OrderModelViewSet, 'order')
router.register('user', UserViewSet, 'user')
router.register('client', ClientModelViewSet, 'client')
router.register('merchant', MerchantModelViewSet, 'merchant')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('apps.user.urls')),

]
