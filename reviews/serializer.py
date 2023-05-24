from rest_framework import serializers

from reviews.models import Review, ReviewStatus, ReviewsProduct


class OrderReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ProductReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewsProduct
        fields = "__all__"


class ReviewStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewStatus
        fields = "__all__"