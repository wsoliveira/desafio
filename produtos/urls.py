#from .views import ChangePasswordView
from produtos.api.viewsets import FavoritoViewSet
from django.urls import path, include
from rest_framework import routers


router_v1 = routers.DefaultRouter()
router_v1.register(r'favoritos', FavoritoViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]