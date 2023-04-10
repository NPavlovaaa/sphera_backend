from django.urls import path, include
from rest_framework import routers
from products.views import *

router = routers.DefaultRouter()
router.register(r'products', ProductListViewSet)
router.register(r'roasting', RoastingMethodsViewSet)
router.register(r'processing', ProcessingMethodsViewSet)
router.register(r'variety', VarietyViewSet)
router.register(r'weight_selection', WeightSelectionViewSet)
router.register(r'weight', WeightViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:id>/', ProductListItemView.as_view(), name=''),
]
