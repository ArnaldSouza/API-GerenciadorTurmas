from django.shortcuts import render
from rest_framework import viewsets
from .models import Turma
from .serializers import TurmaSerializer, TurmaCreateSerializer

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TurmaCreateSerializer
        return TurmaSerializer

