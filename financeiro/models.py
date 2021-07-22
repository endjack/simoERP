from django.db.models import F
from datetime import datetime
from django.db.models.deletion import CASCADE, PROTECT
from fornecedores.models import Fornecedor
from obras.models import Obra
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ContaPagamento(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    documento = models.CharField(max_length=50, null=True, blank=True, default="-")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=CASCADE, null=True, blank=True)
    data_inclusao = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    vencimento = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    pago = models.BooleanField(default=False)
    valor = models.DecimalField('valor', max_digits=20, decimal_places=2, null=True, blank=True)
    obs = models.TextField(max_length=500, null=True, blank=True)
    centro_de_custo = models.ForeignKey(Obra, on_delete=CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=PROTECT)
    
    class Meta:
       ordering = ('vencimento',)
    
class Pagamento(models.Model):
    conta = models.ForeignKey(ContaPagamento, on_delete=CASCADE, null=True, blank=True)
    valor_original = models.CharField(max_length=50, null=True, blank=True)
    valor = models.DecimalField('valor', max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    data = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    total = models.BooleanField(default=False)
    obs = models.TextField(max_length=500, null=True, blank=True)
    
    class Meta:
       ordering = [F('data').desc(nulls_last=True)]
    
    
class Recebimento(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    documento = models.CharField(max_length=50, null=True, blank=True, default="-")
    centro_de_custo = models.ForeignKey(Obra, on_delete=CASCADE, null=True, blank=True)
    data = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    valor = models.DecimalField('valor', max_digits=20, decimal_places=2, null=True, blank=True)
    obs = models.TextField(max_length=500, null=True, blank=True)
    
    class Meta:
       ordering = [F('data').desc(nulls_last=True)]