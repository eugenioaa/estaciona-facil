from django.db import models

class Avaliacao(models.Model):
    usuario = models.CharField(max_length=100, default="Anônimo")  # ou use um User FK se quiser login
    nota_seguranca = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    nota_praticidade = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    nota_preco = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    nota_disponibilidade = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    data_avaliacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Avaliação de {self.usuario} em {self.data_avaliacao.strftime('%d/%m/%Y')}"

    def media_avaliacao(self):
        return round((self.nota_seguranca + self.nota_praticidade + self.nota_preco + self.nota_disponibilidade) / 4, 2)
