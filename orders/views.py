from django.shortcuts import render
import jwt
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from clients.models import Cart, Client
from clients.serializer import CartSerializer, ClientSerializer
from config import settings

from orders.models import DeliveryMethod, Order, Status
from orders.serializer import DeliveryMethodSerializer, OrderSerializer, StatusSerializer
import datetime
from django.db import transaction
from django.utils import dateformat

from rest_framework.exceptions import AuthenticationFailed
from users.models import User


class DeliveryMethodViewSet(ModelViewSet):
    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodSerializer



class OrderViewSet(ModelViewSet):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class OrderView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user_role = User.objects.get(user_id=self.request.user.user_id).role.role_id
        carts = []

        if user_role == 2:
            client = Client.objects.get(user_id=self.request.user.user_id)
            carts = Cart.objects.filter(client=client.client_id, active=False)

        elif user_role == 1:
            carts = Cart.objects.filter(active=False)

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
            order = Order.objects.get(order_id=item['order_id'])
            serializer_order = OrderSerializer(order)

            order_date = dateformat.format(order.order_date, settings.DATE_FORMAT)
            delivery_date = dateformat.format(order.delivery_date, settings.DATE_FORMAT)

            status = Status.objects.get(status_id=serializer_order.data['status'])
            serializer_status = StatusSerializer(status)

            client = Client.objects.get(client_id=serializer_cart.data['client'])
            serializer_client = ClientSerializer(client)

            orders.append(
                {'status': serializer_status.data, 'order': serializer_order.data, 'order_date': order_date,
                 'delivery_date': delivery_date, 'client': serializer_client.data})

        return Response(orders)

    def post(self, request):
        if request.method == 'POST':
            data = {'delivery': 1, 'order_sum': request.data['order_sum'], 'status': 2,
                    'order_date': datetime.datetime.now(), 'delivery_date': datetime.datetime.now().date(),
                    'dispatch_date': None,
                    'package': request.data['package'], 'address': request.data['address']
                    }

            serializer_class = OrderSerializer(data=data)
            if serializer_class.is_valid():
                with transaction.atomic():
                    order = Order.objects.create(
                        delivery=serializer_class.validated_data['delivery'],
                        order_sum=serializer_class.validated_data['order_sum'],
                        status=serializer_class.validated_data['status'],
                        order_date=serializer_class.validated_data['order_date'],
                        delivery_date=serializer_class.validated_data['delivery_date'],
                        dispatch_date=serializer_class.validated_data['dispatch_date'],
                        package=serializer_class.validated_data['package'],
                        address=serializer_class.validated_data['address']
                    )
                    client = Client.objects.get(user_id=self.request.user.user_id)
                    Cart.objects.filter(client_id=client.client_id, active=True).update(order=order.order_id, active=False)

                return Response(serializer_class.data)
            return Response(serializer_class.errors)
