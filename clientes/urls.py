#from .views import ChangePasswordView

from clientes.api.viewsets import ClienteViewSet
from django.urls import path, include
from rest_framework import routers


router_v1 = routers.DefaultRouter()
router_v1.register(r'clientes', ClienteViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]