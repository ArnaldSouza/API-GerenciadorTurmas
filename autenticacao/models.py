from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TIPO_CHOICES = [
        ('aluno', 'Aluno'),
        ('professor', 'Professor'),
        ('admin', 'Administrador'),
    ]
    
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_CHOICES)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.username} - {self.get_tipo_usuario_display()}"