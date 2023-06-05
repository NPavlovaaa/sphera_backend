import datetime
import jwt
from django.utils import dateformat
from rest_framework.authentication import BaseAuthentication
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.viewsets import ModelViewSet

from clients.models import Client, Level
from clients.serializer import ClientSerializer, LevelSerializer
from config import settings

from users.models import User, AdminIncomeChange, Role
from users.serializer import UserSerializer, AdminIncomeChangeSerializer, RoleSerializer

from django.contrib.auth.hashers import make_password

from django.db import transaction
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import permissions


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = User.objects.all()
        data = []
        for item in queryset:
            user_serializer = UserSerializer(item)
            date_joined = dateformat.format(item.date_joined, settings.DATE_FORMAT)
            data.append(
                {'username': user_serializer.data['username'],
                 'avatar': user_serializer.data['avatar'],
                 'date_joined': date_joined,
                 'first_name': user_serializer.data['first_name'],
                 'last_name': user_serializer.data['last_name'],
                 'is_active': user_serializer.data['is_active'],
                 }
            )
        return Response(data)



class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class CreateUserAndClientModelView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [permissions.AllowAny]

    def post(self, request, **kwargs):
        if request.method == 'POST':
            user_data = {'user_id': request.data['user_id'],
                         'password': request.data['password'],
                         'username': request.data['username'],
                         'avatar': request.FILES.get('avatar'),
                         'role': 2
                         }
            client_data = {'first_name': request.data['first_name'], 'last_name': request.data['last_name'],
                           'phone': request.data['phone'],
                           'birthday': request.data['birthday'], 'level': 1, 'scores': 0,
                           'user': request.data['user_id']
                           }
            user_serializer = UserSerializer(data=user_data)
            if user_serializer.is_valid():
                with transaction.atomic():
                    User.objects.create(
                        user_id=user_serializer.validated_data['user_id'],
                        password=make_password(user_serializer.validated_data['password']),
                        username=user_serializer.validated_data['username'],
                        avatar=user_serializer.validated_data['avatar'],
                        role=user_serializer.validated_data['role']
                    )
                    client_serializer = ClientSerializer(data=client_data)
                    if client_serializer.is_valid():
                        Client.objects.create(
                            first_name=client_serializer.validated_data['first_name'],
                            last_name=client_serializer.validated_data['last_name'],
                            phone=client_serializer.validated_data['phone'],
                            birthday=client_serializer.validated_data['birthday'],
                            level=client_serializer.validated_data['level'],
                            scores=client_serializer.validated_data['scores'],
                            user=client_serializer.validated_data['user']
                        )
                        return Response(client_serializer.data, status=status.HTTP_201_CREATED)
                    return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        try:
            user = User.objects.get(user_id=self.request.user.user_id)
            user_serializer = UserSerializer(user)
            user_role = user_serializer.data['role']

            if user_role == 2:
                client = Client.objects.get(user=user_serializer.data['user_id'])
                serializer_client = ClientSerializer(client)
                level = Level.objects.get(level_id=serializer_client.data['level'])
                serializer_level = LevelSerializer(level)
                data = {'user': user_serializer.data, 'client': serializer_client.data, 'level': serializer_level.data}

            else:
                data = {'user': user_serializer.data}

            return Response(data)

        except:
            raise AuthenticationFailed('User not found!')


class LogoutView(APIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class CustomerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data =[]
        clients = Client.objects.all()
        for item in clients:
            serializer_client = ClientSerializer(item)
            user = User.objects.get(user_id=item.user.user_id)
            user_serializer = UserSerializer(user)
            date_joined = dateformat.format(user.date_joined, settings.DATE_FORMAT)
            level = Level.objects.get(level_id=serializer_client.data['level'])
            serializer_level = LevelSerializer(level)
            data.append(
                {'username': user_serializer.data['username'],
                 'id': serializer_client.data['client_id'],
                 'avatar': user_serializer.data['avatar'],
                 'date_joined': date_joined,
                 'first_name': serializer_client.data['first_name'],
                 'last_name': serializer_client.data['last_name'],
                 'phone': serializer_client.data['phone'],
                 'level': serializer_level.data['level_name'],
                 'scores': serializer_client.data['scores'],
                 'address': serializer_client.data['address'],
                 }
            )
        return Response(data)


class AdminIncomeChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = User.objects.get(user_id=self.request.user.user_id)
        if user:
            data = {
                'note': request.data['note'],
                'action': request.data['action'],
                'price': request.data['price'],
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

                    return Response({'data': serializer_class.data, 'status': status.HTTP_200_OK})
            return Response({'data': serializer_class.data, 'status': status.HTTP_500_INTERNAL_SERVER_ERROR})