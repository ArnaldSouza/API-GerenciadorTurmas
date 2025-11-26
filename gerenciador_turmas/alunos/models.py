from django.db import models

class Aluno(models.Model):
    nome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=6, unique=True)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.nome} ({self.matricula})"
