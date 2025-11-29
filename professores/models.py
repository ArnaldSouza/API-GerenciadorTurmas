from django.db import models

class Professor(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return self.nome

