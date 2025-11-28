from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProfessorViewSet

router = DefaultRouter()
router.register(r'professores', ProfessorViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]