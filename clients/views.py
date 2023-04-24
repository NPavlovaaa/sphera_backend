import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from clients.models import Client, Cart
from clients.serializer import ClientSerializer, CartSerializer
from django.db import transaction
from rest_framework import status

from products.models import ProcessingMethod, Product, RoastingMethod, Weight, WeightSelection
from products.serializer import ProcessingMethodSerializer, ProductSerializer, RoastingMethodSerializer, WeightSelectionSerializer, WeightSerializer

class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        payload = jwt.decode(token, key="secret", algorithms=['HS256'])
        client = Client.objects.filter(user=payload['id']).first()
        serializer_class = ClientSerializer(client)

        return Response(serializer_class.data)

class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartView(APIView):
    def get(self, request, id):
        data = Cart.objects.filter(client=id)
        carts = []
        for item in data:
            cart_serializer = CartSerializer(item)
            product = Product.objects.get(product_id=cart_serializer.data['product'])
            product_serializer = ProductSerializer(product)

            weight_selection =  WeightSelection.objects.get(weight_selection_id=cart_serializer.data['weight_selection'])
            weight_selection_serializer = WeightSelectionSerializer(weight_selection)

            weight = Weight.objects.get(weight_id=weight_selection_serializer.data['weight'])
            weight_serializer = WeightSerializer(weight)

            roasting = RoastingMethod.objects.get(roasting_method_id=product_serializer.data['roasting_method'])
            roasting_serializer = RoastingMethodSerializer(roasting)

            processing = ProcessingMethod.objects.get(processing_method_id=product_serializer.data['processing_method'])
            processing_serializer = ProcessingMethodSerializer(processing)


            carts.append({'cart_id': cart_serializer.data['cart_id'], 'product': product_serializer.data, 'count': cart_serializer.data['product_count'],
                          'weight': weight_serializer.data['weight'], 'price': weight_selection_serializer.data['price'] * cart_serializer.data['product_count'],
                          'roasting': roasting_serializer.data['roasting_method_name'], 'processing': processing_serializer.data['processing_method_name'],
                          'weight_selection': weight_selection_serializer.data['weight_selection_id']})
        return Response(carts)

    def post(self, request, **kwargs):
        if request.method == 'POST':
            cart_serializer = CartSerializer(data=request.data)
            if cart_serializer.is_valid():
                with transaction.atomic():
                    cart = Cart.objects.create(
                        client = cart_serializer.validated_data['client'],
                        weight_selection = cart_serializer.validated_data['weight_selection'],
                        product_count = 1,
                        product =  WeightSelection.objects.get(weight_selection_id=cart_serializer.validated_data['weight_selection'].weight_selection_id).product
                        )
                    cart.save()
                    return Response(cart_serializer.data, status=status.HTTP_201_CREATED)
            return Response(cart_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductInCartView(APIView):
    def get(self, request, product, client, weight_selection):
        cart = Cart.objects.get(client=client, product=product, weight_selection=weight_selection)
        cart_serializer = CartSerializer(cart)
        if cart_serializer.data:
            return Response(cart_serializer.data)
        else:
            return Response(cart_serializer.errors)

