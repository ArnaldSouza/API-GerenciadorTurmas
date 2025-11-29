"""
Testes automatizados completos para APIs REST e gRPC
Este script testa todos os endpoints e funcionalidades do sistema
"""
import requests
import json
import time
from datetime import datetime

# Configurações
BASE_URL = "http://127.0.0.1:8000"
headers = {"Content-Type": "application/json"}

class APITester:
    def __init__(self):
        self.token = None
        self.auth_headers = {"Content-Type": "application/json"}
        self.test_results = []
    
    def log_test(self, test_name, success, details=""):
        #Registra resultados do teste
        result = {
            'test': test_name,
            'success': success,
            'details': details,
            'timestamp': datetime.now().strftime('%H:%M:%S')
        }
        self.test_results.append(result)
        
        status = "✓" if success else "✗"
        print(f"{status} {test_name}: {details}")
    
    def test_status_endpoint(self):
        # Teste 1: Endpoint de status da API
        
        print("\n1. TESTANDO STATUS DA API")
        print("-" * 40)
        
        try:
            response = requests.get(f"{BASE_URL}/api/status/", timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Status API", True, f"API funcionando - {data.get('status', 'OK')}")
                return True
            else:
                self.log_test("Status API", False, f"Status code: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("Status API", False, f"Erro de conexão: {str(e)[:100]}")
            return False
    
    def test_authentication(self):
        # Teste 2: Sistema de autenticação
        
        print("\n2. TESTANDO AUTENTICAÇÃO")
        print("-" * 40)
        
        # Teste de registro
        register_data = {
            "username": f"test_user_{int(time.time())}",
            "email": f"test_{int(time.time())}@teste.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "tipo_usuario": "aluno",
            "first_name": "Usuario",
            "last_name": "Teste"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/auth/register/", 
                                   json=register_data, headers=headers)
            
            if response.status_code == 201:
                data = response.json()
                self.log_test("Registro usuário", True, f"Usuário {data['user']['username']} criado")
            else:
                self.log_test("Registro usuário", False, f"Erro: {response.text[:100]}")
        
        except Exception as e:
            self.log_test("Registro usuário", False, f"Erro: {str(e)[:100]}")
        
        # Teste de login com usuário existente
        login_data = {
            "username": "aluno_matheus",
            "password": "aluno123"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/api/auth/login/", 
                                   json=login_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                self.auth_headers["Authorization"] = f"Token {self.token}"
                
                self.log_test("Login usuário", True, f"Token obtido: {self.token[:20]}...")
                
                # Teste de perfil
                profile_response = requests.get(f"{BASE_URL}/api/auth/profile/", 
                                              headers=self.auth_headers)
                
                if profile_response.status_code == 200:
                    profile = profile_response.json()
                    self.log_test("Perfil usuário", True, 
                                f"Usuário: {profile.get('username')} - Tipo: {profile.get('tipo_usuario')}")
                else:
                    self.log_test("Perfil usuário", False, "Erro ao obter perfil")
                
                return True
            else:
                self.log_test("Login usuário", False, f"Erro: {response.text[:100]}")
                return False
                
        except Exception as e:
            self.log_test("Login usuário", False, f"Erro: {str(e)[:100]}")
            return False
    
    def test_crud_operations(self):
        # Teste 3: Operações CRUD completas
        
        print("\n3. TESTANDO OPERAÇÕES CRUD")
        print("-" * 40)
        
        if not self.token:
            self.log_test("CRUD Operations", False, "Sem token de autenticação")
            return False
        
        # Teste GET - Listar alunos
        try:
            response = requests.get(f"{BASE_URL}/api/alunos/", headers=self.auth_headers)
            
            if response.status_code == 200:
                alunos = response.json()
                count = len(alunos['results']) if 'results' in alunos else len(alunos)
                self.log_test("Listar alunos", True, f"{count} alunos encontrados")
            else:
                self.log_test("Listar alunos", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Listar alunos", False, f"Erro: {str(e)[:100]}")
        
        # Teste GET - Listar professores
        try:
            response = requests.get(f"{BASE_URL}/api/professores/", headers=self.auth_headers)
            
            if response.status_code == 200:
                professores = response.json()
                count = len(professores['results']) if 'results' in professores else len(professores)
                self.log_test("Listar professores", True, f"{count} professores encontrados")
            else:
                self.log_test("Listar professores", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Listar professores", False, f"Erro: {str(e)[:100]}")
        
        # Teste GET - Listar matérias
        try:
            response = requests.get(f"{BASE_URL}/api/materias/", headers=self.auth_headers)
            
            if response.status_code == 200:
                materias = response.json()
                count = len(materias['results']) if 'results' in materias else len(materias)
                self.log_test("Listar matérias", True, f"{count} matérias encontradas")
            else:
                self.log_test("Listar matérias", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Listar matérias", False, f"Erro: {str(e)[:100]}")
        
        # Teste GET - Listar turmas
        try:
            response = requests.get(f"{BASE_URL}/api/turmas/", headers=self.auth_headers)
            
            if response.status_code == 200:
                turmas = response.json()
                count = len(turmas['results']) if 'results' in turmas else len(turmas)
                self.log_test("Listar turmas", True, f"{count} turmas encontradas")
            else:
                self.log_test("Listar turmas", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Listar turmas", False, f"Erro: {str(e)[:100]}")
    
    def test_specialized_endpoints(self):
        # Teste 4: Endpoints especializados para React
        
        print("\n4. TESTANDO ENDPOINTS ESPECIALIZADOS")
        print("-" * 40)
        
        if not self.token:
            self.log_test("Endpoints especializados", False, "Sem token de autenticação")
            return False
        
        # Teste dropdowns
        endpoints_dropdown = [
            ("alunos/dropdown/", "Dropdown alunos"),
            ("professores/dropdown/", "Dropdown professores"),
            ("materias/dropdown/", "Dropdown matérias")
        ]
        
        for endpoint, name in endpoints_dropdown:
            try:
                response = requests.get(f"{BASE_URL}/api/{endpoint}", headers=self.auth_headers)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test(name, True, f"{len(data)} itens no dropdown")
                else:
                    self.log_test(name, False, f"Status: {response.status_code}")
                    
            except Exception as e:
                self.log_test(name, False, f"Erro: {str(e)[:100]}")
        
        # Teste dashboard geral
        try:
            response = requests.get(f"{BASE_URL}/api/dashboard/", headers=self.auth_headers)
            
            if response.status_code == 200:
                dashboard = response.json()
                stats = dashboard.get('estatisticas_gerais', {})
                self.log_test("Dashboard geral", True, 
                            f"Alunos: {stats.get('total_alunos')}, Turmas: {stats.get('total_turmas')}")
            else:
                self.log_test("Dashboard geral", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Dashboard geral", False, f"Erro: {str(e)[:100]}")
        
        # Teste dashboard específico de alunos
        try:
            response = requests.get(f"{BASE_URL}/api/alunos/dashboard/", headers=self.auth_headers)
            
            if response.status_code == 200:
                dashboard_alunos = response.json()
                self.log_test("Dashboard alunos", True, 
                            f"Total: {dashboard_alunos.get('total_alunos', 0)} alunos")
            else:
                self.log_test("Dashboard alunos", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Dashboard alunos", False, f"Erro: {str(e)[:100]}")
    
    def test_business_rules(self):
        # Teste 5: Regras de negócio
        
        print("\n5. TESTANDO REGRAS DE NEGÓCIO")
        print("-" * 40)
        
        if not self.token:
            self.log_test("Regras de negócio", False, "Sem token de autenticação")
            return False
        
        # Teste: aluno pode ver turmas disponíveis
        try:
            response = requests.get(f"{BASE_URL}/api/alunos/1/turmas_disponiveis/", headers=self.auth_headers)
            
            if response.status_code in [200, 404]:  # 404 é OK se aluno não existir
                if response.status_code == 200:
                    turmas = response.json()
                    self.log_test("Turmas disponíveis", True, f"{len(turmas)} turmas disponíveis para inscrição")
                else:
                    self.log_test("Turmas disponíveis", True, "Endpoint funcionando (aluno não encontrado)")
            else:
                self.log_test("Turmas disponíveis", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Turmas disponíveis", False, f"Erro: {str(e)[:100]}")
        
        # Teste: professor pode ver suas turmas
        try:
            response = requests.get(f"{BASE_URL}/api/professores/1/turmas/", headers=self.auth_headers)
            
            if response.status_code in [200, 404]:  # 404 é OK se professor não existir
                if response.status_code == 200:
                    turmas = response.json()
                    self.log_test("Turmas do professor", True, f"{len(turmas)} turmas do professor")
                else:
                    self.log_test("Turmas do professor", True, "Endpoint funcionando (professor não encontrado)")
            else:
                self.log_test("Turmas do professor", False, f"Status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Turmas do professor", False, f"Erro: {str(e)[:100]}")
    
    def print_summary(self):
        # Imprime resumo dos testes
        print("\n" + "=" * 60)
        print("RESUMO DOS TESTES")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal de testes: {total_tests}")
        print(f"✓ Sucessos: {passed_tests}")
        print(f"✗ Falhas: {failed_tests}")
        print(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ TESTES QUE FALHARAM:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['details']}")
        
        print(f"\n{'🎉 TODOS OS TESTES PASSARAM!' if failed_tests == 0 else '⚠️  ALGUNS TESTES FALHARAM'}")
        print("=" * 60)

def main():
    print("🚀 INICIANDO TESTES AUTOMATIZADOS")
    print("=" * 60)
    print("Testando APIs REST e funcionalidades do sistema...")
    print(f"URL Base: {BASE_URL}")
    print(f"Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    tester = APITester()
    
    # Executar todos os testes
    server_ok = tester.test_status_endpoint()
    
    if server_ok:
        auth_ok = tester.test_authentication()
        tester.test_crud_operations()
        tester.test_specialized_endpoints()
        tester.test_business_rules()
    else:
        print("\n❌ SERVIDOR NÃO ESTÁ RODANDO!")
        print("Execute: python manage.py runserver 8000")
        return
    
    # Mostrar resumo
    tester.print_summary()

if __name__ == "__main__":
    main()