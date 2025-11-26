from django.shortcuts import render
from rest_framework import viewsets
from .models import Materia
from .serializers import MateriaSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer

