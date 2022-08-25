from estoque.filters import EstoqueFilter
from estoque.models import *
from .models import *
from requisicao.forms import ObraRequisicaoForm
from django.urls.base import reverse_lazy
from requisicao.models import ItemRequisicao, Requisicao
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
# Create your views here.



class GerarRequisicaoView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'requisicao/gerar-requisicao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        
        context["funcionarios_busca"] = ""
        context["form_obra"] = ObraRequisicaoForm()
        context["filter"] = EstoqueFilter()
  
        req = get_requisicao_temp()
        
        list_itens = ItemRequisicaoTemp.objects.filter(requisicao__pk = req.pk)
        context["list_in_cache"] = list_itens
        context["requisicao"] = req
    
        print_requisicao_temp()
        return context

def get_requisicao_temp():
    requisicao_pk = cache.get('requisicao_cache')
    print('Requisicao cache = '+ str(('vazio' if requisicao_pk == None else requisicao_pk)))
    requisicao_cache = None
    
    if requisicao_pk == None:     
        RequisicaoTemp.objects.all().delete()
        ItemRequisicaoTemp.objects.all().delete()
        requisicao_cache = RequisicaoTemp.objects.create()
        cache.set('requisicao_cache', requisicao_cache.pk )
        requisicao_pk = requisicao_cache.pk
    else:
        requisicao_cache = RequisicaoTemp.objects.get(pk=int(requisicao_pk))
        
    return  requisicao_cache   

def print_requisicao_temp():
        requisicao_cache = get_requisicao_temp()
        print("----->Requisicao nº "+ str(requisicao_cache.pk))
        print("----->Requisicao Solicitante "+ str(('vazio' if requisicao_cache.solicitante == None else requisicao_cache.solicitante.nome)))
        print("----->Requisicao Almoxarife "+ str(('vazio' if requisicao_cache.almoxarife == None else requisicao_cache.almoxarife.username)))
        print("----->Requisicao Obra  "+ str(('vazio' if requisicao_cache.obra == None else requisicao_cache.obra.nome)))
        print("----->Requisicao local  "+ str(('vazio' if requisicao_cache.local == None else requisicao_cache.local.local)))
        print("----->Data  "+ str(('vazio' if requisicao_cache.data == None else requisicao_cache.data)))
    
   
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
            req = get_requisicao_temp()
            req.solicitante = funcionario
            req.save()
            print_requisicao_temp()
            return render(request, template_name='requisicao/fragmentos/funcionario_selecionado.html', context={'funcionario': req.solicitante })

    
    return render(request, template_name='requisicao/fragmentos/funcionario_selecionado.html', context={'funcionario': ""})
     
    
@csrf_exempt
def requisicao_add_obra(request):
    obra = request.POST.get('obra')
    if obra != "":
        obra_sel = Obra.objects.get(pk=int(obra))
        if obra_sel:
            req = get_requisicao_temp()
            req.obra = obra_sel
            req.save()
            print_requisicao_temp()
            return render(request, template_name='requisicao/fragmentos/obra_selecionado.html', context={'obra': req.obra})

  
    return render(request, template_name='requisicao/fragmentos/obra_selecionado.html', context={'obra': ""})

    
@csrf_exempt
def requisicao_add_local(request):
    local = request.POST.get('local')
    if local != "":
        local_sel = Local.objects.get(pk=int(local))
        if local_sel:
            req = get_requisicao_temp()
            req.local = local_sel
            req.save()
            print_requisicao_temp()
            return render(request, template_name='requisicao/fragmentos/local_selecionado.html', context={'local': req.local})

    
    return render(request, template_name='requisicao/fragmentos/local_selecionado.html', context={'local': ""})
       
@csrf_exempt
def requisicao_add_itens_selecionados(request, pk):
    item = Estoque.objects.get(item__pk=pk)
    
    req = get_requisicao_temp()
        
    ItemRequisicaoTemp.objects.create(requisicao = req, item=item)

    list_itens = ItemRequisicaoTemp.objects.filter(requisicao = req)
    
    return render(request, template_name='requisicao/fragmentos/itens_selecionados.html', context={'list_in_cache': list_itens})

@csrf_exempt
def requisicao_excluir_item_lista_selecionada(request, pk):
   
    ItemRequisicaoTemp.objects.filter(pk=pk).delete()
    req = get_requisicao_temp()
    list_itens = ItemRequisicaoTemp.objects.filter(requisicao = req)
   
       
    return render(request, template_name='requisicao/fragmentos/itens_selecionados.html', context={'list_in_cache': list_itens})

@csrf_exempt
def requisicao_verificar_qnt(request, pk):
    itemTemp = ItemRequisicaoTemp.objects.get(pk=pk)
    input_qnt = request.POST.get('qnt'+ str(pk))
    input_qnt = float(input_qnt)
    
    if input_qnt == 0 or input_qnt == "" or input_qnt == None:
        itemTemp.quantidade = 0
            
        context = {
                "itemTemp": itemTemp,
                "textError": "<span style='color:gray'>Adicione quantidade!</span>",
                "styleError" : "border: 1px solid red;"
                
        }
        return render(request, template_name='requisicao/fragmentos/input-qnt.html', context=context)
    
    if input_qnt < 0:
        itemTemp.quantidade = 0    
        context = {
                "itemTemp": itemTemp,
                "textError": "<span style='color:red'>Somente valor positivo!</span>",
                "styleError" : "border: 1px solid red;"
                
        }
        return render(request, template_name='requisicao/fragmentos/input-qnt.html', context=context)
 
    if itemTemp.item.quantidade < input_qnt:
        itemTemp.quantidade = 0
        context = {
                "itemTemp": itemTemp,
                "textError": "<span style='color:red'>Valor superior ao Estoque!</span>",
                "styleError" : "border: 1px solid red;"
                
        }
        return render(request, template_name='requisicao/fragmentos/input-qnt.html', context=context)
    
    itemTemp.quantidade = input_qnt
    itemTemp.save()
    
    print(str(itemTemp.quantidade))

    context = {
                "itemTemp": itemTemp,
                "textError": "",
                "styleError" : "border: 2px solid green;"
                
        }
    return render(request, template_name='requisicao/fragmentos/input-qnt.html', context=context)

@csrf_exempt 
def requisicao_salvar(request):
    req = get_requisicao_temp()
    
    
    if req.solicitante:
            if req.obra:
                if req.local:
                    list_itens = ItemRequisicaoTemp.objects.filter(requisicao = req)
                    if list_itens.exists():
                        req.almoxarife = request.user
                        req.data = datetime.now()
                        req.save()
                        return HttpResponse("<span style='color:green'> Salvo <i class='fas fa-check'></i></span>")
                    else:
                      return HttpResponse("<span style='color:red'>Adicionar Itens!</span>")  
                return HttpResponse("<span style='color:red'>Selecionar Local!</span>")
            else:
              return HttpResponse("<span style='color:red'>Selecionar Obra!</span>")  
    else:
      return HttpResponse("<span style='color:red'>Selecionar Requerente!</span>")
  
    




@csrf_exempt 
def limpar_itens_selecionados(request): 
    req = get_requisicao_temp()
    ItemRequisicaoTemp.objects.filter(requisicao = req).delete()
    return render(request, template_name='requisicao/fragmentos/itens_selecionados.html')
       
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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

  
 
    
