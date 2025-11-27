import grpc
from concurrent import futures
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gerenciador_turmas.settings')
django.setup()

from grpc import StatusCode
from alunos.models import Aluno
from professores.models import Professor
from materias.models import Materia
from turmas.models import Turma
from grpc import ServicerContext
from grpc import StatusCode
from grpc import gerenciador_pb2, gerenciador_pb2_grpc



# --- Aluno ---
class AlunoService(gerenciador_pb2_grpc.AlunoServiceServicer):
    def ListAlunos(self, request, context):
        alunos = Aluno.objects.all()
        return gerenciador_pb2.AlunosList(
            alunos=[gerenciador_pb2.Aluno(
                id=aluno.id, nome=aluno.nome, matricula=aluno.matricula, email=aluno.email
            ) for aluno in alunos]
        )

    def GetAluno(self, request, context):
        try:
            aluno = Aluno.objects.get(pk=request.id)
            return gerenciador_pb2.Aluno(
                id=aluno.id, nome=aluno.nome, matricula=aluno.matricula, email=aluno.email
            )
        except Aluno.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Aluno not found')
            return gerenciador_pb2.Aluno()

    def CreateAluno(self, request, context):
        aluno = Aluno(nome=request.nome, matricula=request.matricula, email=request.email)
        aluno.save()
        return gerenciador_pb2.AlunoId(id=aluno.id)

    def UpdateAluno(self, request, context):
        try:
            aluno = Aluno.objects.get(pk=request.id)
            aluno.nome = request.nome
            aluno.matricula = request.matricula
            aluno.email = request.email
            aluno.save()
        except Aluno.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Aluno not found')
        return gerenciador_pb2.Empty()

    def DeleteAluno(self, request, context):
        try:
            Aluno.objects.get(pk=request.id).delete()
        except Aluno.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Aluno not found')
        return gerenciador_pb2.Empty()



# --- Professor ---
class ProfessorService(gerenciador_pb2_grpc.ProfessorServiceServicer):
    def ListProfessores(self, request, context):
        professores = Professor.objects.all()
        return gerenciador_pb2.ProfessoresList(
            professores=[gerenciador_pb2.Professor(
                id=prof.id, nome=prof.nome, email=prof.email
            ) for prof in professores]
        )

    def GetProfessor(self, request, context):
        try:
            prof = Professor.objects.get(pk=request.id)
            return gerenciador_pb2.Professor(id=prof.id, nome=prof.nome, email=prof.email)
        except Professor.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Professor not found')
            return gerenciador_pb2.Professor()

    def CreateProfessor(self, request, context):
        prof = Professor(nome=request.nome, email=request.email)
        prof.save()
        return gerenciador_pb2.ProfessorId(id=prof.id)

    def UpdateProfessor(self, request, context):
        try:
            prof = Professor.objects.get(pk=request.id)
            prof.nome = request.nome
            prof.email = request.email
            prof.save()
        except Professor.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Professor not found')
        return gerenciador_pb2.Empty()

    def DeleteProfessor(self, request, context):
        try:
            Professor.objects.get(pk=request.id).delete()
        except Professor.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Professor not found')
        return gerenciador_pb2.Empty()



# --- Materia ---
class MateriaService(gerenciador_pb2_grpc.MateriaServiceServicer):
    def ListMaterias(self, request, context):
        materias = Materia.objects.all()
        return gerenciador_pb2.MateriasList(
            materias=[gerenciador_pb2.Materia(
                id=mat.id, nome=mat.nome, descricao=mat.descricao
            ) for mat in materias]
        )

    def GetMateria(self, request, context):
        try:
            mat = Materia.objects.get(pk=request.id)
            return gerenciador_pb2.Materia(id=mat.id, nome=mat.nome, descricao=mat.descricao)
        except Materia.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Materia not found')
            return gerenciador_pb2.Materia()

    def CreateMateria(self, request, context):
        mat = Materia(nome=request.nome, descricao=request.descricao)
        mat.save()
        return gerenciador_pb2.MateriaId(id=mat.id)

    def UpdateMateria(self, request, context):
        try:
            mat = Materia.objects.get(pk=request.id)
            mat.nome = request.nome
            mat.descricao = request.descricao
            mat.save()
        except Materia.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Materia not found')
        return gerenciador_pb2.Empty()

    def DeleteMateria(self, request, context):
        try:
            Materia.objects.get(pk=request.id).delete()
        except Materia.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Materia not found')
        return gerenciador_pb2.Empty()



# --- Turma ---
class TurmaService(gerenciador_pb2_grpc.TurmaServiceServicer):
    def ListTurmas(self, request, context):
        turmas = Turma.objects.all()
        return gerenciador_pb2.TurmasList(
            turmas=[
                gerenciador_pb2.Turma(
                    id=turma.id,
                    materia=turma.materia.id if turma.materia else 0,
                    professor=turma.professor.id if turma.professor else 0,
                    alunos=[aluno.id for aluno in turma.alunos.all()],
                    horario=turma.horario
                ) for turma in turmas
            ]
        )

    def GetTurma(self, request, context):
        try:
            turma = Turma.objects.get(pk=request.id)
            return gerenciador_pb2.Turma(
                id=turma.id,
                materia=turma.materia.id if turma.materia else 0,
                professor=turma.professor.id if turma.professor else 0,
                alunos=[aluno.id for aluno in turma.alunos.all()],
                horario=turma.horario
            )
        except Turma.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Turma not found')
            return gerenciador_pb2.Turma()

    def CreateTurma(self, request, context):
        try:
            materia = Materia.objects.get(pk=request.materia)
            professor = Professor.objects.get(pk=request.professor)
            turma = Turma(materia=materia, professor=professor, horario=request.horario)
            turma.save()
            turma.alunos.set(list(request.alunos))
            turma.save()
            return gerenciador_pb2.TurmaId(id=turma.id)
        except (Materia.DoesNotExist, Professor.DoesNotExist):
            context.set_code(StatusCode.INVALID_ARGUMENT)
            context.set_details('Materia ou Professor inválidos')
            return gerenciador_pb2.TurmaId(id=0)

    def UpdateTurma(self, request, context):
        try:
            turma = Turma.objects.get(pk=request.id)
            materia = Materia.objects.get(pk=request.materia)
            professor = Professor.objects.get(pk=request.professor)
            turma.materia = materia
            turma.professor = professor
            turma.horario = request.horario
            turma.save()
            turma.alunos.set(list(request.alunos))
            turma.save()
        except Turma.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Turma not found')
        except (Materia.DoesNotExist, Professor.DoesNotExist):
            context.set_code(StatusCode.INVALID_ARGUMENT)
            context.set_details('Materia ou Professor inválidos')
        return gerenciador_pb2.Empty()

    def DeleteTurma(self, request, context):
        try:
            Turma.objects.get(pk=request.id).delete()
        except Turma.DoesNotExist:
            context.set_code(StatusCode.NOT_FOUND)
            context.set_details('Turma not found')
        return gerenciador_pb2.Empty()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    gerenciador_pb2_grpc.add_AlunoServiceServicer_to_server(AlunoService(), server)
    gerenciador_pb2_grpc.add_ProfessorServiceServicer_to_server(ProfessorService(), server)
    gerenciador_pb2_grpc.add_MateriaServiceServicer_to_server(MateriaService(), server)
    gerenciador_pb2_grpc.add_TurmaServiceServicer_to_server(TurmaService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print('gRPC server running on port 50051')
    server.wait_for_termination()

if __name__ == '__main__':
    serve()