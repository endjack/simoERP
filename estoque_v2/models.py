
from django.utils import timezone
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
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
    
class Cautela(models.Model):
    
    solicitante = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, related_name='solicitante')
    almoxarifado = models.ForeignKey(User, on_delete=models.PROTECT)
    data_cautela = models.DateTimeField(default=timezone.now)
    data_devolucao = models.DateTimeField(default=timezone.now)
    obra = models.ForeignKey(Obra, on_delete=models.SET_NULL, null=True, blank=True)
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True, blank=True)
    obs_entrega =  models.CharField(max_length=300, null=True, blank=True)
    obs_devolucao =  models.CharField(max_length=300, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'Cautela {self.pk}'
    
class CautelaFerramenta(models.Model):
    
    ferramenta = models.ForeignKey(Ferramenta, on_delete=models.SET_NULL, null=True, related_name='ferramenta')
    cautela = models.ForeignKey(Cautela, on_delete=models.SET_NULL, null=True, related_name='cautela')

    
    def __str__(self) -> str:
        return f'CautelaFerramenta {self.pk}'
    
 