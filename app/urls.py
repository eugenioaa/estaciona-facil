from django.urls import path
from .views import historico_ocupacao_view

urlpatterns = [
    path('historico/', historico_ocupacao_view, name='historico'),
]