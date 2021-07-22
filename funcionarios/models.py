from django.db import models
from obras.models import Obra
from fornecedores.models import Banco
from django.db.models import F

# Create your models here.


class Cargo(models.Model):
    cargo = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.pk} - {self.cargo}"
    
    class Meta:
       ordering = [F('cargo').asc(nulls_last=True)]


class Funcionario(models.Model):

    TIPO_PIX = (
        ("CPF", "CPF"),("CNPJ", "CNPJ"),("TELEFONE", "TELEFONE"),("EMAIL", "EMAIL"),("ALEATÓRIO", "ALEATÓRIO"),
    )
    
    TIPO_CONTA = (
        ("CONTA-CORRENTE", "Conta-Corrente"),("POUPANÇA", "Poupança"),("CONTA-PAGAMENTO", "Conta-pagamento"),
    )

    SITUACAO = (
        ("ADMITIDO", "Admitido"),("DEMITIDO", "Demitido"),
    )


    situacao = models.CharField(max_length=50, choices=SITUACAO, default="ADMITIDO") 
    matricula = models.CharField(max_length=20, blank=True, null=True)
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    ctps = models.CharField(max_length=30, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    telefone1 = models.CharField(max_length=20, blank=True, null=True)
    telefone2 = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, blank=True, null=True)
    lotacao = models.ForeignKey(Obra, on_delete=models.SET_NULL, blank=True, null=True)
    data_admissao = models.DateField(null=True, blank=True)
    data_demissao = models.DateField(null=True, blank=True)
    salario = models.DecimalField('valor', max_digits=20, decimal_places=2, null=True, blank=True)
    adicional = models.CharField(max_length=50, blank=True, null=True)
    obs = models.TextField(max_length=200, null=True, blank=True)
    banco = models.ForeignKey(Banco, on_delete=models.SET_NULL, blank=True, null=True)
    agencia = models.CharField(max_length=10, blank=True, null=True)
    tipo_conta = models.CharField(max_length=50, choices=TIPO_CONTA, default="CONTA-CORRENTE")
    op = models.CharField(max_length=10, blank=True, null=True)
    conta = models.CharField(max_length=10, blank=True, null=True)
    pix = models.CharField(max_length=10, blank=True, null=True)
    tipo_pix = models.CharField(max_length=50, choices=TIPO_PIX, default="CPF")

    def __str__(self) -> str:
        return self.nome + ' - '+ str(self.cargo.cargo)

    class Meta:
       ordering = [F('nome').asc(nulls_last=True)]
