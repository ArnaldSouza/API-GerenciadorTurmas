from rest_framework import serializers
from .models import Professor

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

class ProfessorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = ['nome', 'email']

class ProfessorDropdownSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='nome', read_only=True)
    value = serializers.CharField(source='id', read_only=True)
    
    class Meta:
        model = Professor
        fields = ['value', 'label', 'email']

class ProfessorResumoSerializer(serializers.ModelSerializer):
    total_turmas = serializers.SerializerMethodField()
    total_alunos = serializers.SerializerMethodField()
    
    class Meta:
        model = Professor
        fields = ['id', 'nome', 'email', 'total_turmas', 'total_alunos']
    
    def get_total_turmas(self, obj):
        return obj.turma_set.count()
    
    def get_total_alunos(self, obj):
        return sum(turma.alunos.count() for turma in obj.turma_set.all())