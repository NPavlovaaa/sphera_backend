from django.urls import path, include
from rest_framework import routers
from products.views import *

router = routers.DefaultRouter()
router.register(r'products', ProductListViewSet)
# router.register(r'roasting', RoastingMethodsViewSet)
# router.register(r'processing', ProcessingMethodsViewSet)
# router.register(r'variety', VarietyViewSet)
# router.register(r'weight_selection', WeightSelectionViewSet)
# router.register(r'weight', WeightViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('products/<int:id>/', ProductListItemView.as_view(), name=''),
    path('weight_selection/<int:id>/', WeightSelectionItemView.as_view(), name=''),
    path('roasting/<int:id>/', RoastingMethodView.as_view(), name=''),
    path('processing/<int:id>/', ProcessingMethodView.as_view(), name=''),
    path('variety/<int:id>/', VarietyView.as_view(), name=''),

]
