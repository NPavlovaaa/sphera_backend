from django.urls import path, include
from rest_framework import routers
from orders.views import *
from . import views


router = routers.DefaultRouter()
router.register(r'delivery_methods', DeliveryMethodViewSet)
router.register(r'orders', OrderViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('create_order/', OrderView.as_view()),
    path('my_orders/<int:id>/', OrderView.as_view(), name=''),
    path('admin_orders/<str:token>/', OrdersAdminView.as_view(), name=''),
]