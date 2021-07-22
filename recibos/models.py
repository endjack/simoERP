from datetime import datetime
from django.db import models
from fornecedores.models import *
from obras.models import *

# Create your models here.

class ReciboFornecedor(models.Model):
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True)
    valor = models.DecimalField('valor', max_digits=20, decimal_places=2, null=True, blank=True)
    data = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    referente = models.TextField(max_length=500, null=True, blank=True)
    obs = models.TextField(max_length=500, null=True, blank=True)
    centro_de_custo = models.ForeignKey(Obra, on_delete=models.SET_NULL, null=True, blank=True)