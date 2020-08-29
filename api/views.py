from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import (TokenAuthentication,
SessionAuthentication,BasicAuthentication)
from rest_framework import viewsets, generics, mixins
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.authtoken.models import Token
from .models import Fazenda, Station
from .serializer import FazendaSerializer, StationSerializer, RegistrationSerializer
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class UserLogin(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user).key
        return Response({
            'id':user.pk,
            'name':user.name,
            'email':user.email,
            'created':user.date_joined,
            'modified':user.modified,
            'token':token
        })

class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = User.objects.filter(email=serializer.validated_data.get('email'))[0]
        return Response({
                        'id':user.pk,
                        'name':user.name,
                        'email':user.email,
                        'created':user.date_joined,
                        'modified':user.modified
                    })

class FazendaViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Fazenda.objects.all()
    serializer_class = FazendaSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]


class StationViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        station = self.get_object()
        if station.fazenda != None:
            return Response({'error':'Não é possível excluir uma estação vinculada a uma fazenda.'})
        else:
            return super(StationViewSet,self).destroy(request)