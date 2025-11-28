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