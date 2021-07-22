from financeiro.models import ContaPagamento, Recebimento
from django.db.models.deletion import CASCADE
from obras.models import Obra
from django.db import models

# Create your models here.

# class ContaPorCentroCusto(models.Model):
#     centro_custo = models.ForeignKey(Obra, on_delete=CASCADE, blank=True, null=True)
#     conta = models.ForeignKey(ContaPagamento, on_delete=CASCADE, blank=True, null=True)
    

# class RecebimentoPorCentroCusto(models.Model):
#     centro_custo = models.ForeignKey(Obra, on_delete=CASCADE, blank=True, null=True)
#     recebimento = models.ForeignKey(Recebimento, on_delete=CASCADE, blank=True, null=True)