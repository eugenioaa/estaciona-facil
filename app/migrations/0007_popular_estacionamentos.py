# Caminho: app/migrations/0007_popular_estacionamentos.py

from django.db import migrations
import datetime

# Lista de estacionamentos com os dados verificados e todos os campos obrigatórios preenchidos.
ESTACIONAMENTOS_DATA = [
    {
        "nome": "Estacionamento do Shopping da Gávea",
        "endereco": "R. Marquês de São Vicente, 52 - Gávea, Rio de Janeiro - RJ, 22451-040",
        "latitude": -22.97633,
        "longitude": -43.22718,
        "horario_abertura": datetime.time(10, 0),
        "horario_fechamento": datetime.time(22, 0),
    },
    {
        "nome": "Estacionamento da PUC-Rio",
        "endereco": "R. Marquês de São Vicente, 225 - Gávea, Rio de Janeiro - RJ, 22451-900",
        "latitude": -22.9768,
        "longitude": -43.2330,
        "horario_abertura": datetime.time(7, 0), # Horário estimado
        "horario_fechamento": datetime.time(23, 0), # Horário estimado
    },
    {
        "nome": "Estacionamento do Shopping Leblon",
        "endereco": "Av. Afrânio de Melo Franco, 290 - Leblon, Rio de Janeiro - RJ, 22430-060",
        "latitude": -22.9843,
        "longitude": -43.2183,
        "horario_abertura": datetime.time(10, 0), # Horário estimado
        "horario_fechamento": datetime.time(22, 0), # Horário estimado
    },
    {
        "nome": "Estacionamento do Zona Sul (Gávea)",
        "endereco": "Av. Rodrigo Otávio, 269 - Gávea, Rio de Janeiro - RJ, 22450-060",
        "latitude": -22.9784,
        "longitude": -43.2259,
        "horario_abertura": datetime.time(7, 0), # Horário estimado
        "horario_fechamento": datetime.time(22, 0), # Horário estimado
    },
    {
        "nome": "Estacionamento do Parque dos Patins",
        "endereco": "Av. Borges de Medeiros, s/n - Lagoa, Rio de Janeiro - RJ, 22470-030",
        "latitude": -22.97899,
        "longitude": -43.21745,
        "horario_abertura": datetime.time(6, 0),
        "horario_fechamento": datetime.time(22, 0),
    },
    {
        "nome": "Estacionamento Pão de Açúcar Leblon (BrasilPark)",
        "endereco": "R. José Linhares, 245 - Leblon, Rio de Janeiro - RJ, 22430-220",
        "latitude": -22.98367,
        "longitude": -43.22154,
        "horario_abertura": datetime.time(7, 0),
        "horario_fechamento": datetime.time(23, 0),
    },
    {
        "nome": "Estacionamento Gávea Trade Center",
        "endereco": "R. Embaixador Carlos Taylor, 105 - Gávea, Rio de Janeiro - RJ, 22451-080",
        "latitude": -22.9754,
        "longitude": -43.2292,
        "horario_abertura": datetime.time(8, 0), # Horário estimado
        "horario_fechamento": datetime.time(20, 0), # Horário estimado
    },
    {
        "nome": "Parque das Figueiras Estacionamentos",
        "endereco": "Av. Borges de Medeiros, 1424 - Lagoa, Rio de Janeiro - RJ, 22470-003",
        "latitude": -22.9723,
        "longitude": -43.2131,
        "horario_abertura": datetime.time(6, 0), # Horário estimado
        "horario_fechamento": datetime.time(22, 0), # Horário estimado
    },
    {
        "nome": "Estacionamento do Rio Design Leblon",
        "endereco": "Av. Ataulfo de Paiva, 270 - Leblon, Rio de Janeiro - RJ, 22440-033",
        "latitude": -22.9839,
        "longitude": -43.2195,
        "horario_abertura": datetime.time(10, 0), # Horário estimado
        "horario_fechamento": datetime.time(22, 0), # Horário estimado
    },
    {
        "nome": "Estapar Estacionamentos Gávea (Praça Santos Dumont)",
        "endereco": "Praça Santos Dumont, 31 - Gávea, Rio de Janeiro - RJ, 22470-060",
        "latitude": -22.97361,
        "longitude": -43.22555,
        "horario_abertura": datetime.time(7, 0),
        "horario_fechamento": datetime.time(23, 0),
    },
]

def popular_estacionamentos(apps, schema_editor):
    Estacionamento = apps.get_model('app', 'Estacionamento')
    for data in ESTACIONAMENTOS_DATA:
        # get_or_create para evitar duplicados se o script for executado mais de uma vez
        Estacionamento.objects.get_or_create(
            nome=data["nome"],
            defaults=data
        )

class Migration(migrations.Migration):

    dependencies = [
        # Aponta para a migração anterior, que populou os bairros
        ('app', '0006_popular_bairros'),
    ]

    operations = [
        migrations.RunPython(popular_estacionamentos),
    ]