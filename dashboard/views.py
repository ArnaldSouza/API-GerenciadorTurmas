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
        'success': True,
        'data': {
            'statistics': {
                'total_alunos': total_alunos,
                'total_professores': total_professores,
                'total_materias': total_materias,
                'total_turmas': total_turmas,
            },
            'user_profile': user_data,
            'featured_items': top_turmas,
        },
        'meta': {
            'resource_type': 'dashboard',
            'user_type': request.user.tipo_usuario if hasattr(request.user, 'tipo_usuario') else 'anonymous'
        }
    })

@api_view(['GET'])
def status_api(request):
    return Response({
        'success': True,
        'message': 'API funcionando corretamente',
        'data': {
            'version': '1.0.0',
            'status': 'healthy',
            'endpoints': {
                'auth': '/api/auth/',
                'alunos': '/api/alunos/',
                'professores': '/api/professores/',
                'materias': '/api/materias/',
                'turmas': '/api/turmas/',
                'dashboard': '/api/dashboard/'
            }
        },
        'meta': {
            'timestamp': request.META.get('HTTP_DATE'),
            'server': 'Django REST Framework'
        }
    })