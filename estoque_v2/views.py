from datetime import timedelta
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from estoque.models import *
from django.views.decorators.csrf import csrf_exempt
from funcionarios.models import Funcionario
from obras.models import Local, Obra
from django.db.models import Sum, Count, F
from requisicao.models import ItemRequisicao, Requisicao


@login_required(login_url='login/')
@csrf_exempt
def inicio_estoquev2(request, template_name = 'estoque_v2/inicio_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'INICIO'
        categorias = Categoria.objects.all()
        itens_count = Item.objects.all().count()
        itens_no_estoque = Estoque.objects.all()
        itens_produtos = itens_no_estoque.aggregate(Sum('quantidade'))['quantidade__sum']
        itens_zerados = itens_no_estoque.filter(quantidade = 0)
        itens_insuficientes = itens_no_estoque.filter(quantidade__lte = F('item__qtd_minima')).filter(quantidade__gt = 0)
      
        
        
        today_date = datetime.now()  
        #Soma de requisições dos últimos 10 dias, contando de hoje.
        req_ultimos_10_dias = Requisicao.objects.filter(data__range=[today_date - timedelta(days=10), today_date]).values(
                                                        'data__date').annotate(count=Count('data__date'))
        
        
        context = {
            'menu_ativo' : _menu_ativo,
            'categorias' : categorias,
            'itens_count' : itens_count,
            'itens_produtos' : itens_produtos,
            'req_ultimos_10_dias' : req_ultimos_10_dias,
            'itens_zerados' : itens_zerados,
            'itens_insuficientes' : itens_insuficientes,
         
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def procurar_estoquev2(request, template_name = 'estoque_v2/procurar_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'PROCURAR'
        categorias = Categoria.objects.all()
     
        context = {
            'menu_ativo' : _menu_ativo,
            'categorias' : categorias,
         
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def detalhar_item_de_estoque(request, pk, template_name = 'estoque_v2/detalhar_item_de_estoque.html'):

    if request.method == 'GET':
        item_estoque = Estoque.objects.get(pk=pk)
       
     
        context = {
            'item_estoque' : item_estoque,
    
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def movimentar_item_de_estoque(request, pk):

    if request.method == 'POST':
        item_estoque = Estoque.objects.get(pk=pk)
        qtd_no_estoque = item_estoque.quantidade
        qtd = float(request.POST.get('qntInput'))
        movimentar = request.POST.get('movimentar')
        
        
        #VALIDAÇÕES QTD
        
        if qtd == '' or qtd <= 0:
            response = HttpResponse('Valor inválido')
            response['HX-Retarget'] = '#errosDeMovimentacao'
        
            print(f'--------{movimentar} de {qtd}----ITEM: {item_estoque}')
            
            return response
        
        elif movimentar == 'SAIDA' and qtd > qtd_no_estoque:
            response = HttpResponse('Valor maior que no Estoque')
            response['HX-Retarget'] = '#errosDeMovimentacao'
        
            print(f'--------{movimentar} de {qtd}----ITEM: {item_estoque}')
            
            return response
            
        else:
            #MOVIMENTAR
            if movimentar == 'SAIDA':
                item_estoque.quantidade = item_estoque.quantidade - qtd
            else:
                item_estoque.quantidade = item_estoque.quantidade + qtd
            
            item_estoque.save()
            
            response = redirect('detalhar_item_de_estoque', pk=pk)
            return response
    
@login_required(login_url='login/')
@csrf_exempt
def filtrar_itens_estoque(request, template_name = 'estoque_v2/fragmentos/procurar/resultados_procurar.html'):

    if request.method == 'POST':
        
        descricao = request.POST.get('descricao') or ''
        marca = request.POST.get('marca') or ''
        categoria = request.POST.get('categoria') or '-1'

        if categoria == '-1':    
            itens = Estoque.objects.all().filter(item__descricao__icontains=descricao).filter(item__marca__icontains=marca)
        else:
            itens = Estoque.objects.all().filter(item__descricao__icontains=descricao).filter(item__marca__icontains=marca).filter(item__categoria__pk=int(categoria))
    
        
        # print(f'-------------RESULTADO DO FILTER ---> {itens}')
       
        context = {
         
            'itens': itens
         
        }
     
 
        return render(request, template_name , context)
 
#TODO REQUISIÇÕES DO ESTOQUE
# ------------------------------------------------------------  REQUISIÇÕES DO ESTOQUE ---------------------------------------------------
   
@login_required(login_url='login/')
@csrf_exempt
def requisicoes_estoquev2(request, template_name = 'estoque_v2/requisicoes_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'REQUISIÇÃO'
        
        from datetime import date
        data_hoje = datetime.now().date()
        requisicoes_do_dia = Requisicao.objects.filter(data__date = data_hoje)
        funcionarios_ativos = Funcionario.objects.all()
        locais = Local.objects.all()
        obras = Obra.objects.all()
        
        
        print(f'------------Requisições do Dia ({data_hoje}):')
        print(f'------------{requisicoes_do_dia}')
     
        context = {
            'menu_ativo' : _menu_ativo,
            'requisicoes_do_dia' : requisicoes_do_dia,
            'funcionarios_ativos' : funcionarios_ativos,
            'locais' : locais,
            'obras' : obras,
            
         
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def criar_requisicao_sem_itens(request):

    if request.method == 'POST':
        solicitante_atual = request.POST.get('solicitante')
        local_atual = request.POST.get('local')
        obra_atual = request.POST.get('obra')
        
        
        if solicitante_atual == '-1' or local_atual == '-1' or obra_atual == '-1':
            response = HttpResponse('Necessário preencher todos os campos.')
            response['HX-Retarget'] = '#ErrorRequisicao'
            return response
            
        else:
            solicitante_atual = Funcionario.objects.get(pk = int(solicitante_atual))
            local_atual = Local.objects.get(pk = int(local_atual))
            obra_atual = Obra.objects.get(pk = int(obra_atual))
         
            nova_req = Requisicao.objects.create(solicitante = solicitante_atual,
                                    local = local_atual,
                                    obra = obra_atual,
                                    almoxarife = request.user,
                                    data = datetime.now())
            
            
            return redirect('requisicoes_estoquev2')
    
@login_required(login_url='login/')
@csrf_exempt
def editar_dados_requisicao(request, pk):

    if request.method == 'POST':
        solicitante_atual = request.POST.get('solicitante')
        local_atual = request.POST.get('local')
        obra_atual = request.POST.get('obra')
        
        
        if solicitante_atual == '-1' or local_atual == '-1' or obra_atual == '-1':
            response = HttpResponse('Necessário preencher todos os campos.')
            response['HX-Retarget'] = '#ErrorRequisicao'
            return response
            
        else:
            solicitante_atual = Funcionario.objects.get(pk = int(solicitante_atual))
            local_atual = Local.objects.get(pk = int(local_atual))
            obra_atual = Obra.objects.get(pk = int(obra_atual))
         
            req_editada = Requisicao.objects.get(pk=pk)
            req_editada.solicitante = solicitante_atual
            req_editada.local = local_atual
            req_editada.obra = obra_atual
            
            req_editada.save()
            
            return redirect('detalhar_requisicao_de_estoque', pk=pk)
            
            
    
@login_required(login_url='login/')
@csrf_exempt
def filtrar_itens_estoque_requisicao(request, pk, template_name = 'estoque_v2/fragmentos/requisicoes/resultados_procurar_itens_requisicao.html'):

    if request.method == 'POST':
        req_atual = Requisicao.objects.get(pk=pk)
        descricao = request.POST.get('descricao') or ''
        marca = request.POST.get('marca') or ''
        categoria = request.POST.get('categoria') or '-1'

        if categoria == '-1':    
            itens = Estoque.objects.all().filter(item__descricao__icontains=descricao).filter(item__marca__icontains=marca)
        else:
            itens = Estoque.objects.all().filter(item__descricao__icontains=descricao).filter(item__marca__icontains=marca).filter(item__categoria__pk=int(categoria))
    
        
        # print(f'-------------RESULTADO DO FILTER ---> {itens}')
       
        context = {
         
            'itens': itens,
            'req_atual': req_atual
         
        }
     
 
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def add_itemRequisicao_requisicao(request, pk, item):

    if request.method == 'POST':
        _input_qtd = f'qntItemDeRequisicao{item}'
        qtd_solicitada = request.POST.getlist(_input_qtd)[0]
        item = Estoque.objects.get(pk=item)
        qtd_item_no_estoque = item.quantidade
        
        print(f'-------------QTD SOLICITADA: {qtd_solicitada}')
        print(f'-------------QTD NO ESTOQUE: {qtd_item_no_estoque}')
        
        #VALIDAÇÕES
        
        if qtd_solicitada == "":
            response = HttpResponse('Valor Inválido!')
            response['HX-Retarget'] = f'#erroQntItemRequisicao{item}'
            return response
        else:
            qtd_solicitada = float(qtd_solicitada) 
        
        if qtd_solicitada > qtd_item_no_estoque:
            response = HttpResponse('Qtd Insuficiente!')
            response['HX-Retarget'] = f'#erroQntItemRequisicao{item}'
            return response
        else:
            item.quantidade  =   qtd_item_no_estoque - qtd_solicitada
            item.save()
            req_atual = Requisicao.objects.get(pk=pk)
            
            ItemRequisicao.objects.create(requisicao = req_atual,
                                          item=item,
                                          quantidade=qtd_solicitada)
            
            return redirect('detalhar_requisicao_de_estoque', pk=pk)
    
@login_required(login_url='login/')
@csrf_exempt
def detalhar_requisicao_de_estoque(request, pk, template_name = 'estoque_v2/detalhar_requisicao_de_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'REQUISIÇÃO'
        req_atual = Requisicao.objects.get(pk=pk)
        categorias = Categoria.objects.all()
        funcionarios_ativos = Funcionario.objects.all()
        locais = Local.objects.all()
        obras = Obra.objects.all()
        
        itensRequisicao = ItemRequisicao.objects.filter(requisicao=req_atual)
     
        context = {
            'menu_ativo' : _menu_ativo,
            'req_atual' : req_atual,
            'categorias' : categorias,
            'itensRequisicao' : itensRequisicao,
            'funcionarios_ativos' : funcionarios_ativos,
            'locais' : locais,
            'obras' : obras,
         
        }
        return render(request, template_name , context)
        
    
@login_required(login_url='login/')
@csrf_exempt
def excluir_item_requisicao_estoque(request, pk, item):

    if request.method == 'GET':
        _menu_ativo = 'REQUISIÇÃO'
        itenRequisicao = ItemRequisicao.objects.get(pk=item)
        
        #DEVOLVER QUANTIDADE AO ITEM DE ESTOQUE
        itemEstoque = itenRequisicao.item
        itemEstoque.quantidade = itemEstoque.quantidade + itenRequisicao.quantidade
        
        itemEstoque.save()
        
        #EXCLUIR ITEMREQUISIÇÃO
        itenRequisicao.delete()
       
        return redirect('detalhar_requisicao_de_estoque', pk=pk)
    

#TODO ITENS DO ESTOQUE
# ------------------------------------------------------------  ITENS DO ESTOQUE ---------------------------------------------------
    
@login_required(login_url='login/')
@csrf_exempt
def cadastrar_itens_estoquev2(request, template_name = 'estoque_v2/cadastrar_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'CADASTRARITENS'
     
        context = {
            'menu_ativo' : _menu_ativo,
         
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def cadastrar_categoria_estoquev2(request, template_name = 'estoque_v2/cadastrar_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'CADASTRARCATEGORIAS'
     
        context = {
            'menu_ativo' : _menu_ativo,
         
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def impressoes_estoquev2(request, template_name = 'estoque_v2/impressoes_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'IMPRESSÃO'
     
        context = {
            'menu_ativo' : _menu_ativo,
         
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def relatorios_estoquev2(request, template_name = 'estoque_v2/relatorios_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'RELATÓRIO'
     
        context = {
            'menu_ativo' : _menu_ativo,
         
        }
        return render(request, template_name , context)
    
    
@login_required(login_url='login/')
@csrf_exempt
def hx_calcular_saldo_estoque(request, pk):

    if request.method == 'GET':
        item_estoque = Estoque.objects.get(pk=pk)
        qtd=float(request.GET.get('qntInput'))
        movimentar = request.GET.get('movimentar')
        
        if movimentar == 'SAIDA' and qtd >= 0 and qtd != '':
            saldo = item_estoque.quantidade - qtd
        elif movimentar == 'ENTRADA' and qtd >= 0 and qtd != '':
             saldo = item_estoque.quantidade + qtd
        else:
          saldo = item_estoque.quantidade
            
             
        saldo = str(saldo).replace(',', '').replace('.', ',')   
        
        return HttpResponse(saldo)
        
    
    
    
    
    
    
    