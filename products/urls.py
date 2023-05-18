from django.urls import path, include
from rest_framework import routers
from products.views import *

router = routers.DefaultRouter()
router.register(r'products', ProductListViewSet)
router.register(r'roasting', RoastingMethodsViewSet)
router.register(r'processing', ProcessingMethodsViewSet)
router.register(r'variety', VarietyViewSet)
router.register(r'product_varieties', ProductVarietyViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('weight_selection/<int:id>/', WeightSelectionItemView.as_view(), name=''),
    path('product_list/<int:offset>/', ProductListView.as_view(), name=''),
    path('product_variety/<int:id>/', ProductVarietyView.as_view(), name=''),
]
