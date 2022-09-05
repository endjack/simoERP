from django.core.cache import cache
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.template import RequestContext


@csrf_exempt
def limpar_cache(request):  
    cache.clear()
    print("------------> CACHE LIMPO <-------------")
    return HttpResponse()





# @csrf_exempt
# def handler404(request, exception, template_name='404.html'):
#     response = render(request, template_name, status=404)
#     response.status_code = 404
#     return response