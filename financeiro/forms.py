from email.policy import default
from django import forms
from multiselectfield import MultiSelectField
from .models import *



# VERSÃO 2 FINANCEIRO
class DescricaoForm(forms.ModelForm):
    class Meta:
        model = DescricaoNota
        fields =  ['nota_fiscal', 'data_emissao','centro_de_custo','descricao']
            
   
class ItensNotaForm(forms.ModelForm):
    
    class Meta:
        model = ItensNota
        fields = '__all__'
        exclude = ['valor',]

        


class PagamentoVistaForm(forms.ModelForm):
    data_pagamento = forms.DateField(initial=datetime.now().strftime("%Y-%m-%d")) #VALOR INICIAL NO INPUT DATA É O DE HOJE
    class Meta:
        model = PagamentoVista
        fields = '__all__'
        exclude = ['usuario',]










class ContaPagamentoForm(forms.ModelForm):
    valor = forms.DecimalField(max_digits=20, decimal_places=2, localize=True)
    tags = MultiSelectField(choices=tuple(TagConta.objects.values_list('pk', 'nome')))
    class Meta:
        model = ContaPagamento
        fields = '__all__'
        exclude = ['usuario']
        
class RecebimentoForm(forms.ModelForm):
    valor = forms.DecimalField(max_digits=20, decimal_places=2, localize=True)
    class Meta:
        model = Recebimento
        fields = '__all__'


        
class PagamentoForm(forms.ModelForm):
    valor = forms.DecimalField(max_digits=20, decimal_places=2, localize=True, required=False)
    class Meta:
        model = Pagamento
        fields = '__all__'

class PagamentoFormTemp(forms.ModelForm):
    valor = forms.DecimalField(max_digits=20, decimal_places=2, localize=True, required=False)
    class Meta:
        model = PagamentoTemp
        fields = '__all__'
        exclude = ['conta',]


    