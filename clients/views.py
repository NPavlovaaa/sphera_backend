import jwt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from clients.models import Client
from clients.serializer import ClientSerializer


class ClientViewSet(ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        payload = jwt.decode(token, key="secret", algorithms=['HS256'])
        client = Client.objects.filter(user=payload['id']).first()
        serializer_class = ClientSerializer(client)

        return Response(serializer_class.data)
