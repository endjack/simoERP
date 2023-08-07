from clientes.models import Fiscal
from django.db import models
from django.db.models import F

# Create your models here.

def def_pasta_upload_imagem(instance, name):
    return f'obra/imagens/obra{instance.pk}_{name}'

class Obra(models.Model):
    nome = models.CharField(max_length=200)
    imagem = models.ImageField(upload_to=def_pasta_upload_imagem, blank=True, null=True)
    objeto = models.TextField(max_length=300, blank=True, null=True)
    endereco = models.CharField(max_length=300)
    contratante = models.CharField(max_length=100)
    num_contrato = models.CharField(max_length=50)
    inicio = models.CharField(max_length=200)
    fiscal = models.ForeignKey(Fiscal, on_delete=models.SET_NULL, null=True)  
    fim = models.CharField(max_length=200)
    valor = models.DecimalField('preço', max_digits=15, decimal_places=2, default=0, blank=True, null=True)
    concluido = models.BooleanField(default=False)
    invisivel = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.nome)+ ' - Contrato: '+ str(self.num_contrato)
    
    class Meta:
       ordering = [F('nome').asc(nulls_last=True)]


class Local(models.Model):
    local = models.CharField(max_length=200, unique=True)
    endereco = models.CharField(max_length=200, blank=True, null=True, default='Sem endereço')

    def __str__(self) -> str:
        return str(self.local) 
    
    class Meta:
       ordering = [F('local').asc(nulls_last=True)]
