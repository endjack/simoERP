from django import forms
from .models import *

class FaturamentoForm(forms.ModelForm):
    valor = forms.DecimalField(max_digits=20, decimal_places=2, localize=True)
    saldo = forms.DecimalField(max_digits=20, decimal_places=2, localize=True)
    class Meta:
        model = Faturamento
        fields = '__all__'
