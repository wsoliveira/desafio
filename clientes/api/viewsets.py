from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from clientes.models import Cliente
from .serializers import ClientesSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = Cliente.objects.all()
    serializer_class = ClientesSerializer
    filter_backends = (DjangoFilterBackend,)  # filtragem por expressao
    filter_fields = ('email',)