from rest_framework import serializers

from products.models import Product, RoastingMethod, ProcessingMethod, Variety, Weight, WeightSelection, ProductVariety, \
    Category


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


class VarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = Variety
        fields = "__all__"


class ProductVarietySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariety
        fields = "__all__"


class WeightSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeightSelection
        fields = "__all__"


class WeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Weight
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
