from django import views
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


class WeightSelectionItemView(APIView):
    def get(self, request, id):
        weight_selection = WeightSelection.objects.filter(product=id).values()
        weights = Weight.objects.all().values()
        weights = list(weights)
        weight_selection = list(weight_selection)
        data = []
        for item in weight_selection:
            data_item = []
            for eee in weights:
                if item['weight_id'] == eee['weight_id']:
                    data_item.append(item['weight_selection_id'])
                    data_item.append(eee['weight'])
                    data_item.append(item['price'])
                    data.append(data_item)

        return Response(data)


class ProductListItemView(views.View):
    def get(self, request, id):
        product = Product.objects.get(product_id=id)
        serializer_class = ProductSerializer(product)
        return Response(serializer_class.data)


class ProccesListView(views.View):
    def get(request):
        processing_methods = Product.PROCESSING_METHODS
        print(processing_methods)
        return Response(processing_methods)