
from financeiro.models import ContaPagamento
import json
from django.http import JsonResponse
from django.core import serializers
from django.http.response import HttpResponse
from fornecedores.models import Fornecedor


def getContasAPagar(request):
    
    if request.method == 'GET' and request.is_ajax():
        id_fornecedor = request.GET.get('id', None)
        fornecedor = Fornecedor.objects.get(pk=id_fornecedor)
        queryset = ContaPagamento.objects.filter(fornecedor=fornecedor).filter(pago=False).order_by("vencimento").values()
        
        return JsonResponse({"contas": list(queryset)}, status=200)
    
  