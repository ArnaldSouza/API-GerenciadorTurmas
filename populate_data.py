#!/usr/bin/env python
"""
Script para popular o banco com dados de teste
Execute: python manage.py shell < populate_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gerenciador_turmas.settings')
django.setup()

from autenticacao.models import CustomUser
from alunos.models import Aluno
from professores.models import Professor
from materias.models import Materia
from turmas.models import Turma

def criar_dados_teste():
    print("=== Criando dados de teste ===")
    
    # 1. Criar usuários
    print("1. Criando usuários...")
    
    # Admin
    if not CustomUser.objects.filter(username='admin').exists():
        admin = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@teste.com',
            password='admin123',
            tipo_usuario='admin'
        )
        print(f"✓ Admin criado: {admin.username}")
    
    # Professores
    professores_data = [
        {'username': 'prof_joao', 'email': 'joao@teste.com', 'nome': 'João Silva'},
        {'username': 'prof_maria', 'email': 'maria@teste.com', 'nome': 'Maria Santos'},
    ]
    
    for prof_data in professores_data:
        if not CustomUser.objects.filter(username=prof_data['username']).exists():
            user = CustomUser.objects.create_user(
                username=prof_data['username'],
                email=prof_data['email'],
                password='prof123',
                tipo_usuario='professor',
                first_name=prof_data['nome'].split()[0],
                last_name=prof_data['nome'].split()[-1]
            )
            
            Professor.objects.create(
                nome=prof_data['nome'],
                email=prof_data['email']
            )
            print(f"✓ Professor criado: {prof_data['nome']}")
    
    # Alunos
    alunos_data = [
        {'username': 'aluno_pedro', 'email': 'pedro@teste.com', 'nome': 'Pedro Oliveira', 'matricula': '2024001'},
        {'username': 'aluno_ana', 'email': 'ana@teste.com', 'nome': 'Ana Costa', 'matricula': '2024002'},
        {'username': 'aluno_carlos', 'email': 'carlos@teste.com', 'nome': 'Carlos Lima', 'matricula': '2024003'},
    ]
    
    for aluno_data in alunos_data:
        if not CustomUser.objects.filter(username=aluno_data['username']).exists():
            user = CustomUser.objects.create_user(
                username=aluno_data['username'],
                email=aluno_data['email'],
                password='aluno123',
                tipo_usuario='aluno',
                first_name=aluno_data['nome'].split()[0],
                last_name=aluno_data['nome'].split()[-1]
            )
            
            Aluno.objects.create(
                nome=aluno_data['nome'],
                matricula=aluno_data['matricula'],
                email=aluno_data['email']
            )
            print(f"✓ Aluno criado: {aluno_data['nome']}")
    
    # 2. Criar matérias
    print("2. Criando matérias...")
    materias_data = [
        {'nome': 'Programação Distribuída', 'descricao': 'Conceitos de sistemas distribuídos'},
        {'nome': 'Banco de Dados', 'descricao': 'Modelagem e implementação de BD'},
        {'nome': 'Engenharia de Software', 'descricao': 'Metodologias de desenvolvimento'},
    ]
    
    for materia_data in materias_data:
        materia, created = Materia.objects.get_or_create(
            nome=materia_data['nome'],
            defaults={'descricao': materia_data['descricao']}
        )
        if created:
            print(f"✓ Matéria criada: {materia.nome}")
    
    # 3. Criar turmas
    print("3. Criando turmas...")
    turmas_data = [
        {
            'materia': 'Programação Distribuída',
            'professor': 'João Silva',
            'horario': 'Segunda 08:00-10:00',
            'alunos': ['Pedro Oliveira', 'Ana Costa']
        },
        {
            'materia': 'Banco de Dados',
            'professor': 'Maria Santos',
            'horario': 'Terça 14:00-16:00',
            'alunos': ['Carlos Lima', 'Pedro Oliveira']
        },
        {
            'materia': 'Engenharia de Software',
            'professor': 'João Silva',
            'horario': 'Quarta 10:00-12:00',
            'alunos': ['Ana Costa']
        },
    ]
    
    for turma_data in turmas_data:
        materia = Materia.objects.get(nome=turma_data['materia'])
        professor = Professor.objects.get(nome=turma_data['professor'])
        
        turma, created = Turma.objects.get_or_create(
            materia=materia,
            professor=professor,
            horario=turma_data['horario']
        )
        
        if created:
            # Adicionar alunos à turma
            for aluno_nome in turma_data['alunos']:
                try:
                    aluno = Aluno.objects.get(nome=aluno_nome)
                    turma.alunos.add(aluno)
                except Aluno.DoesNotExist:
                    print(f"⚠ Aluno não encontrado: {aluno_nome}")
            
            print(f"✓ Turma criada: {materia.nome} - {professor.nome}")
    
    print("\n=== Resumo dos dados criados ===")
    print(f"Usuários: {CustomUser.objects.count()}")
    print(f"Alunos: {Aluno.objects.count()}")
    print(f"Professores: {Professor.objects.count()}")
    print(f"Matérias: {Materia.objects.count()}")
    print(f"Turmas: {Turma.objects.count()}")
    print("\n✅ Dados de teste criados com sucesso!")

if __name__ == '__main__':
    criar_dados_teste()