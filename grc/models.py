from django.db import models
from django.utils import timezone

# Create your models here.

LISTA_FRAMEWORK = (
        ( 'Securant', 'Securant'),
        ('LGPD', 'LGPD'),
)


LISTA_SITUACAO = (
    ('SIM', 'Sim'),
    ('EmP', 'Em parte'),
    ('NAO', 'Não'),
)
class Framework(models.Model):
    nome = models.CharField(max_length=15, choices=LISTA_FRAMEWORK)
    descricao = models.TextField(max_length=1000)

    def __str__(self):
        return self.nome

class Dimension(models.Model):
    framework = models.ForeignKey('Framework', related_name="dimension", on_delete=models.CASCADE)
    nic = models.CharField(max_length=10)
    nome = models.CharField(max_length=15)
    descricao = models.TextField(max_length=1000)

    def __str__(self):
        return self.nome

class Processo(models.Model):
    dimension = models.ForeignKey('Dimension', related_name="processo", on_delete=models.CASCADE)
    nic = models.CharField(max_length=10)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=1000)

    def __str__(self):
        return self.dimension.nic + " - " + self.nome

class Procedimento(models.Model):
    processo = models.ForeignKey('Processo', related_name="procedimento", on_delete=models.CASCADE)
    nic = models.CharField(max_length=10)
    descricao = models.TextField(max_length=1000)
    atendida = models.CharField(max_length=15, choices=LISTA_SITUACAO)
    data_conclusao = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return  self.processo.nome + '-' + self.nic