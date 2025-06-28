from django.shortcuts import render, redirect, get_object_or_404
from .forms import AvaliacaoForm, UsuarioRegistrationForm, EstacionamentoForm
from .models import Estacionamento, Avaliacao
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

def telaPrincipal(request):
    return render(request, "telaPrincipal.html")


def sistemaAval(request):
    estacionamentos = Estacionamento.objects.all()
    estac_id = request.GET.get("estac_id")
    estacionamento = None
    avaliacoes = []
    media_seguranca = media_praticidade = media_preco = media_disponibilidade = ''
    form = AvaliacaoForm()

    if estac_id:
        estacionamento = get_object_or_404(Estacionamento, id=estac_id)
        avaliacoes = Avaliacao.objects.filter(estacionamento=estacionamento)

        # Média das notas
        if avaliacoes.exists():
            media_seguranca = render_estrelas(avaliacoes.aggregate(Avg("nota_seguranca"))["nota_seguranca__avg"])
            media_praticidade = render_estrelas(avaliacoes.aggregate(Avg("nota_praticidade"))["nota_praticidade__avg"])
            media_preco = render_estrelas(avaliacoes.aggregate(Avg("nota_preco"))["nota_preco__avg"])
            media_disponibilidade = render_estrelas(avaliacoes.aggregate(Avg("nota_disponibilidade"))["nota_disponibilidade__avg"])

        # POST: salvar avaliação
        if request.method == "POST":
            form = AvaliacaoForm(request.POST)
            if form.is_valid():
                avaliacao = form.save(commit=False)
                avaliacao.estacionamento = estacionamento
                if request.user.is_authenticated:
                    avaliacao.usuario = request.user
                avaliacao.save()
                return redirect(f"{request.path}?estac_id={estac_id}")

    context = {
        "estacionamentos": estacionamentos,
        "estacionamento": estacionamento,
        "avaliacoes": avaliacoes,
        "media_seguranca": media_seguranca,
        "media_praticidade": media_praticidade,
        "media_preco": media_preco,
        "media_disponibilidade": media_disponibilidade,
        "avaliacao_form": form,
    }
    return render(request, "telaAval.html", context)


def render_estrelas(media):
    if media is None:
        return "☆☆☆☆☆"
    arred = round(media)
    return "★" * arred + "☆" * (5 - arred)


def register_view(request):
    form = UsuarioRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("sistema_avaliacao")
    return render(request, "registroUser.html", {"form": form})


def registerEstacionamento_view(request):
    form = EstacionamentoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("sistema_avaliacao")
    return render(request, "registroEstacionamento.html", {"form": form})
