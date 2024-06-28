from django.db.models import F, ExpressionWrapper, Sum, DecimalField
from datetime import datetime
from django.db.models.deletion import CASCADE, PROTECT, DO_NOTHING
from fornecedores.models import Fornecedor
from obras.models import Obra
from django.db import models
from django.contrib.auth.models import User
import locale

locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')  

UNIDADES = (
        ("UNID", "Unidade"),("M", "Metros"),("M2", "Metros2"),("M3", "Metros3"),("CX", "Caixa"), ("CJ", "Conjunto"),
        ("PCT", "Pacote"),("PÇ", "Peça"),("TON", "Tonelada"),("L", "Litros"),("BD", "Balde"), ("GL","Galão"), ("LT","Latão"), ("QTD", "Quantidade"),
    )
# VERSÃO 2 DO FINANCEIRO
class DescricaoNota(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    nota_fiscal = models.CharField(max_length=50, null=True, blank=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=DO_NOTHING, null=True, blank=True, related_name='saidas' ) #para buscar todas as saidas do fornecedor tal = fornecedor.saidas.all()
    data_emissao = models.DateField(null=True, blank=True)
    centro_de_custo = models.ForeignKey(Obra, on_delete=DO_NOTHING, null=True, blank=True, related_name='saidas')
    
            
class ItensNota(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    qtd = models.DecimalField(default=0, max_digits=20, decimal_places=4, blank=True, null=True)
    unid_medida = models.CharField(max_length=50, choices=UNIDADES, default="UNID")
    valor = models.DecimalField(max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    
    
    def get_nota_by_item(self):
        return self.notacompleta_set.all().first()
    
    def valor_BR(self):
        return locale.currency(self.valor, grouping=True)
    
    def valor_total_BR(self):
        return locale.currency(self.qtd * self.valor, grouping=True)
    

    
class NotaCompleta(models.Model):
    saida = models.ForeignKey(DescricaoNota, on_delete=CASCADE, null=True, blank=True)
    itens = models.ManyToManyField(ItensNota)
    valor = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    desconto = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    pago = models.BooleanField(default=False)
    forma_pagamento = models.IntegerField(default=0, blank=True)  # 0 = Em aberto | 1 = A vista | 2 = Boleto
    usuario = models.ForeignKey(User, on_delete=PROTECT, null=True)

    def valor_Total_itens_BR(self):
        total = 0
        
        for v in self.itens.all():
            total +=  float(v.qtd) * float(v.valor)
          
        return locale.currency(total, grouping=True)
    
    def get_valor_total_itens(self):
            return self.itens.all().aggregate(total_itens = Sum(ExpressionWrapper(F("qtd") *  F("valor"),  output_field=DecimalField())))["total_itens"]

    def get_valor_total_itens_BR(self):
        if self.get_valor_total_itens():
            return locale.currency(self.get_valor_total_itens(), grouping=True)
        else:
          return locale.currency(0, grouping=True)  
    
    def valor_BR(self):
        if self.valor:
            return locale.currency(self.valor, grouping=True)
        else:
            return locale.currency(0, grouping=True)
        
    def get_all_itens_by_nota(self):
        return ItensNota.objects.filter(pk= self.pk).values()
    
    def __str__(self) -> str:
        return f"{self.pk} - {self.saida.nota_fiscal}"


class PagamentoVista(models.Model):
    conta = models.ForeignKey(NotaCompleta, on_delete=DO_NOTHING, null=True, blank=True)
    valor_pago = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    acrescimo = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    data_pagamento = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=PROTECT)
    obs = models.TextField(max_length=255, null=True, blank=True)
    
    def valor_pago_BR(self):
        return locale.currency(self.valor_pago, grouping=True)
    
    def valor_total_BR(self):
        if self.acrescimo:
            return locale.currency((self.conta.valor or 0) + (self.acrescimo or 0), grouping=True)
        else:
            return locale.currency(self.conta.valor or 0, grouping=True)
    
    def acrescimo_BR(self):
        return locale.currency(self.acrescimo, grouping=True)

    
class ContaBoleto(models.Model):    
    conta = models.ForeignKey(NotaCompleta, on_delete=DO_NOTHING, null=True, blank=True)
    parcela = models.IntegerField(blank=True)
    total_parcelas = models.IntegerField(blank=True)
    doc = models.CharField(max_length=25, null=True, blank=True)
    valor = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    data_vencimento= models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=PROTECT)
    pago = models.BooleanField(default=False)
    obs = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        verbose_name= 'Boleto'
    
    def valor_BR(self):
        return locale.currency(self.valor, grouping=True)
    
    def situacao_print(self):
        if self.pago:
            return 'Pago'
        else:
            if self.data_vencimento < datetime.date(datetime.now()):
                return 'Atrasado'
            else:
                return 'Em Dia'
   
        
class PagamentoBoleto(models.Model):    
    conta = models.ForeignKey(NotaCompleta, on_delete=DO_NOTHING, null=True, blank=True)
    boleto = models.ForeignKey(ContaBoleto, on_delete=DO_NOTHING, null=True, blank=True)
    acrescimo = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    valor_pago= models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    data_pagamento= models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=PROTECT)
    obs = models.CharField(max_length=100, null=True, blank=True)
    
    def valor_pago_BR(self):
        return locale.currency(self.valor_pago, grouping=True)
    
    def valor_total_BR(self):
        return locale.currency(self.conta.valor + self.acrescimo, grouping=True)

      

# VERSÃO 1 FINANCEIRO
class ContaPagamento(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    documento = models.CharField(max_length=50, null=True, blank=True, default="-")
    nota_fiscal = models.CharField(max_length=50, null=True, blank=True, default="-")
    fornecedor = models.ForeignKey(Fornecedor, on_delete=CASCADE, null=True, blank=True)
    data_inclusao = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    vencimento = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    pago = models.BooleanField(default=False)
    valor = models.DecimalField('valor', max_digits=20, decimal_places=2, null=True, blank=True)
    acrescimos = models.DecimalField('acrescimos', max_digits=20, decimal_places=2, default=0)
    total = models.DecimalField('total', max_digits=20, decimal_places=2, null=True, blank=True)
    obs = models.TextField(max_length=255, null=True, blank=True)
    centro_de_custo = models.ForeignKey(Obra, on_delete=CASCADE, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=PROTECT)
    tags = models.ManyToManyField(to='TagConta', blank=True)
    
    class Meta:
       ordering = ('vencimento',)
       
    def save(self, *args, **kwargs):
        if self.acrescimos:
            self.total = self.valor + self.acrescimos
        else:
            self.total = self.valor
        super(ContaPagamento, self).save(*args, **kwargs)
       
    def __str__(self) -> str:
        return f"{self.pk} - {self.descricao}"
    

    

    
class Pagamento(models.Model):
    conta = models.ForeignKey(ContaPagamento, on_delete=CASCADE, null=True, blank=True)
    valor_original = models.CharField(max_length=50, null=True, blank=True)
    valor = models.DecimalField('valor', max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    data = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    total = models.BooleanField(default=False)
    obs = models.TextField(max_length=500, null=True, blank=True)
    
    class Meta:
       ordering = [F('data').desc(nulls_last=True)]
       
    def __str__(self) -> str:
        return f"{self.pk} - {self.valor}"

class PagamentoTemp(models.Model):
    conta = models.ForeignKey(ContaPagamento, on_delete=CASCADE, null=True, blank=True)
    valor_original = models.CharField(max_length=50, null=True, blank=True)
    valor = models.DecimalField('valor', max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    data = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    total = models.BooleanField(default=False)
    obs = models.TextField(max_length=500, null=True, blank=True)   
    
    def __str__(self) -> str:
        return f"{self.pk} - {self.valor}" 
    
class Recebimento(models.Model):
    descricao = models.CharField(max_length=200, null=True, blank=True)
    documento = models.CharField(max_length=50, null=True, blank=True, default="-")
    centro_de_custo = models.ForeignKey(Obra, on_delete=CASCADE, null=True, blank=True)
    data = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    valor = models.DecimalField('valor', max_digits=20, decimal_places=2, null=True, blank=True)
    obs = models.TextField(max_length=500, null=True, blank=True)
    
    class Meta:
       ordering = [F('data').desc(nulls_last=True)]
       
class TagConta(models.Model):
    nome = models.CharField(max_length=100, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.pk} - {self.nome}"
    
