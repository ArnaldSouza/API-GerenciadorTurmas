# API Gerenciador de Turmas

## Integrantes do Grupo
- **Arnald Souza** - 236114
- **Bruno Targa** - 211702
- **Christopher Kevin Teixeira Costa** - 211660
- **Gabriel Henrique Vieira de Oliveira** - 210394
- **Matheus Parizotto Martins** - 211067
- **Victor Soares Nunes Pires de Oliveira** - 223585

## O que é?
Sistema de gerenciamento acadêmico que permite:
- Cadastrar alunos, professores e matérias
- Criar turmas e fazer inscrições
- Gerenciar horários e controlar vagas

## Como funciona?
O sistema oferece **duas APIs**:
- **REST API** (JSON) - Para frontends web/mobile
- **gRPC API** - Para comunicação entre serviços

Ambas fazem as mesmas operações: criar, listar, atualizar e deletar dados.

## Como rodar?

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar banco
```bash
python manage.py migrate
python populate_data.py  # dados de exemplo
```

### 3. Iniciar servidor REST
```bash
python manage.py runserver
```
API disponível em: http://localhost:8000/

### 4. Iniciar servidor gRPC (opcional)
```bash
cd grpc
python gerenciador_grpc_server.py
```

## Exemplo de uso
```bash
# Listar alunos
GET http://localhost:8000/api/alunos/

# Criar aluno
POST http://localhost:8000/api/alunos/
{
  "nome": "João Silva",
  "matricula": "141414",
  "email": "joao@exemplo.com"
}

# Inscrever aluno em turma
POST http://localhost:8000/api/alunos/1/inscrever_turma/
{
  "turma_id": 1
}
```

## Tecnologias
Django + Django REST Framework + gRPC + SQLite

---

## Documentação Técnica Completa

### Padrão de Respostas

Todas as respostas seguem um padrão consistente:

### Sucesso (2xx)
```json
{
  "success": true,
  "data": {}, // Dados da resposta
  "message": "Operação realizada com sucesso", // Opcional
  "meta": {
    "status_code": 200,
    "timestamp": "2025-11-29T10:30:00.000Z",
    "endpoint": "/api/endpoint",
    "method": "GET",
    "resource_type": "alunos",
    "total_count": 150 // Para listagens
  }
}
```

### Erro (4xx/5xx)
```json
{
  "success": false,
  "message": "Mensagem do erro",
  "error_code": "VALIDATION_ERROR",
  "errors": {}, // Detalhes específicos do erro
  "meta": {
    "status_code": 400,
    "timestamp": "2025-11-29T10:30:00.000Z",
    "endpoint": "/api/endpoint",
    "method": "POST"
  }
}
```

### Paginação
```json
{
  "success": true,
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_pages": 5,
    "total_count": 100,
    "has_next": true,
    "has_previous": false,
    "next_url": "/api/alunos/?page=2",
    "previous_url": null
  },
  "meta": {}
}
```

## Headers CORS

A API inclui headers CORS permissivos para qualquer origem:

- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: GET, POST, PUT, PATCH, DELETE, OPTIONS`
- `Access-Control-Allow-Headers: Accept, Content-Type, Authorization, X-Requested-With, X-CSRFToken, X-API-Key, Cache-Control`
- `Access-Control-Expose-Headers: Content-Length, X-Total-Count, X-Page-Count`

## Autenticação

### Token Authentication
```bash
# Obter token
POST /api/auth/login/
{
  "username": "usuario",
  "password": "senha"
}

# Resposta
{
  "success": true,
  "data": {
    "token": "abc123...",
    "user": {
      "id": 1,
      "username": "usuario",
      "tipo_usuario": "aluno"
    }
  }
}

# Usar token
Authorization: Token abc123...
```

## Endpoints Principais

### 1. Status da API
```
GET /api/status/
```
Verifica se a API está funcionando.

### 2. Alunos
```
GET    /api/alunos/              # Listar alunos
POST   /api/alunos/              # Criar aluno
GET    /api/alunos/{id}/         # Obter aluno
PUT    /api/alunos/{id}/         # Atualizar aluno
DELETE /api/alunos/{id}/         # Deletar aluno

# Ações específicas
GET    /api/alunos/dropdown/     # Lista para dropdown
GET    /api/alunos/dashboard/    # Resumo para dashboard
GET    /api/alunos/{id}/turmas/  # Turmas do aluno
POST   /api/alunos/{id}/inscrever_turma/  # Inscrever em turma
POST   /api/alunos/{id}/cancelar_inscricao/  # Cancelar inscrição
```

### 3. Professores
```
GET    /api/professores/         # Listar professores
POST   /api/professores/         # Criar professor
GET    /api/professores/{id}/    # Obter professor
PUT    /api/professores/{id}/    # Atualizar professor
DELETE /api/professores/{id}/    # Deletar professor

# Ações específicas
GET    /api/professores/{id}/turmas/     # Turmas do professor
POST   /api/professores/{id}/criar_turma/  # Criar nova turma
```

### 4. Matérias
```
GET    /api/materias/            # Listar matérias
POST   /api/materias/            # Criar matéria
GET    /api/materias/{id}/       # Obter matéria
PUT    /api/materias/{id}/       # Atualizar matéria
DELETE /api/materias/{id}/       # Deletar matéria
```

### 5. Turmas
```
GET    /api/turmas/              # Listar turmas
POST   /api/turmas/              # Criar turma
GET    /api/turmas/{id}/         # Obter turma
PUT    /api/turmas/{id}/         # Atualizar turma
DELETE /api/turmas/{id}/         # Deletar turma

# Ações específicas
GET    /api/turmas/{id}/alunos/  # Alunos da turma
```

### 6. Dashboard
```
GET    /api/dashboard/           # Dashboard geral
```

## Códigos de Status HTTP

- `200 OK` - Operação bem-sucedida
- `201 Created` - Recurso criado com sucesso
- `204 No Content` - Operação bem-sucedida sem conteúdo
- `400 Bad Request` - Dados inválidos
- `401 Unauthorized` - Não autorizado
- `403 Forbidden` - Acesso negado
- `404 Not Found` - Recurso não encontrado
- `409 Conflict` - Conflito de dados
- `422 Unprocessable Entity` - Dados válidos mas não processáveis
- `500 Internal Server Error` - Erro interno do servidor

## Códigos de Erro Customizados

- `VALIDATION_ERROR` - Erro de validação de dados
- `ALREADY_ENROLLED` - Aluno já inscrito na turma
- `TURMA_NOT_FOUND` - Turma não encontrada
- `MATERIA_NOT_FOUND` - Matéria não encontrada
- `UNAUTHORIZED_ACCESS` - Acesso não autorizado
- `DUPLICATE_ENTRY` - Entrada duplicada

## Paginação

Use os parâmetros `page` e `page_size`:
```
GET /api/alunos/?page=2&page_size=10
```

Headers de resposta incluem:
- `X-Total-Count` - Total de itens
- `X-Has-Next` - Se há próxima página
- `X-Has-Previous` - Se há página anterior

## Filtros e Busca

Use parâmetros de query para filtros:
```
GET /api/alunos/?nome=João&matricula=2024
GET /api/turmas/?professor=1&materia=2
```

## Exemplos de Uso

### Frontend JavaScript/TypeScript
```javascript
// Cliente genérico
class APIClient {
  constructor(baseURL, token = null) {
    this.baseURL = baseURL;
    this.token = token;
  }

  async request(endpoint, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...(this.token && { Authorization: `Token ${this.token}` }),
      ...options.headers
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, {
      ...options,
      headers
    });

    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.message);
    }
    
    return data;
  }
}

// Uso
const client = new APIClient('http://localhost:8000/api', 'your-token');

// Listar alunos
const alunos = await client.request('/alunos/');

// Criar aluno
const novoAluno = await client.request('/alunos/', {
  method: 'POST',
  body: JSON.stringify({
    nome: 'João Silva',
    matricula: '2024001',
    email: 'joao@exemplo.com'
  })
});
```

### React Hook
```jsx
import { useState, useEffect } from 'react';

function useAPI(endpoint, dependencies = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function fetchData() {
      try {
        setLoading(true);
        const response = await client.request(endpoint);
        setData(response.data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }
    
    fetchData();
  }, dependencies);

  return { data, loading, error };
}

// Uso no componente
function AlunosList() {
  const { data: alunos, loading, error } = useAPI('/alunos/');
  
  if (loading) return <div>Carregando...</div>;
  if (error) return <div>Erro: {error}</div>;
  
  return (
    <ul>
      {alunos.map(aluno => (
        <li key={aluno.id}>{aluno.nome}</li>
      ))}
    </ul>
  );
}
```

## Considerações de Produção

1. **CORS**: Configure `ALLOWED_HOSTS` adequadamente
2. **HTTPS**: Use sempre HTTPS em produção
3. **Rate Limiting**: Implemente rate limiting conforme necessário
4. **Cache**: Configure cache para endpoints que não mudam frequentemente
5. **Logs**: Implemente logging apropriado
6. **Monitoramento**: Configure health checks e métricas