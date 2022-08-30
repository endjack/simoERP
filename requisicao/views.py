from estoque.filters import EstoqueFilter
from estoque.models import *
from simo.utils import limpar_cache
from .models import *
from .filters import *
from requisicao.forms import ObraRequisicaoForm
from django.urls.base import reverse_lazy
from requisicao.models import ItemRequisicao, Requisicao
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse



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
    
@csrf_exempt
def ver_requisicoes(request):
    filter = RequisicaoFilter()
    reqs = Requisicao.objects.all()
    
    context = {
        'reqs': reqs,
        'filter': filter,
    }
    return render(request, template_name='requisicao/ver-requisicoes.html', context=context)

@csrf_exempt
def ver_itens_requisicao(request,pk):
    req = Requisicao.objects.get(pk=pk)
    itens = ItemRequisicao.objects.filter(requisicao__pk = pk)
    
    context = {
        'itens': itens,
        'req': req,
    }
    return render(request, template_name='requisicao/fragmentos/modal-itens-requisicao.html', context=context)



@csrf_exempt
def buscar_requisicoes(request):
    reqs = Requisicao.objects.all()
    filter_list = RequisicaoFilter(request.GET, reqs) 
    
    
    context = {
        'filter_list': filter_list,
    }
    return render(request, template_name='requisicao/fragmentos/lista-requisicoes.html', context=context)


@csrf_exempt
def excluir_requisicoes(request, pk):
    Requisicao.objects.filter(pk=pk).delete()
    reqs = Requisicao.objects.all()
    filter_list = RequisicaoFilter(request.GET, reqs) 
   
    
    print(filter_list)
    context = {
        'filter_list': filter_list,
    }
    return render(request, template_name='requisicao/fragmentos/lista-requisicoes.html', context=context)

def get_requisicao_temp():
    requisicao_pk = cache.get('requisicao_cache')
    
    # print('Requisicao cache = '+ str(('vazio' if requisicao_pk == None else requisicao_pk)))
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
    cache.set('validacao', False )
    item = ItemRequisicaoTemp.objects.get(pk=pk)
    input_qnt = request.POST.get('qnt'+ str(pk))
    input_qnt = float(input_qnt)
    print("input = "+ str(input_qnt))
    
    resposta = validar_input_quantidade(input_qnt ,item.item)
    
    if not resposta['inpERROR']:
        item.quantidade = input_qnt
        item.save()
        resposta['item'] = item
    else:
        item.quantidade = 0
        resposta['item'] = item    
    
    
    print(str(item.quantidade))

    return render(request, template_name='requisicao/fragmentos/input-qnt.html', context=resposta)

def validar_input_quantidade(input_qnt, item_estoque):
 
    if input_qnt == 0 or input_qnt == "" or input_qnt == None:                
        resposta = {
                "inpERROR": True,
                "textError": "<span style='color:gray'>Adicione quantidade!</span>",
                "styleError" : "border: 1px solid red;"
        }
    else:
        if input_qnt < 0: 
            resposta = {
                    "inpERROR": True,
                    "textError": "<span style='color:red'>Somente valor positivo!</span>",
                    "styleError" : "border: 1px solid red;"
                    
            }
        else:
            if item_estoque.quantidade < input_qnt:   
                resposta = {
                        "inpERROR": True,
                        "textError": "<span style='color:red'>Valor superior ao Estoque!</span>",
                        "styleError" : "border: 1px solid red;"
                      
                }
            else:
                resposta = {
                        "inpERROR": False,
                        "textError": "",
                        "styleError" : "border: 2px solid green;"
                        
                }

    return resposta            

def validar_itens_requisicao(req):
    itens_req = ItemRequisicaoTemp.objects.filter(requisicao = req)
    for item in itens_req:
        # print("itemqnt = "+str(item.quantidade))
        resposta =  validar_input_quantidade(item.quantidade, item.item)
        # print(''+ str(resposta['inpERROR']) + ' - '+ str(item.item.item.pk) + ' Erro: ' + str(resposta['textError']))
        if resposta['inpERROR']:
            return True
    
    return False   
             
@csrf_exempt 
def requisicao_salvar(request):
    req = get_requisicao_temp()
     
    reqERROR = ''
    
    if req.solicitante:
            if req.obra:
                if req.local:
                    list_itens = ItemRequisicaoTemp.objects.filter(requisicao = req)
                    if list_itens.exists():
                        if not validar_itens_requisicao(req):
                            req.almoxarife = request.user
                            req.data = datetime.now()
                            req.save()
                            reqNOVO= criar_requisicao(req)
                            context={
                                'req' : reqNOVO,
                            }
                            response = render(request, template_name='requisicao/fragmentos/status-requisicao.html', context=context)
                            response['HX-Trigger'] = 'reqCriado'
                            cache.set('req_criado', True )
                            return response
                        else:
                            reqERROR = 'VERIFICAR QUANTIDADES'
                            return render(request, template_name='requisicao/fragmentos/status-requisicao.html', context={'reqERROR': reqERROR})
                    else:
                        reqERROR = 'ADICIONAR ITENS'
                        return render(request, template_name='requisicao/fragmentos/status-requisicao.html', context={'reqERROR': reqERROR})
                else:
                    reqERROR = 'SELECIONAR LOCAL'      
                    return render(request, template_name='requisicao/fragmentos/status-requisicao.html', context={'reqERROR': reqERROR})
            else:
                reqERROR = 'SELECIONAR OBRA'  
                return render(request, template_name='requisicao/fragmentos/status-requisicao.html', context={'reqERROR': reqERROR})
    else:
      reqERROR = 'SELECIONAR REQUERENTE'  
      return render(request, template_name='requisicao/fragmentos/status-requisicao.html', context={'reqERROR': reqERROR})
          
def criar_requisicao(reqTemp):
    
    #salvando requisição definitiva
    req = Requisicao()
    req.solicitante = reqTemp.solicitante
    req.almoxarife = reqTemp.almoxarife
    req.obra = reqTemp.obra
    req.local = reqTemp.local
    req.data = reqTemp.data
    req.save()
    
    print(req.__str__())
    
    #salvando itens de Requisição definitivos
    itens_req = ItemRequisicaoTemp.objects.filter(requisicao = reqTemp)
    print("Total itensREq: "+ str(itens_req.count()))
    for item in itens_req:
        item_novo = ItemRequisicao()
        item_novo.requisicao = req
        item_novo.item = item.item
        item_novo.quantidade = item.quantidade
        item_novo.save()
        
        print(item_novo.__str__())
    
    return req

@csrf_exempt 
def limpar_itens_selecionados(request): 
    req = get_requisicao_temp()
    ItemRequisicaoTemp.objects.filter(requisicao = req).delete()
    return render(request, template_name='requisicao/fragmentos/itens_selecionados.html')


       
@csrf_exempt 
def limpar_tudo_requisicao(request): 
    
    limpar_cache(request)
    return redirect(reverse_lazy("gerar-requisicao"))
       
@csrf_exempt     
def imprimir_requisicao(request,pk):
    req = Requisicao.objects.get(pk=pk)
    list_itens = ItemRequisicao.objects.filter(requisicao = req)
    
    context = {
        'req' : req,
        'list_itens' : list_itens,
    }
    return render(request, template_name='requisicao/imprimir-requisicao.html', context=context)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
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

  
 
    
