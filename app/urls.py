# Caminho: app/urls.py

from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # Páginas principais
    path('', views.tela_principal, name='tela_principal'),
    path('mapa/', views.mapa_interativo, name='mapa_interativo'),
    path('avaliacoes/', views.tela_avaliacoes, name='tela_avaliacoes'),
    path('historico/', views.historico, name='historico'),

    # Autenticação e Registo
    path('login/', views.login_usuario, name='login'),
    path('logout/', views.logout_usuario, name='logout'),
    path('registro/', views.registro_usuario, name='registro_usuario'),
    path('registro/estacionamento/', views.registro_estacionamento, name='registro_estacionamento'),

    # Gestão de Conta
    path('conta/editar/', views.editar_usuario, name='editar_usuario'),
    path('conta/deletar/', views.deletar_usuario, name='deletar_usuario'),
]