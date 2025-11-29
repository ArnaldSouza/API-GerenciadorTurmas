from django.contrib import admin
from .models import Professor

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ['nome', 'email', 'total_turmas']
    search_fields = ['nome', 'email']
    ordering = ['nome']
    
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('nome', 'email')
        }),
    )
    
    def total_turmas(self, obj):
        return obj.turma_set.count()
    total_turmas.short_description = 'Total de Turmas'
