# Caminho: hello_world/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 1. URL para a área de administração
    path('admin/', admin.site.urls),
    
    # 2. URL para o Django Browser Reload (se estiver a usar)
    path("__reload__/", include("django_browser_reload.urls")),

    # 3. INCLUI TODAS AS URLS DA SUA APLICAÇÃO 'app'
    # Esta é a única linha necessária para conectar a sua app.
    path('', include('app.urls')),
]

# Adiciona URLs para servir ficheiros estáticos e de media em modo de desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)