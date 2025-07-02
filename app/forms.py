from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Avaliacao, Usuario, Estacionamento
# app/forms.py
from .models import Avaliacao, Usuario, Estacionamento, HistoricoOcupacao
class AvaliacaoForm(forms.ModelForm):
    """
    Formulário para submissão de avaliações de estacionamentos.
    Os campos 'usuario' e 'estacionamento' são preenchidos na view.
    """
    class Meta:
        model = Avaliacao
        exclude = ['usuario', 'estacionamento']  # Importante para não exibir no formulário
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


class UsuarioRegistrationForm(UserCreationForm):
    """
    Formulário para registro de novos usuários.
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
            'password2': 'Repita a senha para confirmação.',
        }
        widgets = {
            'lugar_mora': forms.TextInput(attrs={'placeholder': 'Ex: Copacabana'}),
        }


class EstacionamentoForm(forms.ModelForm):
    """
    Formulário para registro ou edição de estacionamentos.
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
            'imagem_url': 'URL da Imagem (opcional)',
        }
        help_texts = {
            'imagem_url': 'Insira um link direto para a imagem (opcional).',
        }
        widgets = {
            'horario_abertura': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fechamento': forms.TimeInput(attrs={'type': 'time'}),
        }

# app/forms.py

class HistoricoOcupacaoForm(forms.ModelForm):
    """
    Formulário para registrar a ocupação de um estacionamento em um dado momento.
    """
    class Meta:
        model = HistoricoOcupacao
        # Mostramos apenas o campo que o usuário precisa preencher.
        # O 'estacionamento' seria definido na view (ex: pela URL da página)
        # e o 'timestamp' é preenchido automaticamente.
        fields = ['vagas_ocupadas']
        
        labels = {
            'vagas_ocupadas': 'Número de Vagas Ocupadas Agora',
        }
        widgets = {
            'vagas_ocupadas': forms.NumberInput(attrs={'placeholder': 'Ex: 42', 'required': True}),
        }