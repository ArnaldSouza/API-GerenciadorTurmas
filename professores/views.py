from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Professor
from .serializers import ProfessorSerializer, ProfessorCreateSerializer
from turmas.models import Turma
from turmas.serializers import TurmaSerializer, TurmaCreateSerializer
from materias.models import Materia
from materias.serializers import MateriaSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProfessorCreateSerializer
        return ProfessorSerializer
    
    def get_professor(self, pk):
        return get_object_or_404(Professor, pk=pk)
    
    @action(detail=True, methods=['get'])
    def turmas(self, request, pk=None):
        professor = self.get_professor(pk)
        turmas = Turma.objects.filter(professor=professor)
        serializer = TurmaSerializer(turmas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def materias(self, request, pk=None):
        professor = self.get_professor(pk)       
        materias = Materia.objects.all()
        serializer = MateriaSerializer(materias, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def criar_turma(self, request, pk=None):
        professor = self.get_professor(pk)
        serializer = TurmaCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            materia_id = serializer.validated_data['materia'].id
            try:
                materia = Materia.objects.get(id=materia_id)
                serializer.validated_data['professor'] = professor
                
                turma = serializer.save()
                response_serializer = TurmaSerializer(turma)
                return Response({
                    'success': True,
                    'message': 'Turma criada com sucesso',
                    'data': response_serializer.data
                }, status=status.HTTP_201_CREATED)
                
            except Materia.DoesNotExist:
                return Response(
                    {
                        'success': False,
                        'message': 'Matéria não encontrada',
                        'error_code': 'MATERIA_NOT_FOUND'
                    }, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)