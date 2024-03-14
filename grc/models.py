from django.db import models
from django.utils import timezone
from django.forms import ModelForm

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

LISTA_STATUS = (
    ('PLANEJADO', 'Planejado'),
    ('ANDAMENTO', 'Andamento'),
    ('CONCLUIDO', 'Concluido'),
    ('CANCELADO', 'Cancelado'),
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
    data_conclusao = models.DateField(default=None)

    def __str__(self):
        return  self.processo.nome + '-' + self.nic

class Editaprocedimento(ModelForm):
    class Meta:
        model = Procedimento
        fields = ["nic","descricao","atendida"]

class Plano(models.Model):
    procedimento = models.ForeignKey('Procedimento', related_name="plano", on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=1000)
    responsavel = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=15, choices=LISTA_STATUS)
    data_inicio = models.DateField(default=timezone.now)
    data_planejada = models.DateField(default=None)
    data_conclusao = models.DateField(default=None)

    def __str__(self):
        return  self.procedimento.nic + ' - ' + self.nome

class Tarefa(models.Model):
    plano = models.ForeignKey('Plano', related_name="tarefa", on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.TextField(max_length=1000)
    responsavel = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=15, choices=LISTA_STATUS)
    data_inicio = models.DateField(default=timezone.now)
    data_planejada = models.DateField(default=None)
    data_conclusao = models.DateField(default=None)

    def __str__(self):
        return  self.plano.nome + ' - ' + self.nome