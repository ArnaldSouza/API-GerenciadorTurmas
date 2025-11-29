from django.contrib import admin
from .models import Materia

@admin.register(Materia)
class MateriaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'descricao', 'total_turmas']
    search_fields = ['nome']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações da Matéria', {
            'fields': ('nome', 'descricao')
        }),
    )
    
    def total_turmas(self, obj):
        return obj.turma_set.count()
    total_turmas.short_description = 'Total de Turmas'
