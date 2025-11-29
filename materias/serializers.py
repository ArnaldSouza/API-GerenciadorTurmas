from rest_framework import serializers
from .models import Materia

class MateriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = '__all__'

class MateriaCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Materia
        fields = ['nome', 'descricao']

class MateriaDropdownSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='nome', read_only=True)
    value = serializers.CharField(source='id', read_only=True)
    
    class Meta:
        model = Materia
        fields = ['value', 'label', 'descricao']

class MateriaResumoSerializer(serializers.ModelSerializer):
    total_turmas = serializers.SerializerMethodField()
    total_professores = serializers.SerializerMethodField()
    
    class Meta:
        model = Materia
        fields = ['id', 'nome', 'descricao', 'total_turmas', 'total_professores']
    
    def get_total_turmas(self, obj):
        return obj.turma_set.count()
    
    def get_total_professores(self, obj):
        return obj.turma_set.values('professor').distinct().count()        