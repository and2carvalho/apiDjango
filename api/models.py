from django.db import models
from django.contrib.auth.models import User

# criação de campo que aceita apenas uppercase
class NameField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(NameField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        return str(value).capitalize()


class Fazenda(models.Model):

    name = models.CharField('Name', max_length=60)
    owner = models.CharField('Owner', max_length=60)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    stations = models.IntegerField("Stations")
    created = models.DateTimeField('Criado em', auto_now=False, auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.name

class Station(models.Model):

    name = NameField('Name', max_length=60)
    latitude = models.DecimalField('Latitude', max_digits=9, decimal_places=6, unique=True)
    longitude = models.DecimalField('Longitude', max_digits=9, decimal_places=6, unique=True)
    created = models.DateTimeField('Criado em', auto_now=False, auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    fazenda = models.ForeignKey(Fazenda, on_delete=models.CASCADE)

    def __str__(self):
        return self.name