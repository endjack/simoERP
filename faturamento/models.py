from django.db import models
from obras.models import Obra
from datetime import datetime


FASE = (
        ("-", "-"),("EMPENHO", "Empenho" ), ("LIQUIDAÇÃO", "Liquidação"),
        ("PAGAMENTO", "Pagamento"),
    )

class Faturamento(models.Model):
    obra = models.ForeignKey(Obra, on_delete=models.SET_NULL, null=True, blank=True)
    data_inclusao = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    num_medicao = models.IntegerField(blank=True, null=True)
    num_notafiscal = models.IntegerField(blank=True, null=True)
    protocolo = models.CharField(max_length=50, blank=True, null=True)
    valor = models.DecimalField('valor', max_digits=20, decimal_places=2, null=True, blank=True)
    fase = models.CharField(max_length=50, choices=FASE, default='-')
    movimentacao = models.CharField(max_length=200, blank=True, null=True)
    pago = models.BooleanField(default=False)
    data_pagamento = models.DateField(null=True, blank=True)
    saldo = models.DecimalField('valor', max_digits=20, decimal_places=2, null=True, blank=True)
    obs = models.TextField(max_length=500, null=True, blank=True)