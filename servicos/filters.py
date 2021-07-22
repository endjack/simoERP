from django.db.models.fields import BLANK_CHOICE_DASH
import django_filters
from django_filters.filters import DateFilter
from .models import *
from distutils.util import strtobool

# BOOLEAN_CHOICES = (('null', 'TODOS'),('false', 'À PAGAR'), ('true', 'PAGO'),)

SITUAÇÃO = [
        ("NÃO INICIADO", "Não Iniciado"),("EM ANDAMENTO", "Em andamento" ), ("FINALIZADO", "Finalizado"),
        ("PENDENTE", "Pendente"),("PARALISADO", "Paralisado" ),
    ]

SITUAÇÃO_AND_EMPTY = [('','Tudo')] + SITUAÇÃO

class ServicosFilter(django_filters.FilterSet):
    descricao = django_filters.CharFilter(lookup_expr='icontains')
    # local = django_filters.CharFilter(field_name='ordem__local', lookup_expr='iexact')
    data_inicial = DateFilter(field_name="data_inicio", lookup_expr='gte')
    data_final = DateFilter(field_name="data_inicio", lookup_expr='lte')
    situacao = django_filters.TypedChoiceFilter(choices = SITUAÇÃO_AND_EMPTY)
    # na_planilha = django_filters.TypedChoiceFilter(choices=BOOLEAN_CHOICES, coerce=strtobool)

    class Meta:
        model = Servico
        fields = ['descricao','data_inicio','situacao','ordem__local',]
