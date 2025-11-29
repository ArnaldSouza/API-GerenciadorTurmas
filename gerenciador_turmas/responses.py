from rest_framework import serializers
from datetime import datetime

class StandardResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField(required=False, allow_blank=True)
    data = serializers.JSONField(required=False)
    errors = serializers.JSONField(required=False)
    meta = serializers.JSONField(required=False)

class MetaSerializer(serializers.Serializer):
    status_code = serializers.IntegerField()
    timestamp = serializers.DateTimeField(default=datetime.now)
    endpoint = serializers.CharField()
    method = serializers.CharField()
    resource_type = serializers.CharField(required=False)
    total_count = serializers.IntegerField(required=False)
    page_count = serializers.IntegerField(required=False)
    current_page = serializers.IntegerField(required=False)

class PaginatedResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    data = serializers.JSONField()
    pagination = serializers.JSONField()
    meta = serializers.JSONField()

class ErrorSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=False)
    message = serializers.CharField()
    error_code = serializers.CharField(required=False)
    errors = serializers.JSONField(required=False)
    meta = serializers.JSONField()

class HealthCheckSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True)
    message = serializers.CharField(default="API funcionando corretamente")
    data = serializers.JSONField()
    meta = serializers.JSONField()

# Utility functions para criar respostas padronizadas
def create_success_response(data=None, message=None, meta=None):
    response = {
        'success': True,
        'data': data,
        'meta': meta or {}
    }
    
    if message:
        response['message'] = message
    
    return response

def create_error_response(message, error_code=None, errors=None, meta=None):
    response = {
        'success': False,
        'message': message,
        'meta': meta or {}
    }
    
    if error_code:
        response['error_code'] = error_code
    
    if errors:
        response['errors'] = errors
    
    return response

def create_paginated_response(data, pagination_info, meta=None):
    return {
        'success': True,
        'data': data,
        'pagination': {
            'page': pagination_info.get('page', 1),
            'page_size': pagination_info.get('page_size', 20),
            'total_pages': pagination_info.get('total_pages', 1),
            'total_count': pagination_info.get('total_count', 0),
            'has_next': pagination_info.get('has_next', False),
            'has_previous': pagination_info.get('has_previous', False),
            'next_url': pagination_info.get('next_url'),
            'previous_url': pagination_info.get('previous_url')
        },
        'meta': meta or {}
    }