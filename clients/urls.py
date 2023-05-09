from django.urls import path, include
from rest_framework import routers
from clients.views import *

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'carts', CartViewSet)
router.register(r'favorites', FavoriteViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name=''),
    path('cart_in_orders/', CartOrdersView.as_view(), name=''),
    path('admin_carts/', CartAdminView.as_view(), name=''),
    path('cart_addition/', CartView.as_view(), name=''),
    path('favorite/<int:id>/', FavoriteView.as_view(), name=''),
    path('product_cart/<int:product>/<int:weight_selection>/', ProductInCartView.as_view(), name=''),
]