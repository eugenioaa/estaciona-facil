# Caminho: app/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# NOVO MODELO PARA OS BAIRROS
class Bairro(models.Model):
    """
    Armazena os nomes dos bairros para serem usados em um dropdown.
    """
    nome = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ['nome']


class Usuario(AbstractUser):
    """
    Modelo de usuário personalizado com campos adicionais.
    """
    email = models.EmailField('email', unique=True)
    
    # CAMPO 'lugar_mora' ATUALIZADO
    # Agora é uma chave estrangeira (ForeignKey) para o modelo Bairro
    lugar_mora = models.ForeignKey(
        Bairro,
        on_delete=models.SET_NULL, # Se um bairro for deletado, o campo no usuário fica nulo
        null=True,
        blank=True,
        verbose_name='Bairro onde mora'
    )

    VEHICLE_CHOICES = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
    ]
    vehicle_type = models.CharField(
        'utiliza veículo',
        max_length=50,
        choices=VEHICLE_CHOICES,
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.email})"


# O resto dos seus modelos (Estacionamento, Avaliacao, etc.) continua igual abaixo...

class Estacionamento(models.Model):
    class Disponibilidade(models.TextChoices):
        BAIXA = 'baixa', 'Baixa'
        MEDIA = 'media', 'Média'
        ALTA = 'alta', 'Alta'

    nome = models.CharField(
        'Nome', 
        max_length=200, 
        help_text="Nome comercial do estacionamento."
    )
    endereco = models.CharField('Endereço', max_length=300)
    imagem_url = models.URLField('URL da Imagem', max_length=500, blank=True, null=True)
    latitude = models.FloatField(
        'Latitude',
        blank=True, null=True,
        help_text="Coordenada de latitude para o mapa (ex: -22.9068)."
    )
    longitude = models.FloatField(
        'Longitude',
        blank=True, null=True,
        help_text="Coordenada de longitude para o mapa (ex: -43.1729)."
    )
    horario_abertura = models.TimeField('Horário de Abertura')
    horario_fechamento = models.TimeField('Horário de Fechamento')
    preco_por_hora = models.DecimalField(
        'Preço por Hora',
        max_digits=8,
        decimal_places=2,
        blank=True, null=True
    )
    vagas_totais = models.PositiveIntegerField('Vagas Totais', blank=True, null=True)
    vagas_disponiveis = models.PositiveIntegerField('Vagas Disponíveis', blank=True, null=True)
    disponibilidade = models.CharField(
        'Disponibilidade',
        max_length=5,
        choices=Disponibilidade.choices,
        default=Disponibilidade.MEDIA,
        help_text="Calculado automaticamente se as vagas forem preenchidas."
    )
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)
    data_atualizacao = models.DateTimeField('Última Atualização', auto_now=True)

    class Meta:
        verbose_name = 'Estacionamento'
        verbose_name_plural = 'Estacionamentos'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if self.vagas_totais is not None and self.vagas_disponiveis is not None and self.vagas_totais > 0:
            percentual_disponivel = (self.vagas_disponiveis / self.vagas_totais) * 100
            if percentual_disponivel <= 10:
                self.disponibilidade = self.Disponibilidade.BAIXA
            elif 10 < percentual_disponivel <= 50:
                self.disponibilidade = self.Disponibilidade.MEDIA
            else:
                self.disponibilidade = self.Disponibilidade.ALTA
        
        super().save(*args, **kwargs)


class Avaliacao(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='avaliacoes'
    )
    estacionamento = models.ForeignKey(
        Estacionamento,
        on_delete=models.CASCADE,
        related_name='avaliacoes',
        null=True,
        blank=True
    )
    nota_seguranca = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    nota_praticidade = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    nota_preco = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    nota_disponibilidade = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        nome_usuario = self.usuario.username if self.usuario else "Anônimo"
        return f"Avaliação de {nome_usuario} em {self.estacionamento.nome} - {self.data_avaliacao.strftime('%d/%m/%Y')}"

    def media_avaliacao(self):
        return round(
            (self.nota_seguranca + self.nota_praticidade + self.nota_preco + self.nota_disponibilidade) / 4, 2
        )


class HistoricoOcupacao(models.Model):
    estacionamento = models.ForeignKey(Estacionamento, on_delete=models.CASCADE, related_name='historico')
    vagas_ocupadas = models.PositiveIntegerField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.estacionamento.nome} - {self.vagas_ocupadas} vagas em {self.timestamp.strftime('%d/%m/%Y %H:%M')}"

    class Meta:
        ordering = ['-timestamp']