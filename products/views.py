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


# class WeightViewSet(ModelViewSet):
#     queryset = Weight.objects.all()
#     serializer_class = WeightSerializer


class WeightSelectionItemView(APIView):
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


class RoastingMethodView(APIView):
    def get(self, request, id):
        data = RoastingMethod.objects.get(roasting_method_id=id)
        serializer_class = RoastingMethodSerializer(data)
        return Response(serializer_class.data)


class ProcessingMethodView(APIView):
    def get(self, request, id):
        data = ProcessingMethod.objects.get(processing_method_id=id)
        serializer_class = ProcessingMethodSerializer(data)
        return Response(serializer_class.data)


class VarietyView(APIView):
    def get(self, request, id):
        data = Variety.objects.get(variety_id=id)
        serializer_class = VarietySerializer(data)
        return Response(serializer_class.data)
