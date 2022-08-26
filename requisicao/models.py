from django.contrib.auth.models import User
from funcionarios.models import Funcionario
from django.db.models.deletion import PROTECT, SET_NULL
from estoque.models import Estoque
from obras.models import Local, Obra
from django.db import models

# Create your models here.

class Requisicao(models.Model):
    obra = models.ForeignKey(Obra, on_delete=SET_NULL, null=True)
    local = models.ForeignKey(Local, on_delete=SET_NULL, null=True)
    solicitante = models.ForeignKey(Funcionario, on_delete=SET_NULL, null=True, related_name="solicitante_req") 
    almoxarife = models.ForeignKey(User, on_delete=PROTECT, null=True)
    data = models.DateTimeField (null=True)

    def __str__(self) -> str:
        return "Id: " + str(self.pk) +" - Solicitante: " + str(self.solicitante.nome)+ ' - Data: ' + str(self.data) 

class RequisicaoTemp(models.Model):
    obra = models.ForeignKey(Obra, on_delete=SET_NULL, null=True, blank=True)
    local = models.ForeignKey(Local, on_delete=SET_NULL, null=True, blank=True)
    solicitante = models.ForeignKey(Funcionario, on_delete=SET_NULL, null=True, related_name="solicitante_req_temp", blank=True) 
    almoxarife = models.ForeignKey(User, on_delete=PROTECT, null=True)
    data = models.DateTimeField (null=True)


    def __str__(self) -> str:
        if self.solicitante == None or self.data == None:
            return "Id: " + str(self.pk) +" - Dados incomplentos"
        
        return "Id: " + str(self.pk) +" - Solicitante: " + str(self.solicitante.nome)+ ' - Data: ' + str(self.data) 

class ItemRequisicao(models.Model):
    requisicao = models.ForeignKey(Requisicao, on_delete=SET_NULL, null=True)
    item = models.ForeignKey(Estoque, on_delete=SET_NULL, null=True)
    quantidade = models.FloatField(blank=True, null=True)

    
    def __str__(self) -> str:
        #Referenciando um ManyToMany no __str__
        #item_req = self.item.all().first()
        return "ItemRequisicaoID: " + str(self.pk) +" - RequisicaoID: " + str(self.requisicao.pk) +" - Item: " + str(self.item.item.descricao)+ ' - Qtd: ' + str(self.quantidade) 

class ItemRequisicaoTemp(models.Model):
    requisicao = models.ForeignKey(RequisicaoTemp, on_delete=SET_NULL, null=True)
    item = models.ForeignKey(Estoque, on_delete=SET_NULL, null=True)
    quantidade = models.FloatField(blank=True, null=True)

    
    def __str__(self) -> str:
            return "ItemRequisicaoID: " + str(self.pk) +" - RequisicaoID: " + str(self.requisicao.pk) +" - Item: " + str(self.item.item.descricao)+ ' - Qtd: ' + str(self.quantidade) 