from django.contrib import admin
from .models import Turma

class AlunoInline(admin.TabularInline):
    model = Turma.alunos.through
    extra = 1
    verbose_name = 'Aluno inscrito'
    verbose_name_plural = 'Alunos inscritos'

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ['get_turma_info', 'professor', 'horario', 'total_alunos', 'vagas_disponiveis']
    list_filter = ['materia', 'professor', 'horario']
    search_fields = ['materia__nome', 'professor__nome']
    ordering = ['materia__nome', 'horario']
    
    fieldsets = (
        ('Informações da Turma', {
            'fields': ('materia', 'professor', 'horario')
        }),
    )
    
    inlines = [AlunoInline]
    
    def get_turma_info(self, obj):
        return f"{obj.materia.nome}"
    get_turma_info.short_description = 'Matéria'
    
    def total_alunos(self, obj):
        return obj.alunos.count()
    total_alunos.short_description = 'Total de Alunos'
    
    def vagas_disponiveis(self, obj):
        # Assumindo limite de 30 alunos por turma
        return 30 - obj.alunos.count()
    vagas_disponiveis.short_description = 'Vagas Disponíveis'
