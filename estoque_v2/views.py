from datetime import timedelta
from decimal import Decimal
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from estoque.models import *
from django.views.decorators.csrf import csrf_exempt
from estoque_v2.models import CategoriaFerramenta, Cautela, CautelaFerramenta, Ferramenta
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
def excluir_item_de_estoque(request, pk):

    if request.method == 'GET':
        item_estoque = Estoque.objects.get(pk=pk)
        item = item_estoque.item
        
        item_estoque.delete()
        item.estocado = False
        item.save()
       
        return redirect('inicio_estoquev2')
    
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
 
#TODO FERRAMENTAL
# ------------------------------------------------------------  FERRAMENTAL  ---------------------------------------------------   
    
@login_required(login_url='login/')
@csrf_exempt
def ver_ferramental_estoquev2(request, template_name = 'estoque_v2/ferramental_estoquev2.html'):

      if request.method == 'GET':
        _menu_ativo = 'FERRAMENTAL'
        
        #TODO COLOCAR AS FERRAMENTAS ACAUTELADAS PRIMEIRO E DEPOIS AS NÃO ACAUTELADAS EM LISTA
        acauteladas = CautelaFerramenta.objects.all()
        
        ferramentas = Ferramenta.objects.filter(acautelada=False)
        categorias_ferramentas = CategoriaFerramenta.objects.all()
        estados = Ferramenta.ESTADO
        funcionarios_ativos = Funcionario.objects.all()
        locais = Local.objects.all()
        obras = Obra.objects.all()
        
        
        context = {
            'menu_ativo' : _menu_ativo,
            'ferramentas' : ferramentas,
            'acauteladas' : acauteladas,
            'categorias_ferramentas' : categorias_ferramentas,
            'estados' : estados,
            'funcionarios_ativos' : funcionarios_ativos,
            'locais' : locais,
            'obras' : obras,
            
         
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def buscar_ferramentas(request, template_name = 'estoque_v2/ferramentas/buscar_ferramentas.html'):

      if request.method == 'GET':
        _menu_ativo = 'FERRAMENTAL'
        
        ferramentas = Ferramenta.objects.all()
        categorias_ferramentas = CategoriaFerramenta.objects.all()
        estados = Ferramenta.ESTADO
        funcionarios_ativos = Funcionario.objects.all()
        locais = Local.objects.all()
        obras = Obra.objects.all()
        
        
        context = {
            'menu_ativo' : _menu_ativo,
            'ferramentas' : ferramentas,
            'categorias_ferramentas' : categorias_ferramentas,
            'estados' : estados,
            'funcionarios_ativos' : funcionarios_ativos,
            'locais' : locais,
            'obras' : obras,
            
         
        }
        return render(request, template_name , context)
    
    
@login_required(login_url='login/')
@csrf_exempt
def add_nova_ferramenta_estoquev2(request):

    if request.method == 'POST':
        
        #VALIDAÇÕES
        if request.POST.get('descricao') == '':
            response = HttpResponse('Erro: Campo DESCRIÇÃO vazio.')
            response['HX-Retarget'] = '#error_ferramenta'
            return response
        else:
            descricao = request.POST.get('descricao').upper()
            
        marca = request.POST.get('marca').upper()
        
        if request.POST.get('categoria') == '-1':
            response = HttpResponse('Erro: Selecione uma CATEGORIA.')
            response['HX-Retarget'] = '#error_ferramenta'
            return response
        else:    
            categoria = CategoriaFerramenta.objects.get(pk = int(request.POST.get('categoria')))
            
        cor = request.POST.get('cor').upper()
        tamanho = request.POST.get('tamanho').upper()
        numeracao = request.POST.get('numeracao')
        preco = request.POST.get('preco')
        
        if request.POST.get('estado') == '-1':
            response = HttpResponse('Erro: Selecione um ESTADO.')
            response['HX-Retarget'] = '#error_ferramenta'
            return response
        else:     
            estado = request.POST.get('estado')
            
        if request.POST.get('radioAtivoSituacaoFerramenta') == 'ATIVO':
            ativa = True
            manutencao = False
        else:
            ativa = False
            manutencao = True
     
        imagemFerramenta = request.FILES.get('imagemFerramenta')
        
        obs = request.POST.get('obs')
        
        
        #CRIAR FERRAMENTA
        Ferramenta.objects.create(descricao = descricao,
                                  categoria = categoria,
                                  marca = marca,
                                  cor = cor,
                                  tamanho = tamanho,
                                  numeracao = numeracao,
                                  preco = preco,
                                  estado = estado,
                                  obs = obs,
                                  ativa = ativa,
                                  manutencao = manutencao,
                                  imagem = imagemFerramenta)

   
        return redirect('ferramental_estoquev2')
    
    
@login_required(login_url='login/')
@csrf_exempt
def criar_cautela_ferramenta(request):

    if request.method == 'POST':
        
        #VALIDAÇÕES
        if request.POST.get('solicitante') == '-1':
            response = HttpResponse('Erro: Selecione um FUNCIONÁRIO.')
            response['HX-Retarget'] = '#error_cautela'
            return response
        else:
            funcionario_atual = Funcionario.objects.get(pk = int(request.POST.get('solicitante')))
        
        if request.POST.get('local') == '-1':
            response = HttpResponse('Erro: Selecione um LOCAL.')
            response['HX-Retarget'] = '#error_cautela'
            return response
        else:
            local_atual = Local.objects.get(pk = int(request.POST.get('local')))
        
        if request.POST.get('obra') == '-1':
            response = HttpResponse('Erro: Selecione uma OBRA.')
            response['HX-Retarget'] = '#error_cautela'
            return response
        else:
            obra_atual = Obra.objects.get(pk = int(request.POST.get('obra')))
            

        #CRIAR CAUTELA
        cautela_atual = Cautela.objects.create(solicitante = funcionario_atual,
                            almoxarifado = request.user,
                            obra = obra_atual,
                            local = local_atual)
        
        return redirect('detalhar_cautela_ferramenta', pk = cautela_atual.pk) 
 
             

    
@login_required(login_url='login/')
@csrf_exempt
def detalhar_cautela_ferramenta(request, pk,  template_name = 'estoque_v2/ferramentas/detalhar_cautela.html'):

    if request.method == 'GET':
        _menu_ativo = 'FERRAMENTAL'
    
        cautela_atual = Cautela.objects.get(pk=pk)
        ferramentas = Ferramenta.objects.all()
         
        context = {
            'menu_ativo' : _menu_ativo,
            'cautela_atual' : cautela_atual,
            'ferramentas' : ferramentas,
         
        }
        return render(request, template_name , context) 
         
    
@login_required(login_url='login/')
@csrf_exempt
def inserir_ferramenta_em_cautela(request, pk, ferr, template_name = 'estoque_v2/ferramentas/detalhar_cautela.html'):

    if request.method == 'GET':

        cautela_atual = Cautela.objects.get(pk=pk)
        
        return redirect('detalhar_cautela_ferramenta', pk = cautela_atual.pk) 
            

    

#TODO ITENS DO ESTOQUE
# ------------------------------------------------------------  ITENS DO ESTOQUE ---------------------------------------------------
    
@login_required(login_url='login/')
@csrf_exempt
def cadastrar_itens_estoquev2(request, template_name = 'estoque_v2/cadastrar_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'CADASTRARITENS'
        categorias_itens = Categoria.objects.all()
        fornecedores = Fornecedor.objects.all()
        
        unid_medidas = Item.UNIDADES
     
        context = {
            'menu_ativo' : _menu_ativo,
            'categorias_itens' : categorias_itens,
            'fornecedores' : fornecedores,
            'unid_medidas' : unid_medidas,
         
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def filtrar_itens_nao_estoque(request, template_name = 'estoque_v2/itens/resultados_procurar_itens.html'):

    if request.method == 'GET':
        descricao = request.POST.get('descricao') or ''
        marca = request.POST.get('marca') or ''
        categoria = request.POST.get('categoria') or '-1'

        if categoria == '-1':    
            itens = Item.objects.all().filter(estocado=False).filter(descricao__icontains=descricao).filter(marca__icontains=marca)
        else:
            itens = Item.objects.all().filter(estocado=False).filter(descricao__icontains=descricao).filter(marca__icontains=marca).filter(categoria__pk=int(categoria))
    
        
        # print(f'-------------RESULTADO DO FILTER ---> {itens}')
       
        context = {
         
            'itens': itens
         
        }
     
 
        return render(request, template_name , context)
    
    
@login_required(login_url='login/')
@csrf_exempt
def detalhar_item_nao_estoquev2(request, pk, template_name = 'estoque_v2/itens/detalhar_item_nao_estoque.html'):

    if request.method == 'GET':
       
        item_atual = Item.objects.get(pk=pk)
    
       
        context = {
         
            'item': item_atual,
            
         
        }
     
 
        return render(request, template_name , context)
    
    
@login_required(login_url='login/')
@csrf_exempt
def editar_dados_item_estoquev2(request, pk, template_name = 'estoque_v2/itens/editar_item_estoque.html'):

    if request.method == 'GET':
        item_atual = Item.objects.get(pk=pk)
        categorias_itens = Categoria.objects.all()
        unid_medidas = Item.UNIDADES
        fornecedores = Fornecedor.objects.all()
       
        context = {
         
            'item': item_atual,
            'categorias_itens': categorias_itens,
            'unid_medidas': unid_medidas,
            'fornecedores': fornecedores,
        }
     
 
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def excluir_item_nao_estocado(request, pk):

    if request.method == 'GET':
        item_atual = Item.objects.get(pk=pk)  
        item_atual.delete()      
 
        return redirect('cadastrar_itens_estoquev2')
    
    
@login_required(login_url='login/')
@csrf_exempt
def estocar_item_nao_estoquev2(request, pk):

    if request.method == 'POST':
        item_atual = Item.objects.get(pk=pk)
        
        estocar = Estoque.objects.create(item=item_atual,
                                            quantidade=0)
        item_atual.estocado = True
        item_atual.save()
  
        return redirect('detalhar_item_de_estoque', pk=estocar.pk)
    
@login_required(login_url='login/')
@csrf_exempt
def add_novo_item_estoque(request):

    if request.method == 'POST':
        
        action = request.POST.get('action')
        
        
        #validação Descricao
        descricao = request.POST.get('descricao')
        if descricao == "" or descricao == None:
            response = HttpResponse('Erro: Insira uma DESCRIÇÃO')
            response['HX-Retarget'] = '#error_item'
            return response
        
        marca = request.POST.get('marca')
        
        #validação Categoria
        categoria = request.POST.get('categoria')
        if categoria == "" or categoria == '-1':
            response = HttpResponse('Erro: Selecione uma CATEGORIA.')
            response['HX-Retarget'] = '#error_item'
            return response
        else:
            categoria = Categoria.objects.get(pk=int(categoria))    
        
        
        #Peso
        peso = request.POST.get('peso')
        if not peso == "":
            peso = float(peso)
        else:
            peso = 0
        
        unid_medida = request.POST.get('unid_medida')
        
        #Preço
        preco = request.POST.get('preco')
        if not preco == "":
            preco = Decimal(preco)
        else:
            preco = 0
        
        
        #validação fornecedor
        fornecedor = request.POST.get('fornecedor')
        if fornecedor == "" or fornecedor == '-1':
            fornecedor = None
        else:
            fornecedor = Fornecedor.objects.get(pk=int(fornecedor))
        
        #Qtd_minima
        qtd_minima = request.POST.get('qtd_minima')
        if qtd_minima == ""  or qtd_minima == '0':
            response = HttpResponse('Erro: Inclua uma QUANTIDADE MÍNIMA > 0.')
            response['HX-Retarget'] = '#error_item'
            return response
            
        else:
            qtd_minima = Decimal(qtd_minima)
        
        imagemItem = request.FILES.get('imagemItem')
        print(f'----------------------------{request.FILES}--------------------------')
        
        if action == "Editar":
            
            item_atual = Item.objects.get(pk=int(request.POST.get('pkEditar')))
            item_atual.descricao=descricao
            item_atual.marca=marca
            item_atual.categoria=categoria
            item_atual.peso=peso
            item_atual.unid_medida=unid_medida
            item_atual.preco=preco
            item_atual.fornecedor=fornecedor
            item_atual.qtd_minima=qtd_minima
            item_atual.imagem=imagemItem
            item_atual.save()
            
            return redirect('detalhar_item_nao_estoquev2', pk=item_atual.pk)
         
        item_atual = Item.objects.create(
            descricao=descricao,
            marca=marca,
            categoria=categoria,
            peso = peso,
            unid_medida = unid_medida,
            preco=preco,
            fornecedor=fornecedor,
            qtd_minima = qtd_minima,
            imagem = imagemItem
            
        )
        
        if action == "Salvar":
            return redirect('cadastrar_itens_estoquev2')
        else:   
            estocar = Estoque.objects.create(item=item_atual,
                                                quantidade=0)
            item_atual.estocado = True
            item_atual.save()
    
            return redirect('detalhar_item_de_estoque', pk=estocar.pk)
            

#TODO CATEGORIAS
# ------------------------------------------------------------  CATEGORIAS---------------------------------------------------


@login_required(login_url='login/')
@csrf_exempt
def cadastrar_categoria_estoquev2(request, template_name = 'estoque_v2/categorias_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'CADASTRARCATEGORIAS'
        categorias_itens = Categoria.objects.all()
        categorias_ferramentas = CategoriaFerramenta.objects.all()
     
        context = {
            'menu_ativo' : _menu_ativo,
            'categorias_itens' : categorias_itens,
            'categorias_ferramentas' : categorias_ferramentas,
         
        }
        return render(request, template_name , context)
    

@login_required(login_url='login/')
@csrf_exempt
def add_nova_categoria_item_estoquev2(request):

    if request.method == 'POST':
        categoria = request.POST.get('categoria').upper()
        
        Categoria.objects.create(categoria = categoria)
     

        return redirect('cadastrar_categoria_estoquev2')
    

@login_required(login_url='login/')
@csrf_exempt
def add_nova_categoria_ferramenta_estoquev2(request):

    if request.method == 'POST':
        categoria = request.POST.get('categoria').upper()
        
        CategoriaFerramenta.objects.create(categoria = categoria)
     

        return redirect('cadastrar_categoria_estoquev2')
    
    

@login_required(login_url='login/')
@csrf_exempt
def excluir_categoria_estoquev2(request, pk, className):

    if request.method == 'GET':
        
        # print(f' ---- Instance: {className}')
        
        if className == 'Categoria':      
            Categoria.objects.get(pk = pk).delete()
            
        if className == 'CategoriaFerramenta':      
            CategoriaFerramenta.objects.get(pk = pk).delete()
     

        return redirect('cadastrar_categoria_estoquev2')
    
    

@login_required(login_url='login/')
@csrf_exempt
def editar_categoria_estoquev2(request, pk, className):

    if request.method == 'POST':
        categoria = request.POST.get('categoria').upper()
        
        if className == 'Categoria':      
            categoria_atual = Categoria.objects.get(pk = pk)
            categoria_atual.categoria = categoria
            categoria_atual.save()
            
        if className == 'CategoriaFerramenta':      
            categoria_atual = CategoriaFerramenta.objects.get(pk = pk)
            categoria_atual.categoria = categoria
            categoria_atual.save()
     

        return redirect('cadastrar_categoria_estoquev2')
    
    
    
    
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
        
    
    
    
    
    
    
    