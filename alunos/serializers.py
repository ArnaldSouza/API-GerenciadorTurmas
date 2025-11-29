from rest_framework import serializers
from .models import Aluno

class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = '__all__'

class AlunoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aluno
        fields = ['nome', 'matricula', 'email']

class AlunoDropdownSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='nome', read_only=True)
    value = serializers.CharField(source='id', read_only=True)
    
    class Meta:
        model = Aluno
        fields = ['value', 'label', 'matricula']

class AlunoResumoSerializer(serializers.ModelSerializer):
    total_turmas = serializers.SerializerMethodField()
    
    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'matricula', 'email', 'total_turmas']
    
    def get_total_turmas(self, obj):
        return obj.turma_set.count()