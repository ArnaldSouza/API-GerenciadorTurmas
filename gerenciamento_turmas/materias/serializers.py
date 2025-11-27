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
        