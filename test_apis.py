# Script de teste das APIs
import requests
import json

# Configurações
BASE_URL = "http://127.0.0.1:8000"
headers = {"Content-Type": "application/json"}

def test_api():
    print("=== TESTANDO APIs REST ===\n")
    
    # 1. Testar status
    print("1. Testando endpoint de status...")
    try:
        response = requests.get(f"{BASE_URL}/api/status/")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✓ API funcionando!")
            print(json.dumps(response.json(), indent=2))
        else:
            print("✗ Erro na API")
    except Exception as e:
        print(f"✗ Erro de conexão: {e}")
    
    print("\n" + "="*50)
    
    # 2. Testar login
    print("2. Testando login de aluno...")
    login_data = {
        "username": "aluno_pedro",
        "password": "aluno123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login/", 
                               json=login_data, headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            print("✓ Login realizado com sucesso!")
            print(f"Token: {token[:20]}...")
            
            # Headers com autenticação
            auth_headers = {
                "Content-Type": "application/json",
                "Authorization": f"Token {token}"
            }
            
            print("\n" + "="*50)
            
            # 3. Testar dashboard
            print("3. Testando dashboard...")
            response = requests.get(f"{BASE_URL}/api/dashboard/", headers=auth_headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✓ Dashboard funcionando!")
                dashboard_data = response.json()
                print(f"Total de turmas: {dashboard_data['estatisticas_gerais']['total_turmas']}")
                print(f"Total de alunos: {dashboard_data['estatisticas_gerais']['total_alunos']}")
                print(f"Usuário logado: {dashboard_data['usuario_logado']['tipo']}")
            
            print("\n" + "="*50)
            
            # 4. Testar lista de turmas
            print("4. Testando lista de turmas...")
            response = requests.get(f"{BASE_URL}/api/turmas/", headers=auth_headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                turmas = response.json()
                print(f"✓ {len(turmas['results']) if 'results' in turmas else len(turmas)} turmas encontradas!")
                
            print("\n" + "="*50)
            
            # 5. Testar dropdown de alunos
            print("5. Testando dropdown de alunos...")
            response = requests.get(f"{BASE_URL}/api/alunos/dropdown/", headers=auth_headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                alunos = response.json()
                print(f"✓ {len(alunos)} alunos no dropdown!")
                for aluno in alunos[:2]:  # Mostrar apenas os 2 primeiros
                    print(f"  - {aluno['label']} (ID: {aluno['value']})")
        
        else:
            print("✗ Erro no login")
            print(response.text)
            
    except Exception as e:
        print(f"✗ Erro: {e}")
    
    print("\n=== TESTE CONCLUÍDO ===")

if __name__ == "__main__":
    test_api()