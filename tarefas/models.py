from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, PROTECT

CORES = (
        ("#ffffff", "Branco"),("#ffebcd", "Creme" ),("#87cefa", "Azul Claro" ),
        ("#c8a2c8", "Lilás"),("#e4f1cb", "Verde Claro" ),("#dedede", "Cinza" ),
    )

class Tarefa(models.Model):
    titulo = models.CharField(max_length=255, null=True)
    cor = models.CharField(max_length=30, choices=CORES, default='#ffffff', blank=True)
    data_inclusao = models.DateTimeField(null=True, blank=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    feito = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=PROTECT)

    class Meta:
       ordering = ('data_inclusao',)