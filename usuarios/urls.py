#from .views import ChangePasswordView
from usuarios.api.viewsets import UsuarioViewSet, UserRegisterViewSet
from django.urls import path, include
from rest_framework import routers


router_v1 = routers.DefaultRouter()
router_v1.register(r'usuarios/registra_usuario', UserRegisterViewSet)
router_v1.register(r'usuarios/dados', UsuarioViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]