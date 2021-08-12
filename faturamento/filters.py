import django_filters
from .models import *

class FaturamentoFilter(django_filters.FilterSet):

    class Meta:
        model = Faturamento
        fields = ['obra',]

