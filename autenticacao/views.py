from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """Registra um novo usuário"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'message': 'Usuário criado com sucesso',
            'user': UserProfileSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    """Autentica um usuário"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'message': 'Login realizado com sucesso',
            'user': UserProfileSerializer(user).data,
            'token': token.key
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_view(request):
    """Desloga um usuário"""
    try:
        request.user.auth_token.delete()
        logout(request)
        return Response({'message': 'Logout realizado com sucesso'})
    except:
        return Response({'error': 'Erro ao fazer logout'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def profile(request):
    """Retorna perfil do usuário logado"""
    serializer = UserProfileSerializer(request.user)
    return Response(serializer.data)
