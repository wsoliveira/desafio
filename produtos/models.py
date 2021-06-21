from django.db import models
from django.utils.translation import gettext_lazy as _
from clientes.models import Cliente

# Create your models here.
class Produto(models.Model):
    produto_id = models.CharField(_('product_id'), max_length=50, unique=True)

    class Meta:
        app_label = 'produtos'
        verbose_name = 'produto'
        verbose_name_plural = 'produtos'

              
class Favorito(models.Model):
    cliente = models.OneToOneField(Cliente, on_delete=models.CASCADE)
    produtos = models.ManyToManyField(Produto, related_name='produtos')

    def __str__(self):
        return self.cliente.nome

    class Meta:
        app_label = 'produtos'
        verbose_name = 'favorito'
        verbose_name_plural = 'favoritos'