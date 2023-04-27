from rest_framework import serializers

from orders.models import DeliveryMethod


class DeliveryMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryMethod
        fields = "__all__"


