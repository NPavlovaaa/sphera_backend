import datetime

from django.db import transaction
from django.utils import dateformat
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from clients.models import Client, Level
from clients.serializer import ClientSerializer, LevelSerializer
from config import settings
from reviews.models import Review
from reviews.serializer import OrderReviewsSerializer
from users.models import User
from users.serializer import UserSerializer


class OrdersReviewListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        data = []
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

            data.append(
                {'review_date': review_date, 'review': serializer_class.data, 'avatar': user_serializer.data['avatar'],
                 'first_name': client_serializer.data['first_name'], 'level': level_serializer.data['level_name']})

        return Response(data)


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
                    'product_quality_assessment': request.data['product_quality_assessment']
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
                    )
                return Response(serializer_class.data)
            return Response(serializer_class.errors)
