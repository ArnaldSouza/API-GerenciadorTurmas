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

class TurmaCardSerializer(serializers.ModelSerializer):
    """Serializer otimizado para cards de turma no React"""
    materia_nome = serializers.CharField(source='materia.nome', read_only=True)
    professor_nome = serializers.CharField(source='professor.nome', read_only=True)
    total_alunos = serializers.SerializerMethodField()
    vagas_disponiveis = serializers.SerializerMethodField()
    
    class Meta:
        model = Turma
        fields = ['id', 'materia_nome', 'professor_nome', 'horario', 'total_alunos', 'vagas_disponiveis']
    
    def get_total_alunos(self, obj):
        return obj.alunos.count()
    
    def get_vagas_disponiveis(self, obj):
        # Assumindo limite de 30 alunos por turma
        return 30 - obj.alunos.count()

class TurmaDetalhesSerializer(serializers.ModelSerializer):
    """Serializer completo para página de detalhes da turma"""
    materia = MateriaSerializer(read_only=True)
    professor = ProfessorSerializer(read_only=True)
    alunos = AlunoSerializer(many=True, read_only=True)
    total_alunos = serializers.SerializerMethodField()
    pode_se_inscrever = serializers.SerializerMethodField()
    
    class Meta:
        model = Turma
        fields = ['id', 'materia', 'professor', 'alunos', 'horario', 'total_alunos', 'pode_se_inscrever']
    
    def get_total_alunos(self, obj):
        return obj.alunos.count()
    
    def get_pode_se_inscrever(self, obj):
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return False
        if request.user.tipo_usuario != 'aluno':
            return False
        return obj.alunos.filter(id=request.user.id).exists() == False