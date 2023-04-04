from products.models import ProcessingMethod, Product, RoastingMethod, Variety, Weight, WeightSelection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from products.serializer import ProductSerializer, RoastingMethodSerializer, ProcessingMethodSerializer, VarietySerializer, WeightSelectionSerializer, WeightSerializer

class ProductListViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RoastingMethodsViewSet(ModelViewSet):
    queryset = RoastingMethod.objects.all()
    serializer_class = RoastingMethodSerializer


class ProcessingMethodsViewSet(ModelViewSet):
    queryset = ProcessingMethod.objects.all()
    serializer_class = ProcessingMethodSerializer


class VarietyViewSet(ModelViewSet):
    queryset = Variety.objects.all()
    serializer_class = VarietySerializer


class WeightSelectionViewSet(ModelViewSet):
    queryset = WeightSelection.objects.all()
    serializer_class = WeightSelectionSerializer


class WeightViewSet(ModelViewSet):
    queryset = Weight.objects.all()
    serializer_class = WeightSerializer