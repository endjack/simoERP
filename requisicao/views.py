from time import sleep
from django.views.generic.list import ListView
from estoque.filters import EstoqueFilter
from estoque.forms import ItemBuscaForm
from estoque.models import *
from .models import *
from django.http.response import HttpResponse
from requisicao.forms import ObraRequisicaoForm
from django.urls.base import reverse, reverse_lazy
from requisicao.models import ItemRequisicao, Requisicao
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from weasyprint import HTML, CSS
from django.db.models import Q
from django.core.cache import cache
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

# Create your views here.



class GerarRequisicaoView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'requisicao/gerar-requisicao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        
        context["funcionarios_busca"] = ""
        context["form_obra"] = ObraRequisicaoForm()
        context["filter"] = EstoqueFilter()
        # cache.clear()
        context["list_in_cache"] = cache.get('list_item_requisicao')
        
           
        return context
    
@csrf_exempt
def requisicao_search_funcionario(request):
    busca = request.POST.get('busca_funcionario')
    if busca != "":
            resultados = Funcionario.objects.filter(nome__istartswith=busca)
        
            if resultados.exists():
                return render(request, template_name='requisicao/fragmentos/lista_busca_funcionarios.html', context={'funcionarios_busca': resultados})

            else:
                return render(request, template_name='requisicao/fragmentos/lista_busca_funcionarios.html', context={'funcionarios_busca': ""})
    else:
        return render(request, template_name='requisicao/fragmentos/lista_busca_funcionarios.html', context={'funcionarios_busca': ""}) 
    
@csrf_exempt
def requisicao_add_funcionario(request, pk):
    if request.POST:
        funcionario = Funcionario.objects.get(pk=pk)
        if funcionario:
            return render(request, template_name='requisicao/fragmentos/funcionario_selecionado.html', context={'funcionario': funcionario})

  
    return render(request, template_name='requisicao/fragmentos/funcionario_selecionado.html', context={'funcionario': ""})
     
    
@csrf_exempt
def requisicao_add_obra(request):
    obra = request.POST.get('obra')
    if obra != "":
        obra_sel = Obra.objects.get(pk=int(obra))
        if obra_sel:
            return render(request, template_name='requisicao/fragmentos/obra_selecionado.html', context={'obra': obra_sel})

  
    return render(request, template_name='requisicao/fragmentos/obra_selecionado.html', context={'obra': ""})

    
@csrf_exempt
def requisicao_add_local(request):
    local = request.POST.get('local')
    if local != "":
        local_sel = Local.objects.get(pk=int(local))
        if local_sel:
            return render(request, template_name='requisicao/fragmentos/local_selecionado.html', context={'local': local_sel})

  
    return render(request, template_name='requisicao/fragmentos/local_selecionado.html', context={'local': ""})
    
       
@csrf_exempt
def requisicao_add_itens_selecionados(request, pk):
    item = Estoque.objects.get(item__pk=pk)
    list_in_cache = cache.get('list_item_requisicao')
    if list_in_cache == None:   
        list_item_requisicao = list()
        list_item_requisicao.append(item)
        cache.set('list_item_requisicao', list_item_requisicao)
    else:
        list_in_cache.append(item)
        cache.set('list_item_requisicao', list_in_cache)  
    
    return render(request, template_name='requisicao/fragmentos/itens_selecionados.html', context={'list_in_cache': cache.get('list_item_requisicao')})

@csrf_exempt
def requisicao_excluir_item_lista_selecionada(request, pk):
    item = Estoque.objects.get(item__pk=pk)
    list_in_cache = cache.get('list_item_requisicao')
    
    list_in_cache.remove(item)
    cache.set('list_item_requisicao', list_in_cache)
        
    return render(request, template_name='requisicao/fragmentos/itens_selecionados.html', context={'list_in_cache': cache.get('list_item_requisicao')})


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# @csrf_exempt   
# def autocomplete_funcionarios(request):
#     busca = request.POST.get('busca')
#     template_name = 'requisicao/lista-funcionarios.html'

#     if busca != "":
#         print(str(busca))
#         funcionarios = Funcionario.objects.filter(nome__istartswith=str(busca))
        
#         if funcionarios.exists():
#             context = {
#             'funcionarios': funcionarios
#         }
#             return render(request, template_name, context )
    
#     return render(request, template_name, context={'funcionarios':""} )

# @csrf_exempt     
# def add_funcionario_requisicao(request):
       
#     if request.method == 'POST':
#         if request.POST.get('id'):
#             id = request.POST.get('id')   
            
#             print(id)
#             solicitante =  Funcionario.objects.get(pk=int(id))
#             req = Requisicao(solicitante=solicitante)
                     
#         cache.set('requisicao_temp', req, 600)      
        
#         return HttpResponse(status=200)
#     else:
#         return HttpResponse('Item Não Adicionado') #TODO FAZER UMA RESPOSTA EM HTML COM TABELA VAZIA
    
# @csrf_exempt     
# def remove_funcionario_requisicao(request):
                       
#     cache.set('requisicao_temp', "", 600)      
        
#     return HttpResponse(status=200)


# @csrf_exempt     
# def add_obra_local_requisicao(request):
                       
#     print(request.POST.get('dados_form[obra]'))   
#     print(request.POST.get('dados_form[local]'))   
    
#     #TODO fazer a adição e mostrar no template
        
#     return HttpResponse(status=200)

  
 
    
