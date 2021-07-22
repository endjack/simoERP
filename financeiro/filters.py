from django import forms
import django_filters
from django_filters.filters import DateFilter
from .models import *
from distutils.util import strtobool

BOOLEAN_CHOICES = (('null', 'TODOS'),('false', 'À PAGAR'), ('true', 'PAGO'),)

class ContasFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(lookup_expr='icontains')
    data_inicial = DateFilter(field_name="vencimento", lookup_expr='gte')
    data_final = DateFilter(field_name="vencimento", lookup_expr='lte')
    pago = django_filters.TypedChoiceFilter(choices=BOOLEAN_CHOICES,
                                            coerce=strtobool)

    class Meta:
        model = ContaPagamento
        fields = ['descricao','centro_de_custo','pago','fornecedor',]
