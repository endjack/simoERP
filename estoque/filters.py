from django import forms
import django_filters
from .models import *
from distutils.util import strtobool


class EstoqueFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(field_name='item__descricao', lookup_expr='icontains')
    marca = django_filters.CharFilter(field_name='item__marca', lookup_expr='icontains')

    class Meta:
        model = Estoque
        fields = ['item__categoria','item__fornecedor']
