from django.urls import path, include
from rest_framework import routers
from orders.views import *


router = routers.DefaultRouter()
router.register(r'delivery_methods', DeliveryMethodViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_order/', OrderView.as_view()),
    path('get_orders/', OrderView.as_view(), name=''),
    path('incomes/', IncomeView.as_view(), name=''),
]