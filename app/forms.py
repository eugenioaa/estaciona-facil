from django import forms
from .models import Avaliacao
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario, Estacionamento

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = [
            'nota_seguranca',
            'nota_praticidade',
            'nota_preco',
            'nota_disponibilidade',
            'comentario',
        ]
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
            'comentario': forms.Textarea(attrs={'rows': 4, 'required': True}),
        }

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

