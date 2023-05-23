from rest_framework import serializers

from reviews.models import Review, ReviewStatus


class OrderReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class ReviewStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewStatus
        fields = "__all__"