from rest_framework import permissions

from products.models import ProcessingMethod, Product, RoastingMethod, Variety, Weight, WeightSelection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from products.serializer import ProductSerializer, RoastingMethodSerializer, ProcessingMethodSerializer, VarietySerializer, WeightSelectionSerializer, WeightSerializer


class ProductListViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RoastingMethodsViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = RoastingMethod.objects.all()
    serializer_class = RoastingMethodSerializer


class ProcessingMethodsViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = ProcessingMethod.objects.all()
    serializer_class = ProcessingMethodSerializer


class VarietyViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = Variety.objects.all()
    serializer_class = VarietySerializer


class WeightSelectionViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = WeightSelection.objects.all()
    serializer_class = WeightSelectionSerializer


class WeightSelectionItemView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        weight_selection = WeightSelection.objects.filter(product=id).values()
        weights = Weight.objects.all().values()
        weights = list(weights)
        weight_selection = list(weight_selection)
        data = []
        for item in weight_selection:
            for weight in weights:
                if item['weight_id'] == weight['weight_id']:
                    data.append({'id': item['weight_selection_id'], 'weight': weight['weight'], 'price': item['price']})
        return Response(data)

