from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from usuarios.models import Usuario
from .serializers import UsuarioRegisterSerializer, UsuariosSerializer


class UsuarioViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = Usuario.objects.all()
    serializer_class = UsuariosSerializer
    http_method_names = ['get']
    filter_backends = (DjangoFilterBackend,)  # filtragem por expressao
    filter_fields = ('email',)

class UserRegisterViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = Usuario.objects.all()
    serializer_class = UsuarioRegisterSerializer
    http_method_names = ['post']