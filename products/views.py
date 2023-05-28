from rest_framework import permissions

from products.models import ProcessingMethod, Product, RoastingMethod, Variety, Weight, WeightSelection, ProductVariety, \
    Category, MakingMethod, ProductMakingMethod
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from products.serializer import ProductSerializer, RoastingMethodSerializer, ProcessingMethodSerializer, \
    VarietySerializer, WeightSelectionSerializer, ProductVarietySerializer, CategorySerializer, MakingMethodSerializer


class ProductListViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, offset):
        queryset = Product.objects.all()[offset:9 + offset]
        serializer_class = ProductSerializer(queryset, many=True)
        return Response(serializer_class.data)


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


class ProductVarietyViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = ProductVariety.objects.all()
    serializer_class = ProductVarietySerializer


class ProductVarietyView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        queryset = ProductVariety.objects.filter(product_id=id)
        data = []
        for item in queryset:
            variety = Variety.objects.get(variety_id=item.variety_id)
            variety_serializer = VarietySerializer(variety)
            # product = Product.objects.get(product_id=item.product.product_id)
            # product_serializer = ProductSerializer(product)
            data.append(variety_serializer.data)
        return Response(data)

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


class ProductMakingMethodView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, id):
        data = []
        product_making_methods = ProductMakingMethod.objects.filter(product=id)
        for item in product_making_methods:
            making_method = MakingMethod.objects.get(making_method_id=item.making_method.making_method_id)
            serializer_class = MakingMethodSerializer(making_method)
            data.append(serializer_class.data)
        return Response(data)


class CategoriesViewSet(ModelViewSet):
    permission_classes = [permissions.AllowAny]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
