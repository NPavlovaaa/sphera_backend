import datetime

from django.db import transaction
from django.utils import dateformat
from rest_framework import permissions, status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from clients.models import Client, Level
from clients.serializer import ClientSerializer, LevelSerializer
from config import settings
from reviews.models import Review, ReviewStatus, ReviewsProduct
from reviews.serializer import OrderReviewsSerializer, ReviewStatusSerializer, ProductReviewsSerializer
from users.models import User
from users.serializer import UserSerializer


class OrdersReviewListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = []
        user_role = User.objects.get(user_id=self.request.user.user_id).role.role_id

        if user_role == 2:
            queryset = Review.objects.filter(review_status=2)

        elif user_role == 1:
            queryset = Review.objects.all()

        for item in queryset:
            review_date = dateformat.format(item.review_date, settings.DATE_FORMAT)
            serializer_class = OrderReviewsSerializer(item)
            client = Client.objects.get(client_id=serializer_class.data['client'])
            client_serializer = ClientSerializer(client)
            user = User.objects.get(user_id=client_serializer.data['user'])
            user_serializer = UserSerializer(user)
            level = Level.objects.get(level_id=client_serializer.data['level'])
            level_serializer = LevelSerializer(level)
            review_status = ReviewStatus.objects.get(review_status_id=serializer_class.data['review_status'])
            review_status_serializer = ReviewStatusSerializer(review_status)

            data.append(
                {'review_date': review_date, 'review': serializer_class.data, 'avatar': user_serializer.data['avatar'],
                 'first_name': client_serializer.data['first_name'], 'level': level_serializer.data['level_name'],
                 'review_status': review_status_serializer.data['review_status_name']
                 })

        return Response(data)


class ProductsReviewListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = []
        user_role = User.objects.get(user_id=self.request.user.user_id).role.role_id

        if user_role == 2:
            queryset = ReviewsProduct.objects.filter(review_status=2)

        elif user_role == 1:
            queryset = ReviewsProduct.objects.all()

        for item in queryset:
            review_date = dateformat.format(item.review_date, settings.DATE_FORMAT)
            serializer_class = ProductReviewsSerializer(item)
            client = Client.objects.get(client_id=serializer_class.data['client'])
            client_serializer = ClientSerializer(client)
            user = User.objects.get(user_id=client_serializer.data['user'])
            user_serializer = UserSerializer(user)
            level = Level.objects.get(level_id=client_serializer.data['level'])
            level_serializer = LevelSerializer(level)
            review_status = ReviewStatus.objects.get(review_status_id=serializer_class.data['review_status'])
            review_status_serializer = ReviewStatusSerializer(review_status)

            data.append(
                {'review_date': review_date, 'review': serializer_class.data, 'avatar': user_serializer.data['avatar'],
                 'first_name': client_serializer.data['first_name'], 'level': level_serializer.data['level_name'],
                 'review_status': review_status_serializer.data['review_status_name']
                 })

        return Response(data)


class ProductsReviewUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_role = User.objects.get(user_id=self.request.user.user_id).role.role_id
        if user_role == 1:
            if request.data['detail'] == 'publish':
                review = ReviewsProduct.objects.filter(review_id=request.data['review_id']).update(review_status=2)
            elif request.data['detail'] == 'cancel':
                review = ReviewsProduct.objects.filter(review_id=request.data['review_id']).update(review_status=3)
            if review:
                return Response({'status': status.HTTP_200_OK})
        return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR})


class OrdersReviewUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user_role = User.objects.get(user_id=self.request.user.user_id).role.role_id
        if user_role == 1:
            if request.data['detail'] == 'publish':
                review = Review.objects.filter(review_id=request.data['review_id']).update(review_status=2)
            elif request.data['detail'] == 'cancel':
                review = Review.objects.filter(review_id=request.data['review_id']).update(review_status=3)
            if review:
                return Response({'status': status.HTTP_200_OK})
        return Response({'status': status.HTTP_500_INTERNAL_SERVER_ERROR})


class OrdersReviewCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.get(user_id=self.request.user.user_id)
        client = Client.objects.get(user=user.user_id)
        client_serializer = ClientSerializer(client)
        if request.method == 'POST':
            data = {'review_text': request.data['review_text'],
                    'order': request.data['order'],
                    'client': client_serializer.data['client_id'],
                    'review_date': datetime.datetime.now(),
                    'delivery_assessment': request.data['delivery_assessment'],
                    'product_quality_assessment': request.data['product_quality_assessment'],
                    'review_status': 1
                    }
            serializer_class = OrderReviewsSerializer(data=data)
            if serializer_class.is_valid():
                with transaction.atomic():
                    Review.objects.create(
                        review_text=serializer_class.validated_data['review_text'],
                        client=serializer_class.validated_data['client'],
                        order=serializer_class.validated_data['order'],
                        review_date=serializer_class.validated_data['review_date'],
                        delivery_assessment=serializer_class.validated_data['delivery_assessment'],
                        product_quality_assessment=serializer_class.validated_data['product_quality_assessment'],
                        review_status=serializer_class.validated_data['review_status']
                    )
                return Response(serializer_class.data)
            return Response(serializer_class.errors)


class ProductsReviewCreateView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.get(user_id=self.request.user.user_id)
        client = Client.objects.get(user=user.user_id)
        client_serializer = ClientSerializer(client)
        if request.method == 'POST':
            data = {'review_text': request.data['review_text'],
                    'product': request.data['product'],
                    'client': client_serializer.data['client_id'],
                    'review_date': datetime.datetime.now(),
                    'product_quality_assessment': request.data['product_quality_assessment'],
                    'review_status': 1
                    }
            serializer_class = ProductReviewsSerializer(data=data)
            if serializer_class.is_valid():
                with transaction.atomic():
                    ReviewsProduct.objects.create(
                        review_text=serializer_class.validated_data['review_text'],
                        client=serializer_class.validated_data['client'],
                        product=serializer_class.validated_data['product'],
                        review_date=serializer_class.validated_data['review_date'],
                        product_quality_assessment=serializer_class.validated_data['product_quality_assessment'],
                        review_status=serializer_class.validated_data['review_status']
                    )
                return Response(serializer_class.data)
            return Response(serializer_class.errors)