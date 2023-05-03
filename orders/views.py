from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from clients.models import Cart, Client
from clients.serializer import CartSerializer
from config import settings

from orders.models import DeliveryMethod, Order, Status
from orders.serializer import DeliveryMethodSerializer, OrderSerializer, StatusSerializer
import datetime
from django.db import transaction
from django.utils import dateformat

from products.models import Product

# Форматирование даты
class DeliveryMethodViewSet(ModelViewSet):
    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodSerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderView(APIView):
    def get(self, request, id):
        carts = Cart.objects.filter(client=id, active=False)
        # orders = Order.objects.all()
        data_orders = []
        orders = []
        unique = []

        for item in carts:
            serializer_cart = CartSerializer(item)
            get_order = Order.objects.get(order_id=serializer_cart.data['order'])
            serializer_order = OrderSerializer(get_order)
            data_orders.append(serializer_order.data)

        for item in data_orders:
            if item not in unique:
                unique.append(item)

        for item in unique:
            # carts = Cart.objects.filter(client=id, active=False, order=item['order_id'])
            # serializer_cart = CartSerializer(carts)
            order = Order.objects.get(order_id=item['order_id'])
            serializer_order = OrderSerializer(order)

            order_date = dateformat.format(order.order_date, settings.DATE_FORMAT)
            delivery_date = dateformat.format(order.delivery_date, settings.DATE_FORMAT)

            status = Status.objects.get(status_id=serializer_order.data['status'])
            serializer_status = StatusSerializer(status)

            orders.append({'status': serializer_status.data, 'order': serializer_order.data, 'order_date': order_date[1::], 'delivery_date': delivery_date[1::]})

        return Response(orders)

    parser_classes = (MultiPartParser,FormParser,JSONParser)
    def post(self, request):
        if request.method == 'POST':
            data = {'delivery': request.data['delivery'], 'order_sum': request.data['order_sum'], 'status': 2,
                    'order_date': datetime.datetime.now(), 'delivery_date': datetime.datetime.now(), 'dispatch_date': None,
                    'package': request.data['package'], 'address': request.data['address']
            }

            serializer_class = OrderSerializer(data=data)
            print(serializer_class.is_valid())
            if serializer_class.is_valid():
                with transaction.atomic():
                    order = Order.objects.create(
                    delivery = serializer_class.validated_data['delivery'],
                    order_sum = serializer_class.validated_data['order_sum'],
                    status = serializer_class.validated_data['status'],
                    order_date = serializer_class.validated_data['order_date'],
                    delivery_date = serializer_class.validated_data['delivery_date'],
                    dispatch_date = serializer_class.validated_data['dispatch_date'],
                    package = serializer_class.validated_data['package'],
                    address = serializer_class.validated_data['address']
                    )
                    for item in request.data['cart']:
                        Cart.objects.filter(cart_id=item['cart_id']).update(order=order.order_id, active=False)
                return Response(serializer_class.data)
            return Response(serializer_class.errors)