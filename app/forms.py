from django import forms
from .models import Avaliacao

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
