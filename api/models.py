from django.db import models
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Fazenda(models.Model):

    name = models.CharField('Name', max_length=60)
    owner = models.CharField('Owner', max_length=60)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    stations = models.IntegerField('Stations')
    created = models.DateTimeField('Criado em', auto_now=False, auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.name

class Station(models.Model):

    name = models.CharField('Name', max_length=60)
    latitude = models.DecimalField('Latitude', max_digits=9, decimal_places=6, unique=True)
    longitude = models.DecimalField('Longitude', max_digits=9, decimal_places=6, unique=True)
    created = models.DateTimeField('Criado em', auto_now=False, auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)