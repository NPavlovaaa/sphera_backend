from django.urls import path, include
from rest_framework import routers
from clients.views import *

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'carts', CartViewSet)
# router.register(r'favorites', FavoriteViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name=''),
    path('cart_in_orders/', CartOrdersView.as_view(), name=''),
    path('admin_carts/', CartAdminView.as_view(), name=''),
    path('cart_addition/', CartView.as_view(), name=''),
    path('favorites/', FavoriteListView.as_view()),
    path('create_favorite/', FavoriteListView.as_view()),
    path('favorite_detail/<int:product>/', FavoriteDetailView.as_view()),
    path('favorite_delete/<int:id>/', FavoriteDetailView.as_view()),
    # path('favorite/<int:product>/', FavoriteView.as_view(), name=''),
    # path('favorite_list/', FavoriteListView.as_view(), name=''),
    path('product_cart/<int:product>/<int:weight_selection>/', ProductInCartView.as_view(), name=''),
    path('achievements/', ClientAchievementsView.as_view(), name=''),
]