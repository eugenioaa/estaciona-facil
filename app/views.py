# Imports organizados e corrigidos
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db.models import Avg
from django.core.serializers import serialize

from .forms import AvaliacaoForm, UsuarioRegistrationForm, EstacionamentoForm, LoginForm
from .models import Estacionamento, Avaliacao, HistoricoOcupacao

# --- Views do Mapa e Páginas Principais ---

def mapa_interativo(request):
    """
    View que busca todos os estacionamentos com coordenadas válidas
    e os envia para o template do mapa de forma segura (JSON).
    """
    estacionamentos_com_coordenadas = Estacionamento.objects.filter(
        latitude__isnull=False, 
        longitude__isnull=False
    )
    # CORRIGIDO: Serializa os dados para o formato JSON para usar com json_script
    estacionamentos_json = serialize('json', estacionamentos_com_coordenadas)
    
    context = {
        'estacionamentos_json': estacionamentos_json,
    }
    return render(request, 'app/mapa_interativo.html', context)

# Caminho: app/views.py

def tela_principal(request):
    """
    Exibe a página principal com as últimas 5 avaliações.
    """
    ultimas_avaliacoes = Avaliacao.objects.filter(comentario__isnull=False).exclude(comentario='').order_by('-id')[:5]
    context = {
        "ultimas_avaliacoes": ultimas_avaliacoes
    }
    # CORRIGIDO: O nome do ficheiro agora está em minúsculas, como no seu projeto.
    return render(request, "app/telaprincipal.html", context)

def historico(request):
    """
    Exibe o histórico de ocupação.
    """
    historico_list = HistoricoOcupacao.objects.all()
    context = {
        'historico_list': historico_list
    }
    # CORRIGIDO: Caminho do template com o namespace 'app'
    return render(request, 'app/historico.html', context)

# --- Views de Avaliação ---

def tela_avaliacoes(request):
    """
    Página para ver e submeter avaliações de um estacionamento.
    """
    estacionamentos = Estacionamento.objects.all()
    estac_id = request.GET.get("estac_id")
    estacionamento = None
    avaliacoes = []
    media_seguranca = media_praticidade = media_preco = media_disponibilidade = ''
    form = AvaliacaoForm()

    if estac_id:
        estacionamento = get_object_or_404(Estacionamento, id=estac_id)
        avaliacoes = Avaliacao.objects.filter(estacionamento=estacionamento)

        if avaliacoes.exists():
            media_seguranca = render_estrelas(avaliacoes.aggregate(Avg("nota_seguranca"))["nota_seguranca__avg"])
            media_praticidade = render_estrelas(avaliacoes.aggregate(Avg("nota_praticidade"))["nota_praticidade__avg"])
            media_preco = render_estrelas(avaliacoes.aggregate(Avg("nota_preco"))["nota_preco__avg"])
            media_disponibilidade = render_estrelas(avaliacoes.aggregate(Avg("nota_disponibilidade"))["nota_disponibilidade__avg"])

        if request.method == "POST":
            form = AvaliacaoForm(request.POST)
            if form.is_valid():
                avaliacao = form.save(commit=False)
                avaliacao.estacionamento = estacionamento
                if request.user.is_authenticated:
                    avaliacao.usuario = request.user
                avaliacao.save()
                # CORRIGIDO: Redirecionamento para a mesma página de forma segura
                return redirect(f"{request.path}?estac_id={estac_id}")

    context = {
        "estacionamentos": estacionamentos, "estacionamento": estacionamento, "avaliacoes": avaliacoes,
        "media_seguranca": media_seguranca, "media_praticidade": media_praticidade,
        "media_preco": media_preco, "media_disponibilidade": media_disponibilidade,
        "avaliacao_form": form,
    }
    return render(request, "app/telaAval.html", context)

def render_estrelas(media):
    """Função auxiliar para renderizar a média de notas como estrelas."""
    if media is None:
        return "☆☆☆☆☆"
    arred = round(media)
    return "★" * arred + "☆" * (5 - arred)

# --- Views de Autenticação e Registo ---

def registro_usuario(request):
    form = UsuarioRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        # CORRIGIDO: Redirecionamento usando o nome da URL
        return redirect("app:login")
    return render(request, "app/registroUser.html", {"form": form})

def registro_estacionamento(request):
    form = EstacionamentoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("app:tela_principal")
    return render(request, "app/registroEstacionamento.html", {"form": form})

def login_usuario(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('app:tela_principal')
        else:
            form.add_error(None, 'Utilizador ou senha inválidos.')
    return render(request, 'app/login.html', {'form': form})

def logout_usuario(request):
    logout(request)
    return redirect('app:tela_principal')

# --- Views de Gestão de Conta ---

@login_required
def editar_usuario(request):
    user = request.user
    if request.method == 'POST':
        form = UsuarioRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('app:tela_principal')
    else:
        form = UsuarioRegistrationForm(instance=user)
    return render(request, 'app/editarUser.html', {'form': form})

@login_required
def deletar_usuario(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        return redirect('app:tela_principal')
    return render(request, 'app/deletar_usuario.html')