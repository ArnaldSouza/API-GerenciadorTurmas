from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'tipo_usuario', 'is_active', 'date_joined']
    list_filter = ['tipo_usuario', 'is_active', 'date_joined']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )
