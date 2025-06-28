from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo de usuário personalizado com campos adicionais.
    """
    email = models.EmailField('email', unique=True)
    lugar_mora = models.CharField('lugar onde mora', max_length=255, blank=True, null=True)

    VEHICLE_CHOICES = [
        ('carro', 'Carro'),
        ('moto', 'Moto'),
    ]
    vehicle_type = models.CharField(
        'utiliza veículo',
        max_length=10,
        choices=VEHICLE_CHOICES,
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = ['email']  # username continua obrigatório

    def __str__(self):
        return f"{self.username} ({self.email})"


class Estacionamento(models.Model):
    """
    Modelo para armazenar informações sobre um estacionamento.
    """
    DISPONIBILIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
    ]

    nome = models.CharField('Nome', max_length=200)
    endereco = models.CharField('Endereço', max_length=300)
    disponibilidade = models.CharField(
        'Disponibilidade',
        max_length=5,
        choices=DISPONIBILIDADE_CHOICES,
        default='media',
    )
    horario_abertura = models.TimeField('Horário de Abertura')
    horario_fechamento = models.TimeField('Horário de Fechamento')
    imagem_url = models.URLField('URL da Imagem', max_length=500, blank=True, null=True)
    data_criacao = models.DateTimeField('Data de Criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Estacionamento'
        verbose_name_plural = 'Estacionamentos'
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.endereco}"


class Avaliacao(models.Model):
    """
    Avaliação de um estacionamento, podendo ser feita por usuário autenticado ou anônimo.
    """
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
