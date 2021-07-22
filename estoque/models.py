from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from fornecedores.models import Fornecedor


# Create your models here.

class Categoria(models.Model):
    categoria = models.CharField(max_length=200, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.categoria

class Item(models.Model):
    
    
    UNIDADES = (
        ("UNID", "Unidade"),("M", "Metros"),("M2", "Metros2"),("M3", "Metros3"),("CX", "Caixa"), ("CJ", "Conjunto"),
        ("PCT", "Pacote"),("PÇ", "Peça"),("TON", "Tonelada"),("LT", "Litros"),("BD", "Balde"), ("QTD", "Quantidade"),
    )

    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True, default='Sem Descrição')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, blank=True, null=True, default='Sem Fornecedor')
    descricao = models.CharField(max_length=200, blank=True, null=True, unique=True)
    peso = models.FloatField(default=0, blank=True, null=True)
    unid_medida = models.CharField(max_length=50, choices=UNIDADES, default="UNID")
    qtd_minima = models.IntegerField(default=0, blank=True, null=True)
    preco = models.DecimalField('preço', max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)

    class Meta:
        ordering = ('descricao',)
    
    def __str__(self) -> str:
        return str(self.descricao)+ ' - '+ str(self.categoria if self.categoria != None else 'sem categoria')
    


class MovimentacaoEstoque(models.Model):
    TIPOS = (("1","Entrada"),("2","Saída"))

    tipo = models.CharField(max_length=50, choices=TIPOS, default="1")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)
    qtd = models.FloatField(default=0, blank=True, null=True)
    data = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return str("Entrada" if self.tipo == '1' else "Saída")+ ' - ' + str(self.qtd)+ ' - ' + str(self.item.descricao) 

class Estoque(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="estoque")
    quantidade = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:   
        return str(self.item.descricao)+ ' - ' + str(self.quantidade)