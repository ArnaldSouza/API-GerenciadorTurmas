from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Aluno
from .serializers import AlunoSerializer, AlunoCreateSerializer, AlunoDropdownSerializer, AlunoResumoSerializer
from turmas.models import Turma
from turmas.serializers import TurmaSerializer, InscricaoTurmaSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return AlunoCreateSerializer
        return AlunoSerializer
    
    @action(detail=True, methods=['get'])
    def turmas(self, request, pk=None):
        aluno = get_object_or_404(Aluno, pk=pk)
        turmas = Turma.objects.filter(alunos=aluno)
        serializer = TurmaSerializer(turmas, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def turmas_disponiveis(self, request, pk=None):
        aluno = get_object_or_404(Aluno, pk=pk)
        turmas_matriculadas = Turma.objects.filter(alunos=aluno).values_list('id', flat=True)
        turmas_disponiveis = Turma.objects.exclude(id__in=turmas_matriculadas)
        serializer = TurmaSerializer(turmas_disponiveis, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def inscrever_turma(self, request, pk=None):
        aluno = get_object_or_404(Aluno, pk=pk)
        serializer = InscricaoTurmaSerializer(data=request.data)
        
        if serializer.is_valid():
            turma_id = serializer.validated_data['turma_id']
            try:
                turma = Turma.objects.get(id=turma_id)
                
                if turma.alunos.filter(id=aluno.id).exists():
                    return Response(
                        {'error': 'Aluno já está inscrito nesta turma'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                turma.alunos.add(aluno)
                return Response({'message': 'Inscrição realizada com sucesso'})
                
            except Turma.DoesNotExist:
                return Response(
                    {'error': 'Turma não encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def cancelar_inscricao(self, request, pk=None):
        aluno = get_object_or_404(Aluno, pk=pk)
        serializer = InscricaoTurmaSerializer(data=request.data)
        
        if serializer.is_valid():
            turma_id = serializer.validated_data['turma_id']
            try:
                turma = Turma.objects.get(id=turma_id)
                turma.alunos.remove(aluno)
                return Response({'message': 'Inscrição cancelada com sucesso'})
                
            except Turma.DoesNotExist:
                return Response(
                    {'error': 'Turma não encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def dropdown(self, request):
        alunos = Aluno.objects.all()
        serializer = AlunoDropdownSerializer(alunos, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        alunos = Aluno.objects.all()[:10]
        serializer = AlunoResumoSerializer(alunos, many=True)
        return Response({
            'alunos': serializer.data,
            'total_alunos': Aluno.objects.count(),
        })