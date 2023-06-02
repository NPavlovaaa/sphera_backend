import datetime

from django.db import transaction
from django.utils import dateformat
from rest_framework import permissions, status

from clients.models import Cart, Client
from clients.serializer import CartSerializer, ClientSerializer
from config import settings
from orders.models import Order
from orders.serializer import OrderSerializer
from products.models import ProcessingMethod, Product, RoastingMethod, Variety, Weight, WeightSelection, ProductVariety, \
    Category, MakingMethod, ProductMakingMethod, AdminProductChange
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from products.serializer import ProductSerializer, RoastingMethodSerializer, ProcessingMethodSerializer, \
    VarietySerializer, WeightSelectionSerializer, ProductVarietySerializer, CategorySerializer, MakingMethodSerializer, \
    WeightSerializer, AdminProductChangeSerializer
from users.models import User
from users.serializer import UserSerializer
from django.db.models.functions import TruncMonth


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


class ProductWarehouseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = []
        unique = []
        products = Product.objects.all()

        for product in products:
            product_serializer = ProductSerializer(product)
            processing_method = ProcessingMethod.objects.get(
                processing_method_id=product_serializer.data['processing_method'])
            processing_serializer = ProcessingMethodSerializer(processing_method)
            roasting_method = RoastingMethod.objects.get(
                roasting_method_id=product_serializer.data['roasting_method'])
            roasting_serializer = RoastingMethodSerializer(roasting_method)
            weight_selection = WeightSelection.objects.filter(product=product.product_id)
            weight_1000_serializer = WeightSelectionSerializer(weight_selection[1])
            weight_250_serializer = WeightSelectionSerializer(weight_selection[0])
            date = dateformat.format(product.date_added, settings.DATE_FORMAT)
            data.append({'product_id': product_serializer.data['product_id'],
                         'image': product_serializer.data['image_min'],
                         'date': date,
                         'product_name': product_serializer.data['product_name'],
                         'processing_method': processing_serializer.data['processing_method_name'],
                         'roasting_method': roasting_serializer.data['roasting_method_name'],
                         'quantity': product_serializer.data['quantity'],
                         'price_250': weight_250_serializer.data['price'],
                         'price_1000': weight_1000_serializer.data['price']})

        for item in data:
            if item not in unique:
                unique.append(item)

        return Response(unique)


class ProductConsumptionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, name):
        data = []
        unique = []
        data_orders = []
        product = Product.objects.get(product_name=name)
        product_serializer = ProductSerializer(product)

        processing_method = ProcessingMethod.objects.get(
            processing_method_id=product_serializer.data['processing_method'])
        processing_serializer = ProcessingMethodSerializer(processing_method)
        roasting_method = RoastingMethod.objects.get(roasting_method_id=product_serializer.data['roasting_method'])
        roasting_serializer = RoastingMethodSerializer(roasting_method)

        carts = Cart.objects.filter(product=product.product_id, active=False)

        for item in carts:
            serializer_cart = CartSerializer(item)

            get_order = Order.objects.get(order_id=serializer_cart.data['order'])
            serializer_order = OrderSerializer(get_order)
            data_orders.append(serializer_order.data)

        for item in data_orders:
            if item not in unique:
                unique.append(item)

        for item in unique:
            cart = Cart.objects.filter(order=item['order_id'], active=False).first()
            serializer_cart = CartSerializer(cart)

            weight_selection = WeightSelection.objects.get(weight_selection_id=serializer_cart.data['weight_selection'])
            weight_selection_serializer = WeightSelectionSerializer(weight_selection)
            weight = Weight.objects.get(weight_id=weight_selection.weight.weight_id)
            weight_serializer = WeightSerializer(weight)

            client = Client.objects.get(client_id=serializer_cart.data['client'])
            order = Order.objects.get(order_id=item['order_id'])
            order_date = dateformat.format(order.order_date, settings.DATE_FORMAT)

            user = User.objects.get(user_id=client.user.user_id)
            serializer_user = UserSerializer(user)

            data.append(
                {'product_count': serializer_cart.data['product_count'], 'date': order_date,
                 'username': serializer_user.data['username'], 'price': weight_selection_serializer.data['price'],
                 'weight': weight_serializer.data['weight'], 'action': 'Consumption',
                 'processing_method': processing_serializer.data['processing_method_name'],
                 'roasting_method': roasting_serializer.data['roasting_method_name'],
                })

        admin_changes = AdminProductChange.objects.filter(product_id=product.product_id)

        for item in admin_changes:
            serializer_class = AdminProductChangeSerializer(item)
            date = dateformat.format(item.date, settings.DATE_FORMAT)
            data.append(
                {'product_count': serializer_class.data['count'], 'date': date,
                 'username': 'Администратор', 'price': serializer_class.data['price'],
                 'processing_method': processing_serializer.data['processing_method_name'],
                 'action': serializer_class.data['action']})
        return Response({'data': data, 'quantity': product_serializer.data['quantity']})


class AdminProductChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.get(user_id=self.request.user.user_id)
        product = Product.objects.get(product_name=request.data['product']['product_name'])
        if user:
            data = {
                'product': product.product_id,
                'count': request.data['count'],
                'action': request.data['action'],
                'price': request.data['price'],
                'user': user.user_id,
                'date': datetime.datetime.now().date()
            }
            serializer_class = AdminProductChangeSerializer(data=data)
            if serializer_class.is_valid():
                with transaction.atomic():
                    AdminProductChange.objects.create(
                        product=serializer_class.validated_data['product'],
                        count=serializer_class.validated_data['count'],
                        action=serializer_class.validated_data['action'],
                        user=serializer_class.validated_data['user'],
                        date=serializer_class.validated_data['date'],
                        price=serializer_class.validated_data['price'],
                    )
                    if request.data['action'] == 'Consumption':
                        product_quantity = Product.objects.get(product_id=product.product_id).quantity - float(request.data['count'])
                    else:
                        product_quantity = Product.objects.get(product_id=product.product_id).quantity + float(request.data['count'])

                    Product.objects.filter(product_id=product.product_id).update(quantity=product_quantity)

                    return Response({'data': serializer_class.data, 'status': status.HTTP_200_OK})
            return Response({'data': serializer_class.data, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})


class ProductCountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = []
        i = 1
        while i < 13:
            orders = Order.objects.filter(order_date__month=i)
            order_weight = 0
            for order in orders:
                carts = Cart.objects.filter(order=order.order_id)
                for cart in carts:
                    weight_selection = WeightSelection.objects.get(weight_selection_id=cart.weight_selection.weight_selection_id)
                    weight = Weight.objects.get(weight_id=weight_selection.weight.weight_id)
                    order_weight += weight.weight * cart.product_count
            data.append(order_weight/1000)
            i += 1

        # serializer = OrderSerializer(orders, many=True)
        return Response(data)


