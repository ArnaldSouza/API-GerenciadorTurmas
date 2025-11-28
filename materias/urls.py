from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MateriaViewSet

router = DefaultRouter()
router.register(r'materias', MateriaViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]