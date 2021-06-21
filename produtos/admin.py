from django.contrib import admin
from .models import Produto, Favorito

# Register your models here.
admin.site.register([Produto, Favorito])
