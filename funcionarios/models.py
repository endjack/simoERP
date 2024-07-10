from django.db import models
from django.core.exceptions import ValidationError
from obras.models import Local, Obra
from fornecedores.models import Banco
from django.db.models import F

# Create your models here.


class Cargo(models.Model):
    cargo = models.CharField(max_length=200)

    def __str__(self) -> str:
        return f"{self.pk} - {self.cargo}"
    
    class Meta:
       ordering = [F('cargo').asc(nulls_last=True)]
       
       
class FuncionarioV2(models.Model):
    
    class Contratos(models.TextChoices):
         DETERMINADO = 'DETERMINADO', 'Prazo Determinado'
         INDETERMINADO = 'INDETERMINADO', 'Prazo Indeterminado'
         
    class TipoPix(models.TextChoices):
         CPF = 'CPF', 'CPF'
         CNPJ = 'CNPJ', 'CNPJ'
         TELEFONE = 'TELEFONE', 'Telefone'
         EMAIL = 'E-MAIL', 'E-mail'
         ALEATÓRIO = 'ALEATÓRIO', 'Aleatório'
         
    class EstadoCivil(models.TextChoices):
         SOLTEIRO = 'SOLTEIRO', 'SOLTEIRO'
         CASADO = 'CASADO', 'CASADO'
         SEPARADO = 'SEPARADO', 'SEPARADO'
         DIVORCIADO = 'DIVORCIADO', 'DIVORCIADO'
         VIUVO = 'VIÚVO', 'VIÚVO'
    
    class TipoConta(models.TextChoices):
         CONTA_CORRENTE = 'CONTA-CORRENTE', 'Conta-Corrente'
         POUPANÇA = 'POUPANÇA', 'Poupança'
         CONTA_PAGAMENTO = 'CONTA-PAGAMENTO', 'Conta-pagamento'
         
    class TipoDemissao(models.TextChoices):
         COM_JUSTA_CAUSA = 'COM JUSTA CAUSA', 'Demissão POR justa causa'
         SEM_JUSTA_CAUSA = 'SEM JUSTA CAUSA', 'Demissão SEM justa causa'
         PEDIDO_POR_JUSTA_CAUSA = 'PEDIDO POR JUSTA_CAUSA', 'Pedido de demissão POR justa causa'
         PEDIDO_SEM_JUSTA_CAUSA = 'PEDIDO SEM JUSTA_CAUSA', 'Pedido de demissão SEM justa causa'

    
    class Situacao(models.TextChoices):
         ADMITIDO = "ADMITIDO", "Admitido"
         DEMITIDO = "DEMITIDO", "Demitido"
         AFASTADO_INSS_POR_DOENÇA = "AFASTADO INSS - POR DOENÇA", "Afastado por Doença"
         AFASTADO_INSS_POR_ACIDENTE = "AFASTADO INSS - POR ACIDENTE", "Afastado por Acidente"
         
    def validate_image(fieldfile_obj):
        filesize = fieldfile_obj.file.size
        megabyte_limit = 5.0
        if filesize > megabyte_limit*1024*1024:
            raise ValidationError("Tamanho máximo da Imagem é %sMB" % str(megabyte_limit))
    
    #dados pessoais     
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    rg = models.CharField(max_length=20, blank=True, null=True)
    ctps = models.CharField(max_length=30, blank=True, null=True)
    cnh = models.CharField(max_length=30, blank=True, null=True)
    categoria_cnh = models.CharField(max_length=20, blank=True, null=True)
    data_nascimento = models.DateField(null=True, blank=True)
    foto = models.ImageField(upload_to='funcionarios/', validators=[validate_image], blank=True, null=True)
    cep_endereco = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    telefone1 = models.CharField(max_length=20, blank=True, null=True)
    telefone2 = models.CharField(max_length=20, blank=True, null=True)
    estado_civil = models.CharField(max_length=50, choices=EstadoCivil.choices, default=EstadoCivil.SOLTEIRO)
    nome_mae = models.CharField(max_length=200,  blank=True, null=True)
    nome_pai = models.CharField(max_length=200,  blank=True, null=True)
    nacionalidade = models.CharField(max_length=200,  blank=True, null=True)
    
    #dados contratuais  
    situacao = models.CharField(max_length=50, choices=Situacao.choices, default=Situacao.ADMITIDO) #
    tipo_contrato = models.CharField(max_length=20, choices=Contratos.choices, default=Contratos.DETERMINADO) 
    data_admissao = models.DateField(null=True, blank=True)
    data_inicio_prorrogacao = models.DateField(null=True, blank=True)
    data_fim_prorrogacao = models.DateField(null=True, blank=True)
    matricula = models.CharField(max_length=20, blank=True, null=True)
    cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, blank=True, null=True)
    salario = models.FloatField(max_length=20, default=0)
    adicional = models.FloatField(max_length=20, default=0)
    data_ultimo_exame = models.DateField(null=True, blank=True)
    lotacao = models.ForeignKey(Obra, on_delete=models.SET_NULL, blank=True, null=True)
    tipo_responsavel = models.BooleanField(default=False)
    data_inicio_afastamento = models.DateField(null=True, blank=True)
    data_fim_afastamento = models.DateField(null=True, blank=True)
    data_demissao = models.DateField(null=True, blank=True)
    tipo_demissao = models.CharField(max_length=50, choices=TipoDemissao.choices, default=TipoDemissao.COM_JUSTA_CAUSA)
    
    #outras informações
    analfabeto = models.BooleanField(default=False)
    esocial = models.CharField(max_length=20, blank=True, null=True)
    data_cadastro = models.DateField(auto_now=True)
    ativo = models.BooleanField(default=True)
    obs = models.TextField(max_length=200, null=True, blank=True)
    responsavel_direto = models.ForeignKey('ResponsávelObraFuncionariov2', on_delete=models.SET_NULL, blank=True, null=True)
    
    #dados bancários  
    banco = models.ForeignKey(Banco, on_delete=models.SET_NULL, blank=True, null=True)
    agencia = models.CharField(max_length=10, blank=True, null=True)
    tipo_conta = models.CharField(max_length=50, choices=TipoConta.choices, default=TipoConta.CONTA_CORRENTE)
    conta = models.CharField(max_length=10, blank=True, null=True)
    op = models.CharField(max_length=10, blank=True, null=True)
    pix = models.CharField(max_length=50, blank=True, null=True)
    tipo_pix = models.CharField(max_length=50, choices=TipoPix.choices, default=TipoPix.CPF)
   
   
    def get_local_de_trabalho_by_funcionario(self):
        local = LocalDeTrabalhoFuncionario.objects.get(funcionario = self)
     
        if local:
            return local
        else:
            return None
   
     
    def get_funcionarios_livres():
       
        funcionarios = FuncionarioV2.objects.all().values_list('id', flat=True)
        locais_de_trabalho = LocalDeTrabalhoFuncionario.objects.all().values_list('funcionario__id', flat=True)
        
        livres_ids = list(funcionarios.difference(locais_de_trabalho))
        
        return FuncionarioV2.objects.filter(pk__in=livres_ids)
    
    def __str__(self) -> str:
        return self.nome + ' - '+ str(self.cargo.cargo)


class DependenteFuncionariov2(models.Model):
    nome = models.CharField(max_length=200)
    cpf = models.CharField(max_length=20, blank=True, null=True)
    funcionario = models.ForeignKey(FuncionarioV2, on_delete=models.CASCADE, blank=True, null=True)       
       
       
class ResponsávelObraFuncionariov2(models.Model):
    responsavel = models.OneToOneField(FuncionarioV2, on_delete=models.CASCADE)        
                
       
class LocalDeTrabalhoFuncionario(models.Model):
    local = models.ForeignKey(Local, on_delete=models.CASCADE)      
    funcionario = models.OneToOneField(FuncionarioV2, on_delete=models.CASCADE)    
       
    def __str__(self) -> str:
        return self.funcionario.nome +' - '+ str(self.local.local)   
       
       
       
       
       
       
       
       
       
#---------------------------------------- versão 1.0 -----------------------------------------------#    

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
