from fornecedores.models import Fornecedor
from funcionarios.models import Cargo
from django import forms
from django.db.models import fields
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import DateInput
from .models import *

AnexarImagensServicoFormSet = inlineformset_factory(Servico, FotosServico, fields=("foto",))

class ServicoForm(ModelForm):

 

    class Meta:
        model = Servico
        fields = '__all__'
        exclude = ['ordem','finalizado',]
        
class FinalizarServicoForm(ModelForm):
    class Meta:
        model = Servico
        fields = ['data_termino']

class FiltrarOrdem(ModelForm):
    class Meta:
        model= OrdemServico
        fields = ['local']
    
class OrdemServicoForm(ModelForm):  
    class Meta:
        model = OrdemServico
        fields = '__all__'
        exclude = ['na_planilha']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            id_funcionario = Cargo.objects.get(cargo="ENCARREGADO")
        except (AttributeError, Cargo.DoesNotExist):
            self.fields['encarregado'] = forms.ModelChoiceField(queryset = Funcionario.objects.filter(cargo=-1))
        else:
            self.fields['encarregado'] = forms.ModelChoiceField(queryset = Funcionario.objects.filter(cargo=id_funcionario.pk) #//TODO colocar ENCARREGADO para ser dinâmico e não fixo com ID
        )

        
class FuncionarioServicoForm(ModelForm):  
    class Meta:
        model = FuncionarioServico
        fields = '__all__'
        exclude = ['servico']
        
class FornecedorServicoForm(ModelForm):  
    class Meta:
        model = FornecedorServico
        fields = '__all__'
        exclude = ['servico']
        
class ItemServicoForm(ModelForm):  
    class Meta:
        model = ItensServico
        fields = '__all__'
        exclude = ['servico']
  