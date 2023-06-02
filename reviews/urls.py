from django.urls import path, include
from rest_framework import routers

from reviews.views import *

router = routers.DefaultRouter()
router.register(r'review_statuses', ReviewStatusesViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('reviews/', OrdersReviewListView.as_view()),
    path('product_reviews/', ProductsReviewListView.as_view()),
    path('create_review/', OrdersReviewCreateView.as_view()),
    path('create_review_product/', ProductsReviewCreateView.as_view()),
    path('review_update/', OrdersReviewUpdateView.as_view()),
    path('product_review_update/', ProductsReviewUpdateView.as_view()),
]
