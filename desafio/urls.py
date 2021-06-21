"""desafio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.permissions import IsAdminUser
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt import views as jwt_views
import usuarios.urls as urls_api_acessos
import clientes.urls as urls_api_clientes
import produtos.urls as urls_api_produtos

admin.site.site_header = "DESAFIO admin"
admin.site.site_title = "DESAFIO admin"
admin.site.index_title = "DESAFIO administração"
admin.site.site_url = "http://EmDesenvolvimento.com.br"


urlpatterns = [
    path('api/docs/', include_docs_urls(title='Back-End Desafio - Welligton S. De Oliveira', permission_classes=[IsAdminUser])),
    path('admin/', admin.site.urls),
    path('api/', include(urls_api_acessos)),
    path('api/', include(urls_api_clientes)),
    path('api/', include(urls_api_produtos)),
    path('api/v1/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'), 
    path('api/v1/token/verify/', jwt_views.TokenVerifyView.as_view(), name='token_verify'),

]