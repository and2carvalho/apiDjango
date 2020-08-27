from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet, UserLogin, FazendaViewSet, StationViewSet
from .serializer import LoginSerializer

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'fazenda', FazendaViewSet)
router.register(r'station', StationViewSet)
router.register(r'cadastro', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('<int:pk>', include(router.urls)),
    path('login/', UserLogin.as_view(serializer_class=LoginSerializer), name='login')
]
