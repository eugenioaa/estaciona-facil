# Caminho: app/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Avaliacao, Usuario, Estacionamento, HistoricoOcupacao, Bairro

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


# --- Formulário de Registo de Utilizador (ATUALIZADO PARA AUTOCOMPLETE) ---
class UsuarioRegistrationForm(UserCreationForm):
    """
    Formulário de registo com campo de bairro com autocompletar.
    """
    # Campo visível para o utilizador digitar o nome do bairro
    lugar_mora_nome = forms.CharField(
        label='Bairro onde mora',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Comece a digitar o nome do bairro...',
            'autocomplete': 'off',
            'class': 'bairro-autocomplete' # Classe para o JavaScript encontrar
        })
    )
    # Campo escondido que guardará o ID do bairro selecionado
    lugar_mora = forms.ModelChoiceField(
        queryset=Bairro.objects.all(),
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = UserCreationForm.Meta.fields + ('email', 'lugar_mora', 'vehicle_type')

    def clean(self):
        # Garante que se o nome do bairro for apagado, o ID também é limpo.
        cleaned_data = super().clean()
        if not cleaned_data.get('lugar_mora_nome'):
            cleaned_data['lugar_mora'] = None
        return cleaned_data


# --- Formulário para EDITAR Utilizador (ATUALIZADO PARA AUTOCOMPLETE) ---
class CustomUserChangeForm(UserChangeForm):
    """
    Formulário de edição de perfil com campo de bairro com autocompletar.
    """
    password = None # Remove o campo de senha da edição de perfil

    lugar_mora_nome = forms.CharField(
        label='Bairro onde mora',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Comece a digitar o nome do bairro...',
            'autocomplete': 'off',
            'class': 'bairro-autocomplete'
        })
    )
    lugar_mora = forms.ModelChoiceField(
        queryset=Bairro.objects.all(),
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'lugar_mora', 'vehicle_type')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Preenche o campo de nome com o bairro atual do utilizador ao carregar a página
        if self.instance and self.instance.lugar_mora:
            self.fields['lugar_mora_nome'].initial = self.instance.lugar_mora.nome

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('lugar_mora_nome'):
            cleaned_data['lugar_mora'] = None
        return cleaned_data


# --- Formulário de Registo de Estacionamento ---
class EstacionamentoForm(forms.ModelForm):
    """
    Formulário para registo ou edição de estacionamentos.
    """
    class Meta:
        model = Estacionamento
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
    Formulário para registar a ocupação de um estacionamento em um dado momento.
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