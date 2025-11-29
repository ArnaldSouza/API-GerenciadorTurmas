from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from alunos.models import Aluno
from professores.models import Professor
from materias.models import Materia
from turmas.models import Turma

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_geral(request):
    total_alunos = Aluno.objects.count()
    total_professores = Professor.objects.count()
    total_materias = Materia.objects.count()
    total_turmas = Turma.objects.count()
    
    user_data = {}
    if request.user.tipo_usuario == 'aluno':
        try:
            aluno = Aluno.objects.get(id=request.user.id)
            user_data = {
                'tipo': 'aluno',
                'turmas_inscritas': aluno.turma_set.count(),
                'turmas_disponiveis': Turma.objects.exclude(alunos=aluno).count()
            }
        except Aluno.DoesNotExist:
            user_data = {'tipo': 'aluno', 'erro': 'Perfil de aluno não encontrado'}
    
    elif request.user.tipo_usuario == 'professor':
        try:
            professor = Professor.objects.get(id=request.user.id)
            user_data = {
                'tipo': 'professor',
                'minhas_turmas': professor.turma_set.count(),
                'total_alunos_minhas_turmas': sum(turma.alunos.count() for turma in professor.turma_set.all())
            }
        except Professor.DoesNotExist:
            user_data = {'tipo': 'professor', 'erro': 'Perfil de professor não encontrado'}
    
    top_turmas = []
    for turma in Turma.objects.all()[:5]:
        top_turmas.append({
            'id': turma.id,
            'materia': turma.materia.nome,
            'professor': turma.professor.nome,
            'total_alunos': turma.alunos.count(),
            'horario': turma.horario
        })
    
    return Response({
        'estatisticas_gerais': {
            'total_alunos': total_alunos,
            'total_professores': total_professores,
            'total_materias': total_materias,
            'total_turmas': total_turmas,
        },
        'usuario_logado': user_data,
        'top_turmas': top_turmas,
    })

@api_view(['GET'])
def status_api(request):
    return Response({
        'status': 'API funcionando',
        'endpoints': [
            '/api/auth/', '/api/alunos/', '/api/professores/', 
            '/api/materias/', '/api/turmas/', '/api/dashboard/'
        ]
    })