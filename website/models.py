from django.db import models
from django.utils import timezone

# Create your models here.

LISTA_CATEGORIAS = (
    ('INFORMATIVO', 'iNFORMATIVO'),
    ('NOTICIA', 'Notícia'),
    ('CONTO', 'Conto'),
    ('OUTROS', 'Outros')
)

class Website(models.Model):
    titulo = models.CharField(max_length=100)
    artigo = models.TextField(max_length=1000)
    categoria = models.CharField(max_length=15, choices=LISTA_CATEGORIAS)
    autor = models.CharField(max_length=100),
    data_criacao = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.titulo