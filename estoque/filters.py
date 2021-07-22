from django import forms
import django_filters
from django_filters.filters import DateFilter
from .models import *
from distutils.util import strtobool


class EstoqueFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Item
        fields = ['descricao','categoria','fornecedor']
