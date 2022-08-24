from django.core.cache import cache
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render


@csrf_exempt
def limpar_cache(request):  
    cache.clear()
    print("------------> CACHE LIMPO <-------------")
    return render(request, template_name='requisicao/fragmentos/itens_selecionados.html')