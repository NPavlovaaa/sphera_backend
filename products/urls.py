from django.urls import path, include
from rest_framework import routers
from products.views import *

router = routers.DefaultRouter()
router.register(r'products', ProductListViewSet)
router.register(r'roasting', RoastingMethodsViewSet)
router.register(r'processing', ProcessingMethodsViewSet)
router.register(r'variety', VarietyViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('weight_selection/<int:id>/', WeightSelectionItemView.as_view(), name=''),
]
