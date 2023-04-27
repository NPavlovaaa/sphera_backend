from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from orders.models import DeliveryMethod
from orders.serializer import DeliveryMethodSerializer


class DeliveryMethodViewSet(ModelViewSet):
    queryset = DeliveryMethod.objects.all()
    serializer_class = DeliveryMethodSerializer