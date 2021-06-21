from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Cliente(models.Model):
    nome = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email address'), unique=True)

    def __str__(self):
        return self.email

    class Meta:
        app_label = 'clientes'
        verbose_name = "cliente"
        verbose_name_plural = "clientes"
        ordering = ['nome']
              