from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from rest_framework import viewsets, generics, mixins
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Fazenda, Station
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


#from rest_framework.decorators import api_view, authentication_classes, permission_classes
#from rest_framework.response import Response
#from rest_framework.parsers import JSONParser
#from rest_framework import status
#
#@api_view(['GET','POST'])
#@authentication_classes([TokenAuthentication, SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
#def lista_fazenda(request):
#    if request.method == 'POST':
#        try:
#            serializer = FazendaSerializer(data=request.data)
#            if serializer.is_valid():
#                serializer.save()
#                return Response(serializer.data, status=status.HTTP_201_CREATED)
#            else:
#                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#        except Exception as e:
#            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#    else:
#        resp = FazendaSerializer(Fazenda.objects.all(), many=True)
#        return Response(resp.data)
#
#@api_view(['PUT', 'DELETE', 'PATCH', 'GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#@permission_classes([IsAuthenticated])
#def update_fazenda(request, id):
#
#    try:
#        fazenda = Fazenda.objects.get(pk=id)
#    except Exception as e:
#        return Response({'error' : str(e)}, status=status.HTTP_404_NOT_FOUND)
#    if request.method == 'PUT':
#        serializer = FazendaSerializer(fazenda, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_200_OK)
#        else:
#            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#    elif request.method == 'DELETE':
#        fazenda.delete()
#        return Response({'status' : f'id {id} excluido'}, status=status.HTTP_204_NO_CONTENT)
#    else:
#        resp = FazendaSerializer(fazenda)
#        return Response (resp.data, status=status.HTTP_200_OK)
#        
#@api_view(['GET','POST'])
#@api_view(['PUT', 'DELETE', 'PATCH', 'GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#def lista_station(request):
#    if request.method == 'POST':
#        try:
#            serializer = StationSerializer(data=request.data)
#            if serializer.is_valid():
#                serializer.save()
#                return Response(serializer.data, status=status.HTTP_201_CREATED)
#            else:
#                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#        except Exception as e:
#            return Response({'error':str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#    else:
#        resp = StationSerializer(Station.objects.all(), many=True)
#        return Response(resp.data)
#
#@api_view(['PUT','DELETE'])
#@api_view(['PUT', 'DELETE', 'PATCH', 'GET'])
#@authentication_classes([SessionAuthentication, BasicAuthentication])
#def update_station(request, id):
#    try:
#        station = Station.objects.get(pk=id)
#    except Exception as e:
#        return Response({'error' : str(e)}, status=status.HTTP_404_NOT_FOUND)
#    if request.method == 'PUT':
#        serializer = StationSerializer(station, data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#            return Response(serializer.data, status=status.HTTP_200_OK)
#        else:
#            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#    elif request.method == 'DELETE':
#        station.delete()
#        return Response({'status' : f'id {id} excluido'}, status=status.HTTP_204_NO_CONTENT)