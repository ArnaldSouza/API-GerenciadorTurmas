from django.db import models
from materias.models import Materia
from professores.models import Professor
from alunos.models import Aluno

class Turma(models.Model):
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='turmas')
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='turmas')
    alunos = models.ManyToManyField(Aluno, related_name='turmas')
    horario = models.CharField(max_length=100)  

    def __str__(self):
        return f"{self.materia.nome} - {self.professor.nome} ({self.horario})"