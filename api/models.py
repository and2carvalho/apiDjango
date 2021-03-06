from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManager(BaseUserManager):
    
    def _create_user(self, name, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not name:
            raise ValueError('Obrigatório inserir nome do usuário.')
        email = self.normalize_email(email)
        user = self.model(name=name, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, email=None, password=None, **extra_fields):
        return self._create_user(name, email, password, False, False, **extra_fields)    
    
    def create_superuser(self, name, email, password, **extra_fields):
        user=self._create_user(name, email, password, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    
    name = models.CharField('Nome', max_length=30)
    email = models.EmailField('Email', unique=True)
    date_joined = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    is_active = models.BooleanField('active', default=True)
    is_staff = models.BooleanField('staff status', default=False)
    is_trusty = models.BooleanField('trusty', default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def email_user(self, subject, message, from_email=None, **kwargs):

        send_mail(subject, message, from_email, [self.email], **kwargs)

class Fazenda(models.Model):

    name = models.CharField('Name', max_length=60)
    owner = models.CharField('Owner', max_length=60)
    cpf = models.CharField('CPF', max_length=14, unique=True)
    stations = models.IntegerField('Stations')
    created = models.DateTimeField('Criado em', auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)

    def __str__(self):
        return self.name

class Station(models.Model):

    name = models.CharField('Name', max_length=60)
    latitude = models.DecimalField('Latitude', max_digits=9, decimal_places=6, unique=True)
    longitude = models.DecimalField('Longitude', max_digits=9, decimal_places=6, unique=True)
    created = models.DateTimeField('Criado em', auto_now=False, auto_now_add=True)
    modified = models.DateTimeField('Modificado em', auto_now=True)
    fazenda = models.ForeignKey(Fazenda, null=True, blank=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

