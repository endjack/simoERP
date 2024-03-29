from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import SET_NULL
from fornecedores.models import Fornecedor
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.deletion import PROTECT
from datetime import datetime
import locale


locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')  

# Create your models here.

class Categoria(models.Model):
    categoria = models.CharField(max_length=200, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.categoria
    
    def get_all_itens_by_categoria(self):
        return Item.objects.filter(categoria=self.categoria)
    
    def get_counter_itens_by_categoria(self):
        return Item.objects.filter(categoria=self.pk).count()

    def get_class(self):
        return self.__class__.__name__

class Item(models.Model):

    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Tamanho máximo da Imagem é %sMB" % str(megabyte_limit))
      
    UNIDADES = (
        ("UNID", "Unidade"),("KG", "Quilos"),("M", "Metros"),("M2", "Metros2"),("M3", "Metros3"),("CX", "Caixa"), ("CJ", "Conjunto"),
        ("PCT", "Pacote"),("PÇ", "Peça"),("TON", "Tonelada"),("L", "Litros"),("BD", "Balde"), ("GL","Galão"), ("LT","Latão"), ("QTD", "Quantidade"),
    )

    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, blank=True, null=True, default='Sem Descrição')
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, blank=True, null=True, default='Sem Fornecedor')
    descricao = models.CharField(max_length=200, blank=True, null=True, unique=True)
    marca = models.CharField(max_length=200, blank=True, null=True)
    imagem = models.ImageField(upload_to='estoque/', validators=[validate_image], blank=True, null=True)
    peso = models.FloatField(default=0, blank=True, null=True)
    unid_medida = models.CharField(max_length=50, choices=UNIDADES, default="UNID")
    qtd_minima = models.FloatField(default=0, blank=True, null=True)
    preco = models.DecimalField('preço', max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    qr_code = models.ImageField(upload_to='qrcodes/', blank=True, null=True)
    estocado = models.BooleanField(default=False)

    class Meta:
        ordering = ('descricao',)
        
    
    def __str__(self) -> str:
        return str(self.descricao)+ ' - '+ str(self.categoria if self.categoria != None else 'sem categoria')
    
    def get_valor_to_input(self):
        return str(self.preco)
    
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
    quantidade = models.FloatField(default=0)

    def __str__(self) -> str:   
        return str(self.item.descricao)+ ' - ' + str(self.quantidade)
    
    def get_situacao(self):
        
        if not self.item.qtd_minima:
             return 'secondary'
        else: 
            if self.quantidade > self.item.qtd_minima:
                return 'success'
            if self.quantidade <= self.item.qtd_minima and self.quantidade > 0:
                return 'warning'
            if self.quantidade <= 0:
                return 'danger'


class LogMovimentacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=PROTECT)
    # item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    item = models.CharField(max_length=300, blank=True, null=True)
    quantidade = models.FloatField(default=0)
    saldo = models.FloatField(default=0)
    adicionado = models.BooleanField(default=False)
    data_inclusao = models.DateTimeField(auto_now_add=True)
    log = models.CharField(max_length=300, blank=True, null=True)
    
class ItensSelecionados(models.Model):
    estoque = models.OneToOneField(Estoque, on_delete=models.DO_NOTHING)

