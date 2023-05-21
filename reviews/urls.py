from django.urls import path, include
from rest_framework import routers
from reviews.views import *

router = routers.DefaultRouter()
# router.register(r'reviews', OrdersReviewViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('reviews/', OrdersReviewListView.as_view()),
    path('create_review/', OrdersReviewCreateView.as_view()),
]
