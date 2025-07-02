from django.contrib import admin
from .models import Estacionamento, HistoricoOcupacao, Avaliacao, Usuario

# --- Classe de personalização para o Admin do Estacionamento ---
class EstacionamentoAdmin(admin.ModelAdmin):
    # CORRIGIDO: Usando 'endereco', que existe no seu modelo, 
    # em vez de 'capacidade_total'
    list_display = ('nome', 'endereco')

# --- Classe de personalização para o Admin do Historico ---
class HistoricoOcupacaoAdmin(admin.ModelAdmin):
    list_display = ('estacionamento', 'vagas_ocupadas', 'timestamp')
    list_filter = ('estacionamento', 'timestamp')


# --- Seus registros originais, agora corrigidos e sem duplicatas ---

admin.site.register(Estacionamento, EstacionamentoAdmin) 

admin.site.register(HistoricoOcupacao, HistoricoOcupacaoAdmin)

admin.site.register(Avaliacao)
admin.site.register(Usuario)