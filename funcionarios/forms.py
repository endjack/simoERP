from django import forms
from django.forms import models
from .models import *


class InserirFuncionarioForm(forms.ModelForm):  
    salario = forms.DecimalField(max_digits=20, decimal_places=2, localize=True)
    class Meta:
        model = Funcionario
        fields = '__all__'



class InserirCargoForm(forms.ModelForm):  
    class Meta:
        model = Cargo
        fields = '__all__'