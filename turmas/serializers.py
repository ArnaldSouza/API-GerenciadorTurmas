from rest_framework import serializers
from .models import Turma
from alunos.serializers import AlunoSerializer
from professores.serializers import ProfessorSerializer
from materias.serializers import MateriaSerializer

class TurmaSerializer(serializers.ModelSerializer):
    alunos = AlunoSerializer(many=True, read_only=True)
    professor = ProfessorSerializer(read_only=True)
    materia = MateriaSerializer(read_only=True)
    
    class Meta:
        model = Turma
        fields = ['id', 'materia', 'professor', 'alunos', 'horario']

class TurmaCreateSerializer(serializers.ModelSerializer):
    alunos_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = Turma
        fields = ['materia', 'professor', 'horario', 'alunos_ids']
    
    def create(self, validated_data):
        alunos_ids = validated_data.pop('alunos_ids', [])
        turma = Turma.objects.create(**validated_data)
        if alunos_ids:
            turma.alunos.set(alunos_ids)
        return turma

class InscricaoTurmaSerializer(serializers.Serializer):
    aluno_id = serializers.IntegerField()
    turma_id = serializers.IntegerField()