from django.contrib import admin
from .models import Aluno

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ['nome', 'matricula', 'email']
    list_filter = ['matricula']
    search_fields = ['nome', 'matricula', 'email']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'email')
        }),
        ('Informações Acadêmicas', {
            'fields': ('matricula',)
        }),
    )
