from django.urls import path, include
from rest_framework import routers
from .views import UsuarioViewSet, UserLogin, FazendaViewSet, StationViewSet, UserCreate

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'fazenda', FazendaViewSet)
router.register(r'station', StationViewSet)
router.register(r'cadastro/admin', UsuarioViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>', include(router.urls)),
    path('cadastro/', UserCreate.as_view(), name='cadastro'),
    path('login/', UserLogin.as_view(), name='login')
]
