from django.urls import path, include
from rest_framework import routers
from products.views import *

router = routers.DefaultRouter()
router.register(r'products', ProductListViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('weight_selection/<int:id>/', WeightSelectionItemView.as_view(), name=''),
    path('roasting/<int:id>/', RoastingMethodView.as_view(), name=''),
    path('processing/<int:id>/', ProcessingMethodView.as_view(), name=''),
    path('variety/<int:id>/', VarietyView.as_view(), name=''),

]
