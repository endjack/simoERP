from django.db import models
from django.db.models import F
# Create your models here.


class Banco(models.Model):
    nome = models.CharField(max_length=50, null=True, blank=True)
    codigo = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
       return f"{self.codigo} - {self.nome}"

class Fornecedor(models.Model):
    
    TIPO_FORNECEDOR = (
        ("PESSOA JURÍDICA", "Pessoa Jurídica"),("PESSOA FÍSICA", "Pessoa Física"),
    )
    
    TIPO_PIX = (
        ("CNPJ", "CNPJ"),("CPF", "CPF"),("TELEFONE", "TELEFONE"),("EMAIL", "EMAIL"),("ALEATÓRIO", "ALEATÓRIO"),
    )
    
    TIPO_CONTA = (
        ("CONTA-CORRENTE", "Conta-Corrente"),("POUPANÇA", "Poupança"),("CONTA-PAGAMENTO", "Conta-pagamento"),
    )
 
    tipo = models.CharField(max_length=50, choices=TIPO_FORNECEDOR, default="PESSOA JURÍDICA")
    nome = models.CharField(max_length=200, null=True, blank=True)
    razao_social = models.CharField(max_length=200, null=True, blank=True)
    inscricao = models.CharField(max_length=25, null=True, blank=True)
    doc = models.CharField(max_length=18, null=True, blank=True)
    endereco = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    telefone1 = models.CharField(max_length=30, null=True, blank=True)
    telefone2 = models.CharField(max_length=30, null=True, blank=True)
    banco = models.ForeignKey(Banco, on_delete=models.SET_NULL, null=True, blank=True)
    conta = models.CharField(max_length=20, null=True, blank=True)
    agencia = models.CharField(max_length=20, null=True, blank=True)
    tipo_conta = models.CharField(max_length=50, choices=TIPO_CONTA, default="CONTA-CORRENTE")
    pix = models.CharField(max_length=30, null=True, blank=True)
    tipo_pix = models.CharField(max_length=50, choices=TIPO_PIX, default="CNPJ")
    faz_nota = models.BooleanField(default=False)
    obs = models.TextField(max_length=500, null=True, blank=True)

    
    def __str__(self):
       return str(self.nome) or "" + str(' - CNPJ: '+ self.doc if self.doc else '') or "" + str(' - Razão Social: ' + self.razao_social) or ""
   
    class Meta:
       ordering = [F('nome').asc(nulls_last=True)]
       
    def template_options(self):
        return f'{self.nome} - {self.doc if self.doc else ""} · ID{self.pk}' #caracter · (alt + 250)

    
   

