from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    """
    Modelo de usuário personalizado com campos adicionais:
    - email: usado como campo único (já presente em AbstractUser, mas reforçado em unique)
    - username: nome de usuário (do AbstractUser)
    - password: gerenciado pelo AbstractUser
    - lugar_mora: local de residência do usuário (opcional para superuser)
    - vehicle_type: tipo de veículo utilizado (Carro ou Moto) (opcional para superuser)
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
        default='carro',
        blank=True,
        null=True,
    )

    # Apenas o email é obrigatório ao criar superuser
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.email})"

class Estacionamento(models.Model):
    """
    Modelo para registrar estacionamentos.
    Campos:
    - nome: nome do estacionamento
    - endereco: endereço completo
    - disponibilidade: nível de vagas disponíveis
    - horario_abertura: hora de início de funcionamento
    - horario_fechamento: hora de término de funcionamento
    - imagem_url: link opcional para imagem do estacionamento
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
