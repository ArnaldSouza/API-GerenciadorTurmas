from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status as http_status
import json
from datetime import datetime

class StandardResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Processar respostas JSON da API
        if (request.path.startswith('/api/') and 
            hasattr(response, 'data') and 
            isinstance(response, Response)):
            
            # Se a resposta já tem o padrão, manter
            if isinstance(response.data, dict) and 'success' in response.data:
                return response
            
            # Padronizar resposta de sucesso
            if 200 <= response.status_code < 300:
                standardized_data = {
                    'success': True,
                    'data': response.data,
                    'meta': {
                        'status_code': response.status_code,
                        'timestamp': datetime.now().isoformat(),
                        'endpoint': request.path,
                        'method': request.method
                    }
                }
                response.data = standardized_data
            
            # Padronizar resposta de erro
            elif response.status_code >= 400:
                error_data = response.data if hasattr(response, 'data') else {}
                standardized_data = {
                    'success': False,
                    'message': self._get_error_message(response.status_code, error_data),
                    'errors': error_data,
                    'meta': {
                        'status_code': response.status_code,
                        'timestamp': datetime.now().isoformat(),
                        'endpoint': request.path,
                        'method': request.method,
                        'error_code': self._get_error_code(response.status_code)
                    }
                }
                response.data = standardized_data
        
        return response
    
    def _get_error_message(self, status_code, error_data):
        messages = {
            400: 'Requisição inválida',
            401: 'Não autorizado',
            403: 'Acesso negado', 
            404: 'Recurso não encontrado',
            405: 'Método não permitido',
            409: 'Conflito de dados',
            422: 'Dados inválidos',
            500: 'Erro interno do servidor'
        }
        
        # Se há uma mensagem customizada, usar ela
        if isinstance(error_data, dict):
            if 'message' in error_data:
                return error_data['message']
            elif 'detail' in error_data:
                return error_data['detail']
        
        return messages.get(status_code, f'Erro HTTP {status_code}')
    
    def _get_error_code(self, status_code):
        codes = {
            400: 'BAD_REQUEST',
            401: 'UNAUTHORIZED', 
            403: 'FORBIDDEN',
            404: 'NOT_FOUND',
            405: 'METHOD_NOT_ALLOWED',
            409: 'CONFLICT',
            422: 'UNPROCESSABLE_ENTITY',
            500: 'INTERNAL_SERVER_ERROR'
        }
        return codes.get(status_code, f'HTTP_{status_code}')

class CORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Headers CORS genéricos para qualquer frontend
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
        response['Access-Control-Allow-Headers'] = (
            'Accept, Content-Type, Authorization, X-Requested-With, '
            'X-CSRFToken, X-API-Key, Cache-Control'
        )
        response['Access-Control-Expose-Headers'] = (
            'Content-Length, X-Total-Count, X-Page-Count'
        )
        response['Access-Control-Max-Age'] = '86400'
        
        return response

class PaginationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Adicionar headers de paginação se disponível
        if (hasattr(response, 'data') and 
            isinstance(response.data, dict) and
            'results' in response.data):
            
            if 'count' in response.data:
                response['X-Total-Count'] = str(response.data['count'])
            
            if 'next' in response.data and response.data['next']:
                response['X-Has-Next'] = 'true'
            else:
                response['X-Has-Next'] = 'false'
                
            if 'previous' in response.data and response.data['previous']:
                response['X-Has-Previous'] = 'true'
            else:
                response['X-Has-Previous'] = 'false'
        
        return response