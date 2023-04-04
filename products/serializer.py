from rest_framework import serializers

from products.models import Product, RoastingMethod, ProcessingMethod


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

class RoastingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoastingMethod
        fields = "__all__"

class ProcessingMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessingMethod
        fields = "__all__"
