from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt import views as jwt_views
from .views import FazendaViewSet, StationViewSet, UserViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register(r'fazenda', FazendaViewSet)
router.register(r'station', StationViewSet)

urlpatterns = [
    #path('fazenda/', FazendaViewSet.as_view(), name='fazenda'),
    path('cadastro/', UserViewSet.as_view(), name='cadastro'),
    path('', jwt_views.ObtainJSONWebToken.as_view(), name='get-token'),
    path('', include(router.urls))
]
