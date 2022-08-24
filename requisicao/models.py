from datetime import datetime
from funcionarios.models import Funcionario
from django.db.models.deletion import CASCADE, SET_NULL
from estoque.models import Item
from obras.models import Local, Obra
from django.db import models

# Create your models here.

class Requisicao(models.Model):
    obra = models.ForeignKey(Obra, on_delete=SET_NULL, null=True)
    local = models.ForeignKey(Local, on_delete=CASCADE, null=True)
    solicitante = models.ForeignKey(Funcionario, on_delete=SET_NULL, null=True, related_name="solicitante_req") 
    almoxarife = models.ForeignKey(Funcionario, on_delete=SET_NULL, null=True, related_name="almoxarife_req") 
    data = models.DateField(null=True)

    def __str__(self) -> str:
        return "Id: " + str(self.pk) +" - Solicitante: " + str(self.solicitante.nome)+ ' - Data: ' + str(self.data) 

class RequisicaoTemp(models.Model):
    obra = models.ForeignKey(Obra, on_delete=SET_NULL, null=True)
    local = models.ForeignKey(Local, on_delete=CASCADE, null=True)
    solicitante = models.ForeignKey(Funcionario, on_delete=SET_NULL, null=True, related_name="solicitante_req_temp") 
    almoxarife = models.ForeignKey(Funcionario, on_delete=SET_NULL, null=True, related_name="almoxarife_req_temp") 
    data = models.DateField(null=True)

    def __str__(self) -> str:
        return "Id: " + str(self.pk) +" - Solicitante: " + str(self.solicitante.nome)+ ' - Data: ' + str(self.data) 

class ItemRequisicao(models.Model):
    requisicao = models.ForeignKey(Requisicao, on_delete=CASCADE, null=True)
    item = models.ManyToManyField(Item, blank=True)
    quantidade = models.FloatField(blank=True, null=True)

    
    def __str__(self) -> str:
        #Referenciando um ManyToMany no __str__
        item_req = self.item.all().first()
        if item_req:
            return "RequisicaoID: " + str(self.requisicao.pk) +" - Item: " + str(item_req.descricao)+ ' - Qtd: ' + str(self.quantidade) 

class ItemRequisicaoTemp(models.Model):
    requisicao = models.ForeignKey(RequisicaoTemp, on_delete=CASCADE)
    item = models.ManyToManyField(Item, blank=True)
    quantidade = models.FloatField(blank=True, null=True)

    
    def __str__(self) -> str:
        #Referenciando um ManyToMany no __str__
        item_req = self.item.all().first()
        if item_req:
            return "RequisicaoID: " + str(self.requisicao.pk) +" - Item: " + str(item_req.descricao)+ ' - Qtd: ' + str(self.quantidade) 