from django.db import models

class Rota(models.Model):
    duracao = models.CharField(max_length=100)
    distancia = models.FloatField()
    custo = models.FloatField()


class Viagem(models.Model):
    pontos_de_parada = models.JSONField(default=list, blank=True)
    destino = models.IntegerField()
    origem = models.IntegerField()
    data_hora = models.DateTimeField()
    motorista = models.IntegerField()
    cliente = models.IntegerField()
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=50, default='pendente')  # Adicionado status para gerenciar a viagem

    def __str__(self):
        return f"Viagem de {self.origem} para {self.destino} em {self.data_hora}"
