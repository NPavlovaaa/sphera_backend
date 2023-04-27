from django.urls import path, include
from rest_framework import routers
from orders.views import *

router = routers.DefaultRouter()
router.register(r'delivery_methods', DeliveryMethodViewSet)


urlpatterns = [
    path('', include(router.urls)),
]