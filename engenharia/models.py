from datetime import datetime
from django.db import models

from obras.models import Local, Obra

SITUAÇÃO = (
        (0, "Não Iniciado"),
        (1, "Em andamento"), 
        (2, "Finalizado"),
        (3, "Pendente"),
        (4, "Paralisado"),
    )

class OrdemServicoObras(models.Model):
    numero_os = models.IntegerField(blank=True, null=True, unique=True)
    solicitante = models.CharField(max_length=200, null=True) 
    encarregado = models.CharField(max_length=200, null=True)
    servicos = models.TextField(max_length=500, null=True, blank=True)
    situacao = models.CharField(max_length=50, choices=SITUAÇÃO, default='NÃO INICIADO') 
    obra = models.ForeignKey(Obra, on_delete=models.SET_NULL, null=True)
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True)
    data_recebimento = models.DateField(null=True, blank=True, default=datetime.now().strftime("%d/%m/%Y"))
    data_inicio = models.DateField(null=True, blank=True)
    data_prazo = models.DateField(null=True, blank=True)
    data_conclusao = models.DateField(null=True, blank=True)
    finalizado = models.BooleanField(default=False)
    na_planilha = models.BooleanField(default=False)
    obs = models.TextField(max_length=500, null=True, blank=True)


    def __str__(self) -> str:
        if self.local is not None:
            return "OS nº: " + str(self.numero_os) + " - Local: " + str(self.local.local) 
        else:
            return "OS nº: " + str(self.numero_os) + " - Local: Indefinido" 
        
    def get_situacao(self):
        for s in SITUAÇÃO:
            if int(self.situacao) == s[0]:
                return s[1]

class CategoriaImagem(models.Model):
    categoria = models.CharField(max_length=200, unique=True, null=True)
    ordem_servico = models.ForeignKey(OrdemServicoObras, on_delete=models.SET_NULL, null=True)
    
    def get_imagens_by_category(self):
        imagens = ImagemOS.objects.filter(categoria=self)
        return imagens
   
    
    def __str__(self) -> str:
        return self.categoria

class ImagemOS(models.Model):
    imagem = models.ImageField(upload_to='engenharia/', blank=True, null=True)
    categoria = models.ForeignKey(CategoriaImagem, on_delete=models.SET_NULL, null=True)
    ordem_servico = models.ForeignKey(OrdemServicoObras, on_delete=models.SET_NULL, null=True)
    

    