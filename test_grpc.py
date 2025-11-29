"""
Teste da comunicação gRPC
Este script testa o servidor gRPC e suas funcionalidades
"""
import grpc
import sys
import os

# Adicionar o diretório grpc ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'grpc'))

try:
    import gerenciador_pb2
    import gerenciador_pb2_grpc
except ImportError as e:
    print(f"❌ Erro ao importar arquivos gRPC: {e}")
    print("Certifique-se de que os arquivos .proto foram compilados:")
    print("cd grpc")
    print("python -m grpc_tools.protoc --python_out=. --grpc_python_out=. gerenciador.proto")
    sys.exit(1)

class GRPCTester:
    def __init__(self):
        self.channel = None
        self.stub = None
        self.test_results = []
    
    def log_test(self, test_name, success, details=""):
        """Registra resultado do teste"""
        result = {
            'test': test_name,
            'success': success,
            'details': details
        }
        self.test_results.append(result)
        
        status = "✓" if success else "✗"
        print(f"{status} {test_name}: {details}")
    
    def connect_to_server(self):
        """Conecta ao servidor gRPC"""
        try:
            self.channel = grpc.insecure_channel('localhost:50051')
            self.stub = gerenciador_pb2_grpc.GerenciadorTurmasStub(self.channel)
            
            # Teste de conexão
            grpc.channel_ready_future(self.channel).result(timeout=5)
            self.log_test("Conexão gRPC", True, "Conectado ao servidor gRPC na porta 50051")
            return True
            
        except Exception as e:
            self.log_test("Conexão gRPC", False, f"Erro de conexão: {str(e)[:100]}")
            return False
    
    def test_criar_aluno(self):
        """Teste: Criar aluno via gRPC"""
        try:
            request = gerenciador_pb2.CriarAlunoRequest(
                nome="Aluno gRPC Teste",
                matricula="GRPC2024001",
                email="grpc_aluno@teste.com"
            )
            
            response = self.stub.CriarAluno(request, timeout=10)
            
            if response.sucesso:
                self.log_test("Criar aluno gRPC", True, f"Aluno criado: ID {response.aluno.id}")
                return response.aluno.id
            else:
                self.log_test("Criar aluno gRPC", False, f"Erro: {response.mensagem}")
                return None
                
        except Exception as e:
            self.log_test("Criar aluno gRPC", False, f"Erro: {str(e)[:100]}")
            return None
    
    def test_listar_alunos(self):
        """Teste: Listar alunos via gRPC"""
        try:
            request = gerenciador_pb2.Empty()
            response = self.stub.ListarAlunos(request, timeout=10)
            
            self.log_test("Listar alunos gRPC", True, f"{len(response.alunos)} alunos encontrados")
            return len(response.alunos)
            
        except Exception as e:
            self.log_test("Listar alunos gRPC", False, f"Erro: {str(e)[:100]}")
            return 0
    
    def test_criar_professor(self):
        """Teste: Criar professor via gRPC"""
        try:
            request = gerenciador_pb2.CriarProfessorRequest(
                nome="Professor gRPC Teste",
                email="grpc_professor@teste.com"
            )
            
            response = self.stub.CriarProfessor(request, timeout=10)
            
            if response.sucesso:
                self.log_test("Criar professor gRPC", True, f"Professor criado: ID {response.professor.id}")
                return response.professor.id
            else:
                self.log_test("Criar professor gRPC", False, f"Erro: {response.mensagem}")
                return None
                
        except Exception as e:
            self.log_test("Criar professor gRPC", False, f"Erro: {str(e)[:100]}")
            return None
    
    def test_criar_materia(self):
        """Teste: Criar matéria via gRPC"""
        try:
            request = gerenciador_pb2.CriarMateriaRequest(
                nome="Matéria gRPC Teste",
                descricao="Matéria criada via teste gRPC"
            )
            
            response = self.stub.CriarMateria(request, timeout=10)
            
            if response.sucesso:
                self.log_test("Criar matéria gRPC", True, f"Matéria criada: ID {response.materia.id}")
                return response.materia.id
            else:
                self.log_test("Criar matéria gRPC", False, f"Erro: {response.mensagem}")
                return None
                
        except Exception as e:
            self.log_test("Criar matéria gRPC", False, f"Erro: {str(e)[:100]}")
            return None
    
    def test_criar_turma(self, professor_id, materia_id):
        """Teste: Criar turma via gRPC"""
        if not professor_id or not materia_id:
            self.log_test("Criar turma gRPC", False, "Professor ou matéria não disponível")
            return None
            
        try:
            request = gerenciador_pb2.CriarTurmaRequest(
                professor_id=professor_id,
                materia_id=materia_id,
                horario="Teste gRPC - 19:00-21:00"
            )
            
            response = self.stub.CriarTurma(request, timeout=10)
            
            if response.sucesso:
                self.log_test("Criar turma gRPC", True, f"Turma criada: ID {response.turma.id}")
                return response.turma.id
            else:
                self.log_test("Criar turma gRPC", False, f"Erro: {response.mensagem}")
                return None
                
        except Exception as e:
            self.log_test("Criar turma gRPC", False, f"Erro: {str(e)[:100]}")
            return None
    
    def test_inscrever_aluno(self, aluno_id, turma_id):
        """Teste: Inscrever aluno em turma via gRPC"""
        if not aluno_id or not turma_id:
            self.log_test("Inscrever aluno gRPC", False, "Aluno ou turma não disponível")
            return False
            
        try:
            request = gerenciador_pb2.InscreverAlunoRequest(
                aluno_id=aluno_id,
                turma_id=turma_id
            )
            
            response = self.stub.InscreverAluno(request, timeout=10)
            
            if response.sucesso:
                self.log_test("Inscrever aluno gRPC", True, "Aluno inscrito com sucesso")
                return True
            else:
                self.log_test("Inscrever aluno gRPC", False, f"Erro: {response.mensagem}")
                return False
                
        except Exception as e:
            self.log_test("Inscrever aluno gRPC", False, f"Erro: {str(e)[:100]}")
            return False
    
    def close_connection(self):
        """Fecha conexão gRPC"""
        if self.channel:
            self.channel.close()
    
    def print_summary(self):
        """Imprime resumo dos testes gRPC"""
        print("\n" + "=" * 60)
        print("RESUMO DOS TESTES gRPC")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal de testes: {total_tests}")
        print(f"✓ Sucessos: {passed_tests}")
        print(f"✗ Falhas: {failed_tests}")
        print(f"Taxa de sucesso: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ TESTES gRPC QUE FALHARAM:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  - {result['test']}: {result['details']}")
        
        print(f"\n{'🎉 TODOS OS TESTES gRPC PASSARAM!' if failed_tests == 0 else '⚠️  ALGUNS TESTES gRPC FALHARAM'}")

def main():
    print("🔗 INICIANDO TESTES gRPC")
    print("=" * 60)
    print("Testando servidor gRPC e operações...")
    
    tester = GRPCTester()
    
    # Conectar ao servidor
    if not tester.connect_to_server():
        print("\n❌ SERVIDOR gRPC NÃO ESTÁ RODANDO!")
        print("Execute o servidor gRPC:")
        print("cd grpc")
        print("python gerenciador_grpc_server.py")
        return
    
    try:
        # Testes de operações CRUD via gRPC
        print("\n1. TESTANDO OPERAÇÕES CRUD VIA gRPC")
        print("-" * 40)
        
        # Teste completo de fluxo
        aluno_id = tester.test_criar_aluno()
        professor_id = tester.test_criar_professor()
        materia_id = tester.test_criar_materia()
        
        turma_id = tester.test_criar_turma(professor_id, materia_id)
        
        if aluno_id and turma_id:
            tester.test_inscrever_aluno(aluno_id, turma_id)
        
        # Teste de listagem
        tester.test_listar_alunos()
        
    finally:
        tester.close_connection()
    
    tester.print_summary()

if __name__ == "__main__":
    main()