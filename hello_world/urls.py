# hello_world/urls.py - VERSÃO FINAL E CORRIGIDA

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from app.views import logout_view, telaPrincipal, register_view, register_estacionamento_view, login_view, sistemaAval, editar_usuario_view, deletar_usuario_view


# --- Bloco 1: Inicia a nossa lista de URLs ---
urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')), # A URL do nosso histórico está aqui
]


# --- Bloco 2: ADICIONA as outras URLs à lista já existente ---

# 2. CORREÇÃO FINAL: Usamos "+=" para ADICIONAR, e não substituir.
urlpatterns += [
    path("", telaPrincipal, name="tela_principal"),
    path("aval/", sistemaAval, name="sistema_avaliacao"),
    path("registrarUsuario/", register_view, name="register"),
    path("registroEstacionamento/", register_estacionamento_view, name="register_estacionamento"),
    path("login/", login_view, name="login"),
    path('editar/', editar_usuario_view, name='editar_usuario'),
    path('deletar/', deletar_usuario_view, name='deletar_usuario'),
    path('logout/', logout_view, name='logout'),
    # Se você tiver a URL "__reload__/", pode adicioná-la aqui
    path("__reload__/", include("django_browser_reload.urls")),
]


# --- Bloco 3: Adiciona URLs para arquivos estáticos (em modo de teste) ---
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)