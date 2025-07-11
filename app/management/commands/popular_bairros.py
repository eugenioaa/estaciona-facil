from django.core.management.base import BaseCommand
from app.models import Bairro

class Command(BaseCommand):
    help = 'Popula a base de dados com a lista de bairros do Rio de Janeiro'

    # Lista de bairros da cidade do Rio de Janeiro
    BAIRROS_RIO = [
        "Anchieta", "Bangu", "Barra da Tijuca", "Botafogo", "Campo Grande", "Centro",
        "Copacabana", "Flamengo", "Ipanema", "Jacarepaguá", "Leblon", "Madureira",
        "Méier", "Penha", "Realengo", "Santa Cruz", "São Conrado", "Taquara",
        "Tijuca", "Urca", "Vila Isabel", "Abolição", "Acari", "Água Santa", "Aldeia Campista",
        "Alto da Boa Vista", "Anil", "Bancários", "Barra de Guaratiba", "Barros Filho",
        "Benfica", "Bento Ribeiro", "Bonsucesso", "Brás de Pina", "Cachambi", "Cacuia",
        "Caju", "Camorim", "Campinho", "Cascadura", "Catete", "Catumbi", "Cavalcanti",
        "Cidade de Deus", "Cidade Nova", "Cidade Universitária", "Cocotá", "Coelho Neto",
        "Colégio", "Complexo do Alemão", "Cordovil", "Cosme Velho", "Cosmos", "Costa Barros",
        "Curicica", "Del Castilho", "Deodoro", "Encantado", "Engenheiro Leal", "Engenho da Rainha",
        "Engenho de Dentro", "Engenho Novo", "Estácio", "Freguesia (Ilha do Governador)",
        "Freguesia (Jacarepaguá)", "Galeão", "Gamboa", "Gardênia Azul", "Gávea", "Gericinó",
        "Glória", "Grumari", "Guadalupe", "Guaratiba", "Higienópolis", "Honório Gurgel",
        "Humaitá", "Inhaúma", "Inhoaíba", "Irajá", "Itanhangá", "Jabour", "Jacaré",
        "Jardim América", "Jardim Botânico", "Jardim Carioca", "Jardim Guanabara", "Jardim Sulacap",
        "Joá", "Lagoa", "Laranjeiras", "Leme", "Lins de Vasconcelos", "Magalhães Bastos",
        "Mangueira", "Manguinhos", "Maracanã", "Maré", "Marechal Hermes", "Moneró", "Olaria",
        "Oswaldo Cruz", "Paciência", "Padre Miguel", "Paquetá", "Parada de Lucas", "Parque Anchieta",
        "Parque Colúmbia", "Pavuna", "Pechincha", "Pedra de Guaratiba", "Penha Circular",
        "Piedade", "Pilares", "Pitangueiras", "Portuguesa", "Praça da Bandeira", "Praça Seca",
        "Praia da Bandeira", "Quintino Bocaiuva", "Ramos", "Recreio dos Bandeirantes", "Riachuelo",
        "Ribeira", "Ricardo de Albuquerque", "Rio Comprido", "Rocha", "Rocha Miranda", "Rocinha",
        "Sampaio", "Santa Teresa", "Santíssimo", "Santo Cristo", "Saúde", "Senador Camará",
        "Senador Vasconcelos", "Sepetiba", "Tanque", "Tauá", "Todos os Santos", "Tomás Coelho",
        "Turiaçu", "Vargem Grande", "Vargem Pequena", "Vasco da Gama", "Vaz Lobo", "Vicente de Carvalho",
        "Vidigal", "Vigário Geral", "Vila da Penha", "Vila Kennedy", "Vila Militar", "Vila Valqueire", "Zumbi"
    ]

    def handle(self, *args, **options):
        self.stdout.write('A popular a base de dados com os bairros...')
        count = 0
        for nome_bairro in self.BAIRROS_RIO:
            _, created = Bairro.objects.get_or_create(nome=nome_bairro)
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Concluído! {count} novos bairros foram adicionados.'))