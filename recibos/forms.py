from django import forms
from .models import *

class ReciboForm(forms.ModelForm):
    valor = forms.DecimalField(max_digits=20, decimal_places=2, localize=True)
    class Meta:
        model = ReciboFornecedor
        fields = '__all__'