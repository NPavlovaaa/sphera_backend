import datetime
import jwt
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.viewsets import ModelViewSet

from clients.models import Client, Level
from clients.serializer import ClientSerializer, LevelSerializer

from users.models import User
from users.serializer import UserSerializer

from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.db import transaction
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.contrib.auth import authenticate


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUserAndClientModelView(CreateAPIView):
    parser_classes = (MultiPartParser, FormParser, JSONParser)

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

    def post(self, request):
        user = None
        if request.data['token']:
            print(1)
            token = request.data['token']
            try:
                payload = jwt.decode(token, key="secret", algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Вы не авторизованы!')

            user = User.objects.filter(user_id=payload['id']).first()

        elif request.data['username'] and request.data['password']:
            print(2)
            if request.data['username'] and request.data['password']:
                username = request.data['username']
                passw = request.data['password']

                username_check = User.objects.filter(username=username).first()

                if check_password(passw, username_check.password):
                    user = username_check

                payload = {
                    'id': user.user_id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180),
                    'iat': datetime.datetime.utcnow()
                }

                token = jwt.encode(payload, key="secret", algorithm='HS256')

        elif request.data['token'] == None:
            print(3)
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Вы не авторизованы!!')

            try:
                payload = jwt.decode(token, key="secret", algorithms=['HS256'])

            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Вы не авторизованы!')

            user = User.objects.filter(user_id=payload['id']).first()

        if user is None:
            raise AuthenticationFailed('User not found!')
        else:
            serializer_user = UserSerializer(user)

            if serializer_user.data['role'] == 2:
                client = Client.objects.get(user=user.user_id)
                serializer_client = ClientSerializer(client)
                level = Level.objects.get(level_id=serializer_client.data['level'])
                serializer_level = LevelSerializer(level)
                data = {'user': serializer_user.data, 'client': serializer_client.data, 'level': serializer_level.data,
                        'jwt': token}
            else:
                data = {'user': serializer_user.data, 'jwt': token}
            response = Response()
            response.set_cookie(key='jwt', value=token, httponly=True)
            response.data = data

            return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
