from datetime import datetime
from django.db import models
from django.db.models.deletion import PROTECT, SET_NULL
from obras.models import Local, Obra
from funcionarios.models import Funcionario
from django.contrib.auth.models import User

SITUAÇÃO = (
        ('0', "Não Iniciado"),
        ('1', "Em andamento"), 
        ('2', "Pendente"),
        ('3', "Paralisado"),
    )

class DiarioDeObraContrato(models.Model):

    # class Meta:
    #     managed = True
    #     db_table = 'engenharia_diariodeobracontrato'

    obra = models.ForeignKey(Obra, on_delete=models.SET_NULL, null=True)
    data = models.DateField(null=True, blank=True)
    atividades = models.TextField(max_length=500, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    ordem_servico = models.CharField(max_length=200, null=True, blank=True)   
    tempo_manha =  models.CharField(max_length=200, null=True, blank=True)
    tempo_tarde =  models.CharField(max_length=200, null=True, blank=True)
    equipamentos = models.TextField(max_length=500, null=True, blank=True)
    mao_de_obra = models.TextField(max_length=500, null=True, blank=True)
    ocorrencias = models.TextField(max_length=1000, null=True, blank=True)

class ServiçosDiarioDeObraContrato(models.Model):
    local = models.ForeignKey(Local, on_delete=models.SET_NULL, null=True)
    servicos = models.TextField(max_length=500, null=True, blank=True)
    mao_de_obra = models.TextField(max_length=500, null=True, blank=True)

class OrdemServicoObras(models.Model):
    numero_os = models.IntegerField(blank=True, null=True)
    solicitante = models.CharField(max_length=200, null=True) 
    encarregado = models.CharField(max_length=200, null=True)
    servicos = models.TextField(max_length=500, null=True, blank=True)
    situacao = models.CharField(max_length=50, choices=SITUAÇÃO, default='0') 
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
        
        if self.finalizado:
            return 'Finalizado'
        
        else:     
            for s in SITUAÇÃO:
                if self.situacao == s[0]:
                    print('------------', s[0], ' e ', s[1])
                    return s[1]
                          
    def get_files_by_os(self):
        arquivos = DocumentoOS.objects.filter(ordem_servico=self)
        return arquivos
    
    def get_imagens_by_os(self):
        imagens = ImagemOS.objects.filter(ordem_servico=self)
        return imagens
    
    def get_rdos_by_os(self):
        rdos = DiarioDeObraOs.objects.filter(ordem_servico=self)
        return rdos
    
    def get_funcionarios_by_os(self):
        func = FuncionarioOS.objects.filter(ordem_servico=self)
        return func


class FuncionarioOS(models.Model):
    servico = models.TextField(max_length=500, null=True, blank=True)
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True)
    ordem_servico = models.ForeignKey(OrdemServicoObras, on_delete=models.SET_NULL, null=True)
   
    def __str__(self) -> str:
        return self.funcionario.nome

class CategoriaImagem(models.Model):
    categoria = models.CharField(max_length=100, null=True)
    ordem_servico = models.ForeignKey(OrdemServicoObras, on_delete=models.SET_NULL, null=True)
   
    
    def get_imagens_by_category(self):
        imagens = ImagemOS.objects.filter(categoria=self)
        return imagens
   
    
    def __str__(self) -> str:
        return self.categoria


def def_pasta_upload_imagem(instance, name):
    return f'engenharia/fotos/obra{instance.ordem_servico.obra.pk}os{instance.ordem_servico.numero_os}/{name}'

class ImagemOS(models.Model):
    imagem = models.ImageField(upload_to=def_pasta_upload_imagem, blank=True, null=True)
    categoria = models.ForeignKey(CategoriaImagem, on_delete=models.SET_NULL, null=True)
    ordem_servico = models.ForeignKey(OrdemServicoObras, on_delete=models.SET_NULL, null=True)
    
    

def def_pasta_upload(instance, filename):
    return f'engenharia/file/obra{instance.ordem_servico.obra.pk}os{instance.ordem_servico.numero_os}/{filename}'

class DocumentoOS(models.Model):
    file = models.FileField(upload_to=def_pasta_upload, blank=True, null=True)
    nome = models.CharField(max_length=200, null=True)
    ordem_servico = models.ForeignKey(OrdemServicoObras, on_delete=models.SET_NULL, null=True)    
    
    def filename(self):
        import os
        return os.path.basename(self.file.name)
    
    def extension(self):
        import os
        name, extension = os.path.splitext(self.file.name)
        if extension == ".pdf":
            return '<i style="color:red" class="far fa-file-pdf"></i>'
        if extension == ".doc" or extension == '.docx' :
            return '<i style="color:#1068cc" class="far fa-file-word"></i>'
        if extension == ".xls" or extension == '.xlsx':
            return '<i style="color:green" class="far fa-file-excel"></i>'
        else:
            return extension

class DiarioDeObraOs(models.Model):
    data = models.DateField(null=True, blank=True)
    atividades = models.TextField(max_length=500, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=PROTECT)
    ordem_servico = models.ForeignKey(OrdemServicoObras, on_delete=models.SET_NULL, null=True)   
    tempo_manha =  models.CharField(max_length=200, null=True, blank=True)
    tempo_tarde =  models.CharField(max_length=200, null=True, blank=True)
    equipamentos = models.TextField(max_length=500, null=True, blank=True)
    mao_de_obra = models.TextField(max_length=500, null=True, blank=True)
    ocorrencias = models.TextField(max_length=1000, null=True, blank=True)
    fotos = models.ForeignKey(CategoriaImagem, on_delete=SET_NULL, null=True)
    

    