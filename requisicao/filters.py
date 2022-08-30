
import django_filters
from .models import *
from django_filters.filters import DateFilter



class RequisicaoFilter(django_filters.FilterSet):
    # descricao = django_filters.CharFilter(field_name='item__descricao', lookup_expr='icontains')
    data = DateFilter(field_name="data", lookup_expr='gte')

    class Meta:
        model = Requisicao
        fields = ['solicitante', 'local']