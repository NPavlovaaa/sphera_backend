import hashlib

import requests
from django.http import HttpResponse
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.views import APIView
from clients.models import Cart, Client
from clients.serializer import CartSerializer, ClientSerializer
from config import settings
import json
from orders.models import DeliveryMethod, Order, Status
from orders.serializer import DeliveryMethodSerializer, OrderSerializer, StatusSerializer
import datetime
from django.db import transaction
from django.utils import dateformat

from products.models import WeightSelection, Weight, Product, AdminProductChange
from products.serializer import WeightSelectionSerializer, WeightSerializer, AdminProductChangeSerializer
from users.models import User, AdminIncomeChange
from users.serializer import UserSerializer, AdminIncomeChangeSerializer


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
            carts = Cart.objects.filter(client=client.client_id, active=False).order_by("cart_id")

        elif user_role == 1 or user_role == 3:
            carts = Cart.objects.filter(active=False).order_by("cart_id")

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
            user = User.objects.get(user_id=self.request.user.user_id)
            data = {'delivery': 1, 'order_sum': request.data['order_sum'], 'status': 'created',
                    'order_date': datetime.datetime.now(), 'delivery_date': request.data['user_delivery_date'],
                    'dispatch_date': None, 'user_delivery_time': request.data['user_delivery_time'],
                    'package': request.data['package'], 'address': request.data['address'],
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
                        address=serializer_class.validated_data['address'],
                        user_delivery_time=serializer_class.validated_data['user_delivery_time'],
                    )
                    client = Client.objects.get(user_id=self.request.user.user_id)
                    Cart.objects.filter(client_id=client.client_id, active=True).update(order=order.order_id,
                                                                                        active=False)
                    carts = Cart.objects.filter(client_id=client.client_id, order=order.order_id, active=False)
                    for item in carts:
                        weight_selection = WeightSelection.objects.get(
                            weight_selection_id=item.weight_selection.weight_selection_id)
                        weight = Weight.objects.get(weight_id=weight_selection.weight.weight_id)
                        product_quantity = Product.objects.get(product_id=item.product.product_id).quantity
                        if weight.weight == 250:
                            Product.objects.filter(product_id=item.product.product_id).update(
                                quantity=product_quantity - item.product_count * 0.25)
                        elif weight.weight == 1000:
                            Product.objects.filter(product_id=item.product.product_id).update(
                                quantity=product_quantity - item.product_count)

                    data = {
                        'note': 'Заказ',
                        'action': 'Consumption',
                        'price': order.order_sum,
                        'user': user.user_id,
                        'date': datetime.datetime.now().date()
                    }
                    serializer_class = AdminIncomeChangeSerializer(data=data)
                    if serializer_class.is_valid():
                        with transaction.atomic():
                            AdminIncomeChange.objects.create(
                                note=serializer_class.validated_data['note'],
                                action=serializer_class.validated_data['action'],
                                user=serializer_class.validated_data['user'],
                                date=serializer_class.validated_data['date'],
                                price=serializer_class.validated_data['price'],
                            )

                return Response(serializer_class.data)
            return Response(serializer_class.errors)


class DeliveryCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.method == 'POST':
            data = {'type': request.data['type'], 'matter': request.data['matter'],
                    'total_weight_kg': request.data['total_weight_kg'], 'points': request.data['points']}

            url = "https://robotapitest.dostavista.ru/api/business/1.3/create-order"
            res = requests.post(url, json=data, headers={'Content-Type': 'application/json',
                                                         'X-DV-Auth-Token': '80B4D1DFF00828E2749C9048B7617469E6E94844'})
            if res.status_code == 200:
                created_order = res.json()
                Order.objects.filter(order_id=request.data['id']).update(
                    tracking_url=created_order['order']['points'][0]['tracking_url'],
                    delivery_sum=created_order['order']['payment_amount'],
                    delivery_date=created_order['order']['points'][0]['required_start_datetime'],
                    status='available',
                )

                return Response(created_order)
            else:
                return HttpResponse(res)


class PaymentCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        if request.method == 'POST':
            token = "v2be6s3p4sa9d8yt" + request.data["PaymentId"] + "1685608375285DEMO"
            tokensha256 = str(hashlib.sha256(token.encode()).hexdigest())

            checkopl = {
                "TerminalKey": "1685608375285DEMO",
                "PaymentId": request.data["PaymentId"],
                "Token": tokensha256
            }

            res = requests.post("https://securepay.tinkoff.ru/v2/GetState", json=checkopl)
            print(res.content)

            if res.status_code == 200:
                created_order = res.json()
                return Response(created_order)
            else:
                return HttpResponse(res)


class IncomeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = []
        data_orders = Order.objects.filter(status=2)

        for item in data_orders:
            serializer_order = OrderSerializer(item)
            order_date = dateformat.format(item.order_date, settings.DATE_FORMAT)
            cart = Cart.objects.filter(order=item.order_id).first()
            client = Client.objects.get(client_id=cart.client.client_id)
            user = User.objects.get(user_id=client.user.user_id)
            user_serializer = UserSerializer(user)

            orders.append(
                {'order': serializer_order.data['order_id'], 'date': order_date,
                 'username': user_serializer.data['username'],
                 'price': serializer_order.data['order_sum'], 'action': 'Consumption'})

        admin_changes = AdminProductChange.objects.all()
        incomes_changes = AdminIncomeChange.objects.all()

        for item in admin_changes:
            serializer_class = AdminProductChangeSerializer(item)
            date = dateformat.format(item.date, settings.DATE_FORMAT)
            orders.append(
                {'date': date, 'action': serializer_class.data['action'],
                 'username': 'Администратор', 'price': serializer_class.data['price']})
        for item in incomes_changes:
            serializer_class = AdminIncomeChangeSerializer(item)
            date = dateformat.format(item.date, settings.DATE_FORMAT)
            orders.append(
                {'date': date, 'action': serializer_class.data['action'],
                 'username': 'Администратор', 'price': serializer_class.data['price'],
                 'note': serializer_class.data['note']})

        return Response(orders)
