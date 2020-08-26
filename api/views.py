from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import (TokenAuthentication,
SessionAuthentication,BasicAuthentication)
from rest_framework import viewsets, generics, mixins
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.authtoken.models import Token
#from django.contrib.auth.models import User
from .models import Fazenda, Station, User
from .serializer import FazendaSerializer, StationSerializer, RegistrationSerializer

class UserLogin(ObtainJSONWebToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                       context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = Token.objects.get(user=user).key
        return Response({
            'id':user.pk,
            'name':user.username,
            'email':user.email,
            'token':token
        })

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]

class UsuarioViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.UpdateModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = [IsAuthenticated]

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

