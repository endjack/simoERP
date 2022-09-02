from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT


class Tarefa(models.Model):
    titulo = models.CharField(max_length=100, null=True)
    descricao = models.CharField(max_length=255, null=True)
    cor = models.CharField(max_length=30, default='#0a68cc', blank=True)
    data_inclusao = models.DateTimeField(null=True, blank=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    feito = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=PROTECT)

    class Meta:
       ordering = ('data_inclusao',)