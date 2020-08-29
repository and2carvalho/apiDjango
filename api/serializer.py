from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Fazenda, Station
from django.core.mail import send_mail
from django.conf import settings
import re

User = get_user_model()

class LoginSerializer(JSONWebTokenSerializer):
    
    message = 'Usuário e/ou senha inválidos'

    def validate(self, attrs):
        try:
            user = User.objects.filter(email=attrs['email'])[0]
        except:
            raise serializers.ValidationError(self.message, code='email')
        if not user.check_password(attrs['password']):
            raise serializers.ValidationError(self.message, code='email')
        return super(LoginSerializer,self).validate(attrs)


class RegistrationSerializer(serializers.ModelSerializer):

    confirm_password = serializers.CharField(write_only=True,style={'input_type':'password'})

    class Meta:
        model = User
        fields = ['pk', 'name','email', 'password', 'confirm_password', 'date_joined', 'modified']
        extra_kwargs = {'password':{'write_only':True,'style': {'input_type':'password'}},
                        'pk':{'read_only':True},
                        'date_joined':{'read_only':True},
                        'modified':{'read_only':True}
                        }

    def validate(self, data):

        if User.objects.filter(email=data['email']):
            raise serializers.ValidationError({'error':'E-mail já existente'})
        password = data['password']
        password_mask = re.compile('\w{6,}')
        if not password_mask.match(password):
            raise serializers.ValidationError({'error':'Senha deve conter mais que 6 caracteres.'})
        confirm_password = data.pop('confirm_password')
        if not password == confirm_password:
            raise serializers.ValidationError({'error':'Campo senha e confirma senha devem ser iguais'})
        else:
            return data 

    def send_mail(self, data):

        subject = 'Bem vindo a API de Teste!'
        msg = 'Cadastro realizado com sucesso.\n\n' \
            f'Username: {self.validated_data["name"]}' \
            f'E-mail: {self.validated_data["email"]}\n'
        return send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL,[data.get('email')])

    def create(self, data):

        password = data.pop('password')
        user = User(**data)
        user.set_password(password)
        user.save()
        self.send_mail(data)
        return data

class FazendaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fazenda
        fields = ['id', 'name', 'owner', 'cpf','stations',
                  'created','modified']
    
    def validate(self, data):
        cpf_mask = re.compile('[0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2}')
        if not cpf_mask.match(data['cpf']):
            raise serializers.ValidationError({'error':'O CPF deve ter 11 números'})
        return data

class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = ['id', 'name', 'created', 'latitude', 'longitude','modified', 'fazenda']
        extra_kwargs = {
            'latitude' :  {'write_only':True},
            'longitude' : {'write_only':True},
            'fazenda' : {'write_only':True},
            'modified' : {'read_only':True}
        }

    def create(self, data):
        data['name'] = data.get('name').upper()
        return super(StationSerializer, self).create(data)
