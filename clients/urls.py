from django.urls import path, include
from rest_framework import routers

from clients.views import ClientViewSet, ClientView

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
