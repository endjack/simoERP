
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from estoque.models import Item
from funcionarios.models import Funcionario
from obras.models import Local, Obra


# Create your models here.

class CategoriaFerramenta(models.Model):
    categoria = models.CharField(max_length=200, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.categoria
    
    def get_class(self):
        return self.__class__.__name__



class Ferramenta(models.Model):
    
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Tamanho máximo da Imagem é %sMB" % str(megabyte_limit))
        
    ESTADO = (
        ('0', "NOVA"),('1', "USADA"),('2', "COM DEFEITO"),
        )

    
    categoria = models.ForeignKey(CategoriaFerramenta, on_delete=models.SET_NULL, blank=True, null=True, default='Sem Categoria')
    descricao = models.CharField(max_length=200, blank=True, null=True, unique=True)
    marca = models.CharField(max_length=200, blank=True, null=True)
    preco = models.DecimalField('preço', max_digits=20, decimal_places=2, default=0, null=True, blank=True)
    imagem = models.ImageField(upload_to='estoque/', validators=[validate_image], blank=True, null=True)
    cor = models.CharField(max_length=50, blank=True, null=True)
    tamanho = models.CharField(max_length=50, blank=True, null=True)
    numeracao = models.CharField(max_length=50, blank=True, null=True)
    estado = models.CharField(max_length=50, choices=ESTADO, default='1')
    ativa = models.BooleanField(default=False)
    manutencao = models.BooleanField(default=False)
    data_inclusao = models.DateTimeField(default=timezone.now)
    obs =  models.CharField(max_length=300, null=True, blank=True)
    acautelada = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'Ferramenta: {self.pk} - {self.descricao}'
    
    
    def get_situacao_label(self):
        if self.manutencao:
            return '<span class="text-secondary">EM MANUTENÇÃO</span>'
        else:
            if self.acautelada:
                return '<span class="text-danger">RESERVADA</span>'
            else:
                return '<span class="text-success">LIVRE</span>'
    
    def get_situacao(self):
        if self.manutencao:
            return 'manutencao'
        else:
            if self.acautelada:
                return 'reservada'
            else:
                return 'livre'
            
    def get_cautela_by_ferramenta(self):
        if self.acautelada:
            cautelaFerr = CautelaFerramenta.objects.filter(ferramenta = self)[0]
            
            if cautelaFerr is not None:
                return cautelaFerr.cautela
        
        return None
    
class Cautela(models.Model):
    
    SITUACAO = (
        ('0', "EM ABERTO"),('1', "ATIVA"),('2', "ENTREGUE COM OBS"),('3', "ENTREGUE")
        )
    
    solicitante = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, related_name='solicitante')
    almoxarifado = models.ForeignKey(User, on_delete=models.PROTECT)
    data_cautela = models.DateTimeField(default=timezone.now)
    data_devolucao = models.DateTimeField(default=timezone.now)
    obra = models.ForeignKey(Obra, on_delete=models.SET_NULL, null=True, blank=True)
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True)
    obs_entrega =  models.CharField(max_length=300, null=True, blank=True)
    obs_devolucao =  models.CharField(max_length=300, null=True, blank=True)
    ativa = models.BooleanField(default=False)
    situacao = models.CharField(max_length=50, choices=SITUACAO, default='0')
    
    def __str__(self) -> str:
        return f'Cautela {self.pk}'
    
    
    def get_situacao_label(self):
        if self.situacao == "0":
            return '<span class="text-secondary">EM ABERTO</span>'
        elif self.situacao == "1":
            return '<span class="text-success">ATIVA</span>'
        elif self.situacao == "2":
            return '<span class="text-danger">ENTREGUE COM OBS</span>'
        else:
            return '<span class="text-dark">ENTREGUE</span>'
        
    def get_ferramentas(self):
        return CautelaFerramenta.objects.filter(cautela = self)
    
class CautelaFerramenta(models.Model):
    
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.SET_NULL, null=True, related_name='ferramenta')
    cautela = models.ForeignKey(Cautela, on_delete=models.SET_NULL, null=True, related_name='cautela')

    
    def __str__(self) -> str:
        return f'CautelaFerramenta {self.pk}'
    
class Lista(models.Model):
    titulo = models.CharField(max_length=200, blank=True, null=True, unique=True)
    data = models.DateTimeField(default=timezone.now)
    solicitante = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_lista')
    
    
    def __str__(self) -> str:
        return f'Lista {self.pk} - Titulo {self.titulo}'
    
    def get_all_itens_by_lista(self):
        return ListaItem.objects.filter(lista = self)
    
class ListaItem(models.Model):
    
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, related_name='item')
    qtd_estoque = models.FloatField(default=0, null=True)
    qtd_requisitada = models.FloatField(default=0, null=True)
    lista = models.ForeignKey(Lista, on_delete=models.CASCADE, null=True, related_name='lista')
    obs =  models.CharField(max_length=300, null=True, blank=True)
    situacao = models.BooleanField(default=False)

    
    def __str__(self) -> str:
        return f'ListaItem {self.pk}'