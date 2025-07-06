# Caminho: app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Avaliacao, Usuario, Estacionamento, HistoricoOcupacao

# --- Formulário de Login ---
class LoginForm(forms.Form):
    """
    Formulário para autenticação de usuários existentes.
    """
    username = forms.CharField(label='Usuário', max_length=150)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)


# --- Formulário de Avaliação ---
class AvaliacaoForm(forms.ModelForm):
    """
    Formulário para submissão de avaliações de estacionamentos.
    """
    class Meta:
        model = Avaliacao
        exclude = ['usuario', 'estacionamento']
        labels = {
            'nota_seguranca': 'Nota - Segurança (1 a 5)',
            'nota_praticidade': 'Nota - Praticidade (1 a 5)',
            'nota_preco': 'Nota - Preço (1 a 5)',
            'nota_disponibilidade': 'Nota - Disponibilidade (1 a 5)',
            'comentario': 'Comentário',
        }
        widgets = {
            'nota_seguranca': forms.NumberInput(attrs={'min': 1, 'max': 5, 'required': True}),
            'nota_praticidade': forms.NumberInput(attrs={'min': 1, 'max': 5, 'required': True}),
            'nota_preco': forms.NumberInput(attrs={'min': 1, 'max': 5, 'required': True}),
            'nota_disponibilidade': forms.NumberInput(attrs={'min': 1, 'max': 5, 'required': True}),
            'comentario': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Escreva aqui seu comentário...'}),
        }


# --- Formulário de Registo de Utilizador ---
class UsuarioRegistrationForm(UserCreationForm):
    """
    Formulário para registro de novos usuários, herdando os campos de senha do Django.
    """
    class Meta:
        model = Usuario
        # CORRIGIDO: UserCreationForm já inclui os campos de senha.
        # Listamos apenas os campos do nosso modelo personalizado.
        fields = [
            'username',
            'email',
            'lugar_mora',
            'vehicle_type',
        ]
        labels = {
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'lugar_mora': 'Local de residência',
            'vehicle_type': 'Tipo de veículo',
        }
        widgets = {
            'lugar_mora': forms.TextInput(attrs={'placeholder': 'Ex: Copacabana'}),
        }


# --- Formulário de Registo de Estacionamento ---
class EstacionamentoForm(forms.ModelForm):
    """
    Formulário para registro ou edição de estacionamentos.
    """
    class Meta:
        model = Estacionamento
        # Adicionei os campos de coordenadas para que possam ser preenchidos no formulário
        fields = [
            'nome', 'endereco', 'horario_abertura', 'horario_fechamento',
            'latitude', 'longitude', 'imagem_url',
        ]
        labels = {
            'nome': 'Nome do Estacionamento',
            'endereco': 'Endereço',
            'horario_abertura': 'Horário de Abertura',
            'horario_fechamento': 'Horário de Fechamento',
            'latitude': 'Latitude',
            'longitude': 'Longitude',
            'imagem_url': 'URL da Imagem (opcional)',
        }
        widgets = {
            'horario_abertura': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fechamento': forms.TimeInput(attrs={'type': 'time'}),
            'latitude': forms.NumberInput(attrs={'placeholder': 'Ex: -22.9068'}),
            'longitude': forms.NumberInput(attrs={'placeholder': 'Ex: -43.1729'}),
        }


# --- Formulário de Histórico de Ocupação ---
class HistoricoOcupacaoForm(forms.ModelForm):
    """
    Formulário para registrar a ocupação de um estacionamento em um dado momento.
    """
    class Meta:
        model = HistoricoOcupacao
        fields = ['vagas_ocupadas']
        labels = {
            'vagas_ocupadas': 'Número de Vagas Ocupadas Agora',
        }
        widgets = {
            'vagas_ocupadas': forms.NumberInput(attrs={'placeholder': 'Ex: 42', 'required': True}),
        }