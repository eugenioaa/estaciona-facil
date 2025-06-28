from django.shortcuts import render, redirect
from .forms import AvaliacaoForm, UsuarioRegistrationForm, EstacionamentoForm

def sistemaAval(request):
    return render(request, "telaAval.html")

def register_view(request):
    form = UsuarioRegistrationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('sistema_avaliacao')
    return render(request, 'registroUser.html', {'form': form})


def registerEstacionamento_view(request):
    form = EstacionamentoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('sistema_avaliacao')
    return render(request, 'registroEstacionamento.html', {'form': form})

def telaPrincipal(request):
    return render(request, "telaPrincipal.html")