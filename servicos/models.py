from clientes.models import Cliente, Fiscal
from datetime import datetime
from funcionarios.models import Funcionario
from fornecedores.models import Fornecedor
from estoque.models import Item
from obras.models import Obra, Local
from django.db import models


# Create your models here.

SITUAÇÃO = (
        ("NÃO INICIADO", "Não Iniciado"),("EM ANDAMENTO", "Em andamento" ), ("FINALIZADO", "Finalizado"),
        ("PENDENTE", "Pendente"),("PARALISADO", "Paralisado" ),
    )
    
TIPO = (
        ("INICIO", "Início"),("DURANTE", "Durante" ),("FIM", "Fim" ),
    )

class OrdemServico(models.Model):
    numero_os = models.IntegerField(blank=True, null=True, unique=True)
    solicitante = models.ForeignKey(Fiscal, on_delete=models.SET_NULL, null=True, blank=True)
    encarregado = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True)
    obra = models.ForeignKey(Obra, on_delete=models.SET_NULL, null=True)
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True)
    data = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    completo_servico = models.BooleanField(default=False)
    completo_funcionarios = models.BooleanField(default=False)
    completo_itens = models.BooleanField(default=False)

 
    def __str__(self) -> str:
        return "ID: " + str(self.pk) + " - Encarregado: " + str(self.encarregado) 

class Servico(models.Model):
    ordem = models.ForeignKey(OrdemServico, on_delete=models.CASCADE, null=True)
    descricao = models.CharField(max_length=200, null=True) 
    situacao = models.CharField(max_length=50, choices=SITUAÇÃO, default='NÃO INICIADO')
    obs = models.TextField(max_length=500, null=True, blank=True)
    data_inicio = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    prazo = models.DateField(null=True, blank=True)
    data_termino = models.DateField(null=True, blank=True)
    finalizado = models.BooleanField(default=False)
    na_planilha = models.BooleanField(default=False)
   
    def __str__(self) -> str:
        return "Serviço: " + str(self.descricao) + " - Situação: " + str(self.situacao)   #TODO COLOCAR PARA APARECER 'FINALIZADO'
    
class FuncionarioServico(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, null=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    
    def __str__(self) -> str:
        return "Servico: Funcionario: {}".format(self.funcionario.nome) 

class FornecedorServico(models.Model): 
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, null=True)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True)
    
class ItensServico(models.Model):
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    qnt = models.DecimalField('Quantidade', max_digits=9 , decimal_places=2)
    
    def __str__(self) -> str:
        return "Serviço:  Qnt: {} - Item: {}".format(self.qnt, self.item)
    
class FotosServico(models.Model):

    servico = models.ForeignKey(Servico, on_delete=models.CASCADE, null=True, blank=True)
    foto = models.ImageField(upload_to='servicos/', height_field='image_height', width_field='image_width', max_length=None)
    tipo = models.CharField(max_length=50, choices=TIPO, default='INICIO')
    
    image_height = models.IntegerField(blank=True, null=True)
    image_width = models.IntegerField(blank=True, null=True)
    
    def get_url(self):
        try:
                # or whatever causes the exception
                return self.foto.url
        except IOError:
                return None
