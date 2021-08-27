from django import forms
from multiselectfield import MultiSelectField
from .models import *

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

    