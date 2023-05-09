import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from clients.models import Client, Cart, Favorite
from clients.serializer import ClientSerializer, CartSerializer, FavoriteSerializer
from django.db import transaction
from rest_framework import status

from products.models import ProcessingMethod, Product, RoastingMethod, Weight, WeightSelection
from products.serializer import ProcessingMethodSerializer, ProductSerializer, RoastingMethodSerializer, \
    WeightSelectionSerializer, WeightSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import permissions


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class CartView(APIView):
    """ Список подкорзин клиента и их добавление
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        client = Client.objects.get(user=self.request.user.user_id)
        queryset = Cart.objects.filter(client=client.client_id, active=True)
        carts = []

        for item in queryset:
            cart_serializer = CartSerializer(item)
            product = Product.objects.get(product_id=cart_serializer.data['product'])
            product_serializer = ProductSerializer(product)

            weight_selection = WeightSelection.objects.get(weight_selection_id=cart_serializer.data['weight_selection'])
            weight_selection_serializer = WeightSelectionSerializer(weight_selection)

            weight = Weight.objects.get(weight_id=weight_selection_serializer.data['weight'])
            weight_serializer = WeightSerializer(weight)

            roasting = RoastingMethod.objects.get(roasting_method_id=product_serializer.data['roasting_method'])
            roasting_serializer = RoastingMethodSerializer(roasting)

            processing = ProcessingMethod.objects.get(processing_method_id=product_serializer.data['processing_method'])
            processing_serializer = ProcessingMethodSerializer(processing)

            carts.append({'cart_id': cart_serializer.data['cart_id'], 'product': product_serializer.data,
                          'count': cart_serializer.data['product_count'],
                          'weight': weight_serializer.data['weight'],
                          'price': weight_selection_serializer.data['price'] * cart_serializer.data['product_count'],
                          'roasting': roasting_serializer.data['roasting_method_name'],
                          'processing': processing_serializer.data['processing_method_name'],
                          'weight_selection': weight_selection_serializer.data['weight_selection_id'],
                          'order': cart_serializer.data['order']})
        return Response(carts)

    def post(self, request, **kwargs):
        if request.method == 'POST':
            client = Client.objects.get(user=self.request.user.user_id)
            cart_data = {'weight_selection': request.data['weight_selection'], 'client': client.client_id}
            serializer_cart = CartSerializer(data=cart_data)
            if serializer_cart.is_valid():
                
                with transaction.atomic():
                    Cart.objects.create(
                        client=client,
                        weight_selection=serializer_cart.validated_data['weight_selection'],
                        product_count=1,
                        product=WeightSelection.objects.get(weight_selection_id=serializer_cart.validated_data[
                            'weight_selection'].weight_selection_id).product,
                        active=True
                    )
                    return Response(serializer_cart.data, status=status.HTTP_201_CREATED)
            return Response(serializer_cart.errors, status=status.HTTP_400_BAD_REQUEST)

class CartOrdersView(APIView):
    """ Список подкорзин клиента в заказе
    """
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        client = Client.objects.get(user=self.request.user.user_id)
        queryset = Cart.objects.filter(client=client.client_id, active=False)
        carts = []

        for item in queryset:
            cart_serializer = CartSerializer(item)
            product = Product.objects.get(product_id=cart_serializer.data['product'])
            product_serializer = ProductSerializer(product)

            weight_selection = WeightSelection.objects.get(weight_selection_id=cart_serializer.data['weight_selection'])
            weight_selection_serializer = WeightSelectionSerializer(weight_selection)

            weight = Weight.objects.get(weight_id=weight_selection_serializer.data['weight'])
            weight_serializer = WeightSerializer(weight)

            roasting = RoastingMethod.objects.get(roasting_method_id=product_serializer.data['roasting_method'])
            roasting_serializer = RoastingMethodSerializer(roasting)

            processing = ProcessingMethod.objects.get(processing_method_id=product_serializer.data['processing_method'])
            processing_serializer = ProcessingMethodSerializer(processing)

            carts.append({'cart_id': cart_serializer.data['cart_id'], 'product': product_serializer.data,
                          'count': cart_serializer.data['product_count'],
                          'weight': weight_serializer.data['weight'],
                          'price': weight_selection_serializer.data['price'] * cart_serializer.data['product_count'],
                          'roasting': roasting_serializer.data['roasting_method_name'],
                          'processing': processing_serializer.data['processing_method_name'],
                          'weight_selection': weight_selection_serializer.data['weight_selection_id'],
                          'order': cart_serializer.data['order']})
        return Response(carts)

class CartViewSet(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class ProductInCartView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, product, weight_selection):
        client = Client.objects.get(user=self.request.user.user_id)
        try:
            cart = Cart.objects.get(client=client, product=product, weight_selection=weight_selection, active=True)

        except Cart.DoesNotExist:
            pass

        if cart:
            cart_serializer = CartSerializer(cart)
        else:
            cart_serializer = None

        return Response(cart_serializer.data)


class FavoriteViewSet(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class FavoriteView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, id):
        favorite = Favorite.objects.filter(client=id)
        favorites = []
        for item in favorite:
            favorite_serializer = FavoriteSerializer(item)
            favorites.append(favorite_serializer.data)
        return Response(favorites)


class CartAdminView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request):
        data = Cart.objects.filter(active=False)

        carts = []
        for item in data:
            cart_serializer = CartSerializer(item)
            product = Product.objects.get(product_id=cart_serializer.data['product'])
            product_serializer = ProductSerializer(product)

            weight_selection = WeightSelection.objects.get(weight_selection_id=cart_serializer.data['weight_selection'])
            weight_selection_serializer = WeightSelectionSerializer(weight_selection)

            weight = Weight.objects.get(weight_id=weight_selection_serializer.data['weight'])
            weight_serializer = WeightSerializer(weight)

            roasting = RoastingMethod.objects.get(roasting_method_id=product_serializer.data['roasting_method'])
            roasting_serializer = RoastingMethodSerializer(roasting)

            processing = ProcessingMethod.objects.get(processing_method_id=product_serializer.data['processing_method'])
            processing_serializer = ProcessingMethodSerializer(processing)

            carts.append({'cart_id': cart_serializer.data['cart_id'], 'product': product_serializer.data,
                          'count': cart_serializer.data['product_count'],
                          'weight': weight_serializer.data['weight'],
                          'price': weight_selection_serializer.data['price'] * cart_serializer.data['product_count'],
                          'roasting': roasting_serializer.data['roasting_method_name'],
                          'processing': processing_serializer.data['processing_method_name'],
                          'weight_selection': weight_selection_serializer.data['weight_selection_id'],
                          'order': cart_serializer.data['order']})
        return Response(carts)
