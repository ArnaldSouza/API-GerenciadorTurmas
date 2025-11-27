from django.shortcuts import render
from rest_framework import viewsets
from .models import Materia
from .serializers import MateriaSerializer, MateriaCreateSerializer

class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MateriaCreateSerializer
        return MateriaSerializer