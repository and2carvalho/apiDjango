from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status, viewsets,generics, mixins
from django.contrib.auth.models import User
from .models import Fazenda, Station
from .serializer import (FazendaSerializer, StationSerializer,
UserSerializer)
import re


class UserViewSet(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny, )


class FazendaViewSet(viewsets.ModelViewSet):
    queryset = Fazenda.objects.all()
    serializer_class = FazendaSerializer
    #permission_classes = (IsAuthenticated, )


    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, pk=None):
       return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

    #def perform_create(self, request):
    #    serializer = FazendaSerializer(data=request.data)
    #    cpf_mask = re.compile('[0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2}')
    #    if serializer.is_valid() and cpf_mask.match(serializer.data['cpf']):
    #        serializer.save()
    #        return Response(serializer.data, status=201)
    #    else:
    #        return Response({'error' : 'Formatação errada de CPF'}, status=400)
    #    return Response(serializer.errors, status=400)

class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    #permission_classes = (IsAuthenticated, )

    def get(self, request, pk=None):
        if pk:
            return self.retrieve(request, pk)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, pk=None):
       return self.update(request, pk)

    def delete(self, request, pk):
        return self.destroy(request, pk)

#@api_view(['GET','POST'])
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
#@api_view(['PUT','DELETE', 'PATCH'])
#def update_fazenda(request, id):
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

#@api_view(['GET','POST'])
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