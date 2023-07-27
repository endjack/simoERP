from datetime import datetime
from django.db import models

from obras.models import Local, Obra

SITUAÇÃO = (
        ("NÃO INICIADO", "Não Iniciado"),("EM ANDAMENTO", "Em andamento" ), ("FINALIZADO", "Finalizado"),
        ("PENDENTE", "Pendente"),("PARALISADO", "Paralisado" ),
    )

class OrdemServicoManutencao(models.Model):
    numero_os = models.IntegerField(blank=True, null=True, unique=True)
    solicitante = models.CharField(max_length=200, null=True) 
    encarregado = models.CharField(max_length=200, null=True)
    descricao_servico = models.CharField(max_length=200, null=True) 
    situacao = models.CharField(max_length=50, choices=SITUAÇÃO, default='NÃO INICIADO') 
    obra = models.ForeignKey(Obra, on_delete=models.SET_NULL, null=True)
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True)
    data_recebimento = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    data_prazo = models.DateField(null=True, blank=True)
    data_conclusao = models.DateField(null=True, blank=True)
    finalizado = models.BooleanField(default=False)
    na_planilha = models.BooleanField(default=False)
    obs = models.TextField(max_length=500, null=True, blank=True)


    def __str__(self) -> str:
        return "OS nº: " + str(self.numero_os) + " - Local: " + str(self.local.local) 
