from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, Estacionamento

class UsuarioRegistrationForm(UserCreationForm):
    """
    Formulário para registrar novos usuários.
    Campos: username, email, senha (password1, password2), lugar_mora, vehicle_type
    """
    class Meta:
        model = Usuario
        fields = [
            'username',
            'email',
            'lugar_mora',
            'vehicle_type',
            'password1',
            'password2',
        ]
        labels = {
            'username': 'Nome de usuário',
            'email': 'E-mail',
            'lugar_mora': 'Local de residência',
            'vehicle_type': 'Tipo de veículo',
        }
        help_texts = {
            'password1': 'Digite uma senha forte.',
            'password2': 'Digite a mesma senha para confirmação.',
        }

class EstacionamentoForm(forms.ModelForm):
    """
    Formulário para criar ou editar registros de estacionamento.
    Campos: nome, endereco, disponibilidade, horario_abertura, horario_fechamento, imagem_url
    """
    class Meta:
        model = Estacionamento
        fields = [
            'nome',
            'endereco',
            'disponibilidade',
            'horario_abertura',
            'horario_fechamento',
            'imagem_url',
        ]
        labels = {
            'nome': 'Nome do Estacionamento',
            'endereco': 'Endereço',
            'disponibilidade': 'Disponibilidade',
            'horario_abertura': 'Horário de Abertura',
            'horario_fechamento': 'Horário de Fechamento',
            'imagem_url': 'URL da Imagem',
        }
        help_texts = {
            'imagem_url': 'Insira um link válido para a imagem (opcional).',
        }
        widgets = {
            'horario_abertura': forms.TimeInput(format='%H:%M'),
            'horario_fechamento': forms.TimeInput(format='%H:%M'),
        }
