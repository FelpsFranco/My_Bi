from django.db import models


class Atendente(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Atendimento(models.Model):
    atendente = models.ForeignKey(Atendente, on_delete=models.CASCADE)
    qtd_chamados = models.IntegerField()
    qtd_registrados = models.IntegerField()
    positivos = models.IntegerField()
    negativos = models.IntegerField()
    data = models.DateField()

    def __str__(self):
        return f"Atendimento por {self.atendente} em {self.data}"
