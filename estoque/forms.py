from django import forms
from django.db.models import fields
from django.forms import ModelForm
from .models import *

class EstoqueModelForm(ModelForm):
    class Meta:
        model = Estoque
        fields = ['item','quantidade']

class MovimentacaoModelForm(ModelForm):
    class Meta:
        model = MovimentacaoEstoque
        fields = ['tipo','qtd']

class InserirItemForm(ModelForm):
    preco = forms.DecimalField(max_digits=20, decimal_places=2, localize=True, required=False)
    
    class Meta:
        model = Item
        fields = '__all__'

class CategoriaModelForm(ModelForm):
        class Meta:
            model = Categoria
            fields = '__all__'

class ItemBuscaForm(ModelForm):
    class Meta:
        model = Item
        fields = ['descricao']