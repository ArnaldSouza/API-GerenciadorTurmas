from rest_framework import permissions

# Permissão customizada para permitir que apenas donos de um objeto possam editá-lo.
class IsOwnerOrReadOnly(permissions.BasePermission):
      
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura para qualquer requisição
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Permissões de escrita apenas para o dono do objeto
        return obj.owner == request.user

# Permissão para professores criarem turmas
class IsProfessorOrReadOnly(permissions.BasePermission):   
        
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.tipo_usuario == 'professor'

# Permissão para alunos
class IsAluno(permissions.BasePermission):
       
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'aluno'

# Permissão para professores
class IsProfessor(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo_usuario == 'professor'