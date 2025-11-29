from django.urls import path
from . import views

urlpatterns = [
    path('api/dashboard/', views.dashboard_geral, name='dashboard_geral'),
    path('api/status/', views.status_api, name='status_api'),
]