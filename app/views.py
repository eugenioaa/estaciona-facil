from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db.models import Avg
from django.core.serializers import serialize
from django.contrib import messages
from django.http import JsonResponse
from .models import Bairro
from django.http import JsonResponse
from django.db.models import Avg, F
from .models import Estacionamento, Bairro
from .models import Estacionamento, Avaliacao, HistoricoOcupacao, Usuario
from unidecode import unidecode
from django.http import JsonResponse
from .models import HistoricoOcupacao


# --- Views do Mapa e Páginas Principais ---

def mapa_interativo(request):
    """
    View que busca todos os estacionamentos com coordenadas válidas
    e os envia para o template, incluindo a avaliação mais recente e outros detalhes.
    """
    estacionamentos_com_coordenadas = Estacionamento.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    )

    estacionamentos_list = []
    for est in estacionamentos_com_coordenadas:
        # Busca a avaliação mais recente que tenha um comentário
        latest_review = Avaliacao.objects.filter(
            estacionamento=est, 
            comentario__isnull=False
        ).exclude(comentario='').order_by('-data_avaliacao').first()

        review_data = None
        if latest_review:
            review_data = {
                'comentario': latest_review.comentario,
                'media_avaliacao': latest_review.media_avaliacao(),
                'usuario': latest_review.usuario.username if latest_review.usuario else "Anônimo",
                'data_avaliacao': latest_review.data_avaliacao.strftime('%d/%m/%Y')
            }

        estacionamentos_list.append({
            'id': est.pk,
            'nome': est.nome,
            'endereco': est.endereco,
            'latitude': est.latitude,
            'longitude': est.longitude,
            'imagem_url': est.imagem_url, # Adicionado
            'horario_abertura': est.horario_abertura.strftime('%H:%M') if est.horario_abertura else 'N/A', # Adicionado
            'horario_fechamento': est.horario_fechamento.strftime('%H:%M') if est.horario_fechamento else 'N/A', # Adicionado
            'preco_por_hora': float(est.preco_por_hora) if est.preco_por_hora is not None else None, # Adicionado
            'latest_review': review_data, # Adicionado
        })
    
    context = {
        'estacionamentos_list': estacionamentos_list,
    }
    return render(request, 'app/mapa_interativo.html', context)

# NOVA VIEW PARA A API DE BUSCA DE ESTACIONAMENTOS
def search_estacionamentos(request):
    query = request.GET.get('q', '').strip()
    query_unaccented = unidecode(query)

    estacionamentos_list = []
    if query:
        todos_estacionamentos = Estacionamento.objects.filter(latitude__isnull=False, longitude__isnull=False)
        resultados = [e for e in todos_estacionamentos if query_unaccented.lower() in unidecode(e.nome).lower()]

        for est in resultados[:10]:
            estacionamentos_list.append({
                'id': est.pk, 
                'nome': est.nome,
                'lat': est.latitude,
                'lng': est.longitude
            })
    
    return JsonResponse(estacionamentos_list, safe=False)

def tela_principal(request):
    ultimas_avaliacoes = Avaliacao.objects.filter(comentario__isnull=False).exclude(comentario='').order_by('-id')[:5]
    context = {"ultimas_avaliacoes": ultimas_avaliacoes}
    return render(request, "app/telaprincipal.html", context)

def historico(request):
    historico_list = HistoricoOcupacao.objects.all()
    context = {'historico_list': historico_list}
    return render(request, 'app/historico.html', context)

# --- Views de Avaliação ---

def tela_avaliacoes(request):
    from .forms import AvaliacaoForm # Importação Local

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
            medias = avaliacoes.aggregate(
                media_seg=Avg("nota_seguranca"),
                media_prat=Avg("nota_praticidade"),
                media_pre=Avg("nota_preco"),
                media_disp=Avg("nota_disponibilidade")
            )
            media_seguranca = render_estrelas(medias["media_seg"])
            media_praticidade = render_estrelas(medias["media_prat"])
            media_preco = render_estrelas(medias["media_pre"])
            media_disponibilidade = render_estrelas(medias["media_disp"])

    if request.method == "POST":
        # Necessário re-buscar o estacionamento no POST
        estacionamento = get_object_or_404(Estacionamento, id=request.POST.get("estacionamento_id"))
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.estacionamento = estacionamento
            if request.user.is_authenticated:
                avaliacao.usuario = request.user
            avaliacao.save()
            return redirect(f"{request.path}?estac_id={estacionamento.id}")

    context = {
        "estacionamentos": estacionamentos, "estacionamento": estacionamento, "avaliacoes": avaliacoes,
        "media_seguranca": media_seguranca, "media_praticidade": media_praticidade,
        "media_preco": media_preco, "media_disponibilidade": media_disponibilidade,
        "avaliacao_form": form,
    }
    return render(request, "app/telaAval.html", context)


def render_estrelas(media):
    if media is None:
        return "☆☆☆☆☆"
    arred = round(media)
    return "★" * arred + "☆" * (5 - arred)

# --- Views de Autenticação e Registo ---

def registro_usuario(request):
    from .forms import UsuarioRegistrationForm # Importação Local

    if request.method == 'POST':
        form = UsuarioRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Por favor, faça o login.')
            return redirect("app:login")
        else:
            print("ERROS NO FORMULÁRIO DE REGISTRO:", form.errors.as_json())
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = UsuarioRegistrationForm()
        
    return render(request, "app/registroUser.html", {"form": form})

def registro_estacionamento(request):
    from .forms import EstacionamentoForm # Importação Local
    if request.method == 'POST':
        form = EstacionamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Estacionamento registrado com sucesso!')
            return redirect("app:tela_principal")
    else:
        form = EstacionamentoForm()
    return render(request, "app/registroEstacionamento.html", {"form": form})


def login_usuario(request):
    from .forms import LoginForm # Importação Local

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('app:tela_principal')
            else:
                messages.error(request, 'Utilizador ou senha inválidos.')
    else:
        form = LoginForm()
        
    return render(request, 'app/login.html', {'form': form})


def logout_usuario(request):
    logout(request)
    return redirect('app:tela_principal')

# --- Views de Gestão de Conta ---

@login_required
def editar_usuario(request):
    from django.contrib.auth.forms import UserChangeForm

    class CustomUserChangeForm(UserChangeForm):
        class Meta(UserChangeForm.Meta):
            model = Usuario
            fields = ('username', 'email', 'lugar_mora', 'vehicle_type')

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('app:editar_usuario')
    else:
        form = CustomUserChangeForm(instance=request.user)
        
    return render(request, 'app/editarUser.html', {'form': form})



@login_required
def deletar_usuario(request):
    if request.method == 'POST':
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, 'Sua conta foi deletada com sucesso.')
        return redirect('app:tela_principal')
        
    return render(request, 'app/deletar_usuario.html')

# NOVA VERSÃO DA VIEW PARA A API DE BUSCA
def search_bairros(request):
    query = request.GET.get('q', '').strip()
    query_unaccented = unidecode(query) # Converte o termo da busca para sem acentos

    bairros_list = []
    if query:
        # Busca todos os bairros e filtra em Python (melhor para lidar com acentos)
        todos_bairros = Bairro.objects.all()
        # Compara a versão sem acentos do nome do bairro com a busca
        resultados = [b for b in todos_bairros if query_unaccented.lower() in unidecode(b.nome).lower()]
        
        for bairro in resultados[:10]: # Limita a 10 resultados
            bairros_list.append({'id': bairro.id, 'nome': bairro.nome})
    
    return JsonResponse(bairros_list, safe=False)

@login_required
def simulador_demanda(request, estacionamento_id):
    estacionamento_principal = get_object_or_404(Estacionamento, pk=estacionamento_id)
    
    # Prepara os dados de TODOS os estacionamentos para a grade
    estacionamentos_qs = Estacionamento.objects.all().order_by('id')
    
    todos_estacionamentos = []
    for est in estacionamentos_qs:
        todos_estacionamentos.append({
            'id': est.id,
            'nome': est.nome,
            'endereco': est.endereco,
            'imagem_url': est.imagem_url,
            # Usa um preço muito alto para nulos, para que fiquem por último na ordenação
            'preco_por_hora': est.preco_por_hora if est.preco_por_hora is not None else 999.0
        })
        
    context = {
        'estacionamento_principal': estacionamento_principal,
        'todos_estacionamentos': todos_estacionamentos,
    }
    
    return render(request, 'app/simulador.html', context)