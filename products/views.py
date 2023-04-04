from products.models import ProcessingMethod, Product, RoastingMethod
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from products.serializer import ProductSerializer, RoastingMethodSerializer, ProcessingMethodSerializer

class ProductListViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class RoastingMethodsViewSet(ModelViewSet):
    queryset = RoastingMethod.objects.all()
    serializer_class = RoastingMethodSerializer

class ProcessingMethodsViewSet(ModelViewSet):
    queryset = ProcessingMethod.objects.all()
    serializer_class = ProcessingMethodSerializer
# class ProductListViewSet(ModelViewSet):
#     products = Product.objects.all()
#     for product in products:
#         roasting_method = RoastingMethod.objects.get(roasting_method_id == product.roasting_method)
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer