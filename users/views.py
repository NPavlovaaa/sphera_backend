import datetime
import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from clients.models import Client, Level
from clients.serializer import ClientSerializer, LevelSerializer

from users.models import User
from users.serializer import UserSerializer

from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework import permissions


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomAuthentication(BaseAuthentication):
    def check_token(self, request):
        auth = JWTAuthentication()
        return auth.authenticate(request)

    def authenticate(self, request):
        user_token = self.check_token(request)
        if user_token is not None:
            user, token = user_token
            return user, token
        else:
            return None


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

            elif user_role == 1:
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
