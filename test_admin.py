# Script para testar o Admin Django
import webbrowser
import time
import requests

def test_admin():
    print("=== TESTANDO ADMIN DJANGO ===\n")
    
    admin_url = "http://127.0.0.1:8000/admin/"
    
    print(f"1. Abrindo admin Django em: {admin_url}")
    print("   Credenciais:")
    print("   Username: admin")
    print("   Password: admin123")
    print()
    
    # Tentar verificar se o servidor está rodando
    try:
        response = requests.get("http://127.0.0.1:8000/admin/", timeout=5)
        if response.status_code == 200:
            print("✓ Servidor Django está rodando!")
            print("✓ Admin Django está acessível!")
            
            # Abrir navegador automaticamente
            webbrowser.open(admin_url)
            print("✓ Navegador aberto automaticamente!")
            
        else:
            print(f"⚠ Servidor responde, mas com status: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Erro ao conectar com servidor: {e}")
        print("   Certifique-se de que o servidor Django está rodando:")
        print("   python manage.py runserver 8000")
    
    print("\n=== FUNCIONALIDADES DO ADMIN ===")
    print("No admin Django você pode:")
    print("1. 👥 Gerenciar ALUNOS:")
    print("   - Listar, adicionar, editar e excluir alunos")
    print("   - Buscar por nome, matrícula ou email")
    print("   - Visualizar informações organizadas")
    
    print("\n2. 👨‍🏫 Gerenciar PROFESSORES:")
    print("   - CRUD completo de professores")
    print("   - Ver quantas turmas cada professor tem")
    print("   - Buscar por nome ou email")
    
    print("\n3. 📚 Gerenciar MATÉRIAS:")
    print("   - Adicionar/editar matérias")
    print("   - Ver quantas turmas cada matéria tem")
    
    print("\n4. 🏫 Gerenciar TURMAS:")
    print("   - Criar e editar turmas")
    print("   - Inscrever/remover alunos das turmas")
    print("   - Ver total de alunos e vagas disponíveis")
    print("   - Filtrar por matéria, professor ou horário")
    
    print("\n5. 🔐 Gerenciar USUÁRIOS:")
    print("   - Criar usuários aluno/professor/admin")
    print("   - Definir permissões e tipos de usuário")
    
    print("\n=== TESTE CONCLUÍDO ===")
    print("Acesse o admin para testar todas as funcionalidades!")

if __name__ == "__main__":
    test_admin()