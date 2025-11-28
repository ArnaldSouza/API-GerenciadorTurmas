from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir que apenas donos de um objeto possam editá-lo.
    """
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura para qualquer requisição
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissões de escrita apenas para o dono do objeto
        return obj.owner == request.user

class IsProfessorOrReadOnly(permissions.BasePermission):
    """
    Permissão para professores criarem turmas
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.tipo_usuario == 'professor'

class IsAluno(permissions.BasePermission):
    """
    Permissão para alunos
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'aluno'

class IsProfessor(permissions.BasePermission):
    """
    Permissão para professores
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'professor'