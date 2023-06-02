from django.urls import path, include
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('registration/', CreateUserAndClientModelView.as_view(), name=''),
    path('customers/', CustomerView.as_view(), name=''),
    path('create_income_change/', AdminIncomeChangeView.as_view(), name=''),
]
