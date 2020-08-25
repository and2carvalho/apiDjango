from rest_framework import serializers
from django.conf import settings
from django.contrib.auth.models import User
from .models import Fazenda, Station
import re


class UserSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ['username','email', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user.__dict__
    


class FazendaSerializer(serializers.ModelSerializer):


    class Meta:
        model = Fazenda
        fields = ['id', 'name', 'owner', 'cpf', 'stations',
        'created','modified']
    
    #def create(self, validated_data):
    #    cpf_mask = re.compile('[0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2}')
    #    cpf = validated_data.pop('cpf')
    #    cpf = str(cpf_mask.match(cpf))
    #    fazenda = Fazenda(**validated_data)
    #    fazenda.save()
    #    return fazenda.__dict__
        
        

class StationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Station
        fields = ['id', 'name', 'latitude', 'longitude',
        'created', 'modified', 'fazenda']
        extra_kwargs = {
            'latitude' :  {'write_only':True},
            'longitude' : {'write_only':True},
            'fazenda' : {'write_only':True},
        }    