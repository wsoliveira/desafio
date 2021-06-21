from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from produtos.models import Favorito
from .serializers import FavoritosSerializer


class FavoritoViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (JWTAuthentication,)
    queryset = Favorito.objects.all()
    serializer_class = FavoritosSerializer
    filter_backends = (DjangoFilterBackend,)  # filtragem por expressao
    filter_fields = ('cliente',)
    http_method_names = ['post','get','delete']
