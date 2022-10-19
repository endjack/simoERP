from re import I
from xml.dom import ValidationErr
from requests import delete
from financeiro.filters import ContasFilter
from financeiro.forms import *
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.urls.base import reverse
from django.db.models import DecimalField, ExpressionWrapper, F, Sum
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.core.cache import cache
from django.http.response import HttpResponseRedirect, HttpResponse
from django_htmx.http import trigger_client_event
from .validations import validar_descricao_nota, validar_item_nota

END_LOG = '\033[0;0m'
LOG_DANGER= '\033[31m'

#VARIÁVEIS GLOBAIS
valor_total_pre_save_a_vista = None
resumo_listagem_boletos = list()
pode_salvar_boleto = False
id_nota_em_processo = None

 #TODO excluir boleto individual
 #TODO excluir Nota Completa  <-----
 #TODO Excluir itens salvar editar não atualiza os itens
 #TODO página de editar os boletos antes de excluir
 #TODO Editar (colocar o itens para serem add no final)


#GET /resumo-do-dia/
@login_required(login_url='login/')
def home_resumo_do_dia(request):
    """
    Retorna a página inicial do financeiro
    """
    template_name = 'financeiro/resumo-do-dia.html'
    today_date = datetime.now()
    
    if request.method == 'GET':
        try:
            contas_do_dia = ContaBoleto.objects.filter(data_vencimento=today_date).filter(pago=False)
            boletos_em_atrazo = ContaBoleto.objects.filter(data_vencimento__range=[datetime.min, today_date - timedelta(days=1)]).filter(pago=False)

            total_valor = contas_do_dia.aggregate(total_valor=Sum('valor'))['total_valor']
            total_valor_em_atraso = boletos_em_atrazo.aggregate(total_valor=Sum('valor'))['total_valor']
    
            #VALIDAÇÃO 'total_valor'
            if not total_valor:
                total_valor = 0
                
            if not total_valor_em_atraso:
                total_valor_em_atraso = 0
        
            context = {
                'contas_do_dia': contas_do_dia,
                'boletos_em_atrazo': boletos_em_atrazo, 
                'total': locale.currency(total_valor, grouping=True),
                'total_valor_em_atraso': locale.currency(total_valor_em_atraso, grouping=True),
                }
        
            return render(request, template_name , context)
        
        except ContaPagamento.DoesNotExist:
            raise Http404("ERRO: Conta não existe!")


#GET /contas-a-pagar/
@login_required(login_url='login/')
def contas_a_pagar(request): 
    template_name = 'financeiro/contas-a-pagar.html'
    
    if request.method == 'GET':
        try:
            context = {
                'filter': ContasFilter()
                }
        
            return render(request, template_name , context)
        
        except ContaPagamento.DoesNotExist:
            raise Http404("ERRO: Conta não existe!")

    
#GET /contas-a-pagar/inserir     
@login_required(login_url='login/')
def inserir_nova_conta_a_pagar(request):
    global id_nota_em_processo
 
    validar_descricao_nota['data_emissao'] = False 
    validar_descricao_nota['centro_de_custo'] = False
    
    template_name = 'financeiro/fragmentos/inserir-conta-a-pagar.html'
    
    if request.method == 'GET':
        form = DescricaoForm()
        fornecedores = Fornecedor.objects.all()
        nota = NotaCompleta.objects.none()
        
        try:   
            if id_nota_em_processo:
                nota = NotaCompleta.objects.get(pk = int(id_nota_em_processo))
                nota.itens.all().delete()
                nota.delete()
                id_nota_em_processo = None
                
                print('\033[31m'+'------------------- DELETADA CONTA TEMPORÁRIA --------------------'+'\033[0;0m') 
                    
            
            context = {
            'form':form,
            'fornecedores': fornecedores,
            'notacompleta': nota,
            }
            
            return render(request, template_name , context)
        
        except ContaPagamento.DoesNotExist:
            raise Http404("ERRO: Conta não existe!")


#GET /contas-a-pagar/modal-itens    
@login_required(login_url='login/')
def modal_itens_conta_a_pagar(request, **kwargs):
    template_name = 'financeiro/fragmentos/inserir-item.html'

    validar_item_nota['descricao'] = False
    validar_item_nota['qtd'] = False
    validar_item_nota['valor'] = False
    
    
    if request.method == 'GET':
        form = ItensNotaForm()
        
        context = {
            'form':form,
            'id_nota_atual': kwargs.get('pk')
        }
            
        return render(request, template_name , context)


#POST /contas-a-pagar/inserir-itens
@login_required(login_url='login/')
def inserir_itens_conta_a_pagar(request, **kwargs):
    global id_nota_em_processo
    
    pk = kwargs.get('pk')
  

    template_name = 'financeiro/fragmentos/itens-inseridos-tabela.html'
    
    if request.method == 'POST':
        form = ItensNotaForm(request.POST)
        
        if pk:
            id_nota = pk
        else:    
            id_nota = id_nota_em_processo
        
        
        if form.is_valid():
            form.instance.valor = request.POST.get('valor').replace(".","").replace(",",".")
            item = form.save()
            print('\033[32m'+f'------------------- ITEM CRIADO: {item.pk} --------------------'+'\033[0;0m') 
        else:
            template_name = 'financeiro/fragmentos/inserir-conta-a-pagar.html'
            response = render(request, template_name , {'erroItem': 'Erro ao Inserir Item', 'form': DescricaoForm()}) 
            response['HX-Retarget'] = 'body'
            response['HX-Swap'] = 'outerHTML'
            return response
        
        
        if id_nota:
            notacompleta = NotaCompleta.objects.get(pk = int(id_nota))
            notacompleta.itens.add(item)
        else:
            notacompleta = NotaCompleta.objects.create()
            print('\033[32m'+f'------------------- CONTA CRIADA {notacompleta.pk} --------------------'+'\033[0;0m') 
            notacompleta.itens.add(item)
        
        print('\033[32m'+f'------------------- ITEM {item.pk} (VALOR: {item.valor }) ADICIONADO A CONTA: {notacompleta.pk} --------------------'+'\033[0;0m') 
        print('\033[32m'+f'------------------- VALOR TOTAL ITENS: {notacompleta.itens.all().aggregate(total_itens = Sum(ExpressionWrapper(F("qtd") *  F("valor"),  output_field=DecimalField())))["total_itens"]} ADICIONADO A CONTA: {notacompleta.pk} --------------------'+'\033[0;0m') 
    

        id_nota_em_processo = notacompleta.pk
    
        context = {
            'notacompleta': notacompleta,
        }
        response = render(request, template_name , context)
        response['HX-Trigger'] = 'itemAddNota'                   
        return response


@login_required(login_url='login/')
def excluir_item_conta_a_pagar(request, pk):
    global id_nota_em_processo
    template_name = 'financeiro/fragmentos/itens-inseridos-tabela.html'
    
    if request.method == 'POST':
        try:
            ItensNota.objects.filter(pk=pk).delete() 
            print('\033[31m'+'------------------- ITEM DELETADO --------------------'+'\033[0;0m')
            notacompleta = NotaCompleta.objects.get(pk = int(id_nota_em_processo))
            
            context = {
                'notacompleta': notacompleta,
            }
                        
            return render(request, template_name , context)
        except (ValueError, TypeError):
            HttpResponse("Erro ao Deletar Item")
    else:          
        HttpResponse("Erro ao Deletar Item")


@login_required(login_url='login/')
@csrf_exempt
def add_descricao_nota(request):
    template_name = 'financeiro/fragmentos/add-descricao-nota.html'
    try:
       
    
        context = {
            
            }
    
        return render(request, template_name , context)
    
    except ContaPagamento.DoesNotExist:
        raise Http404("ERRO: Conta não existe!")

   
@login_required(login_url='login/')
@csrf_exempt
def filtro_contas_a_pagar(request):
    template_name = 'financeiro/fragmentos/resultados-contas-a-pagar.html'
    
    try:
        descricao = request.GET.get('descricao') or ''
        fornecedor = request.GET.get('fornecedor') or ''
        initial_date = request.GET.get('data') or datetime.min   # datetime.min is 1
        end_date = request.GET.get('data_f') or datetime.max  # datetime.max is 9999
        
        if request.GET.get('check_pago') == 'on' and request.GET.get('check_nao_pago') != 'on':
             objects = ContaBoleto.objects.all().filter(pago=True).filter(
                Q(conta__saida__fornecedor__nome__icontains=fornecedor) | Q(conta__saida__fornecedor__razao_social__icontains=fornecedor),
                Q(data_vencimento__range=[initial_date, end_date]),
                Q(conta__saida__nota_fiscal__icontains=descricao) | Q(doc__icontains=descricao))
        
        elif request.GET.get('check_nao_pago') == 'on' and request.GET.get('check_pago') != 'on':
            objects = ContaBoleto.objects.all().filter(pago=False).filter(
                Q(conta__saida__fornecedor__nome__icontains=fornecedor) | Q(conta__saida__fornecedor__razao_social__icontains=fornecedor),
                Q(data_vencimento__range=[initial_date, end_date]),
                Q(conta__saida__nota_fiscal__icontains=descricao) | Q(doc__icontains=descricao))
               
        else:
            objects = ContaBoleto.objects.all().filter(
                Q(conta__saida__fornecedor__nome__icontains=fornecedor) | Q(conta__saida__fornecedor__razao_social__icontains=fornecedor),
                Q(data_vencimento__range=[initial_date, end_date]),
                Q(conta__saida__nota_fiscal__icontains=descricao) | Q(doc__icontains=descricao))
                       
     
             
        if objects:
            total_valor = objects.aggregate(total_valor = Sum('valor'))['total_valor']
            
            context = {
                'contas_atrasadas': objects,
                'total_acresc': 0,
                'total': total_valor,
                }
            
        else:
            context = {
                'contas_atrasadas': objects,
                'total_acresc': 0,
                'total': 0,
                }
        
    
     
        return render(request, template_name , context)
    
    except ContaBoleto.DoesNotExist:
        raise Http404("ERRO: Conta não existe!")


@login_required(login_url='login/')
@csrf_exempt
def get_fornecedores(request):
    template_name = 'financeiro/fragmentos/options-select-fornecedores.html'
    if request.method == 'GET':
        query = request.GET.get('fornecedor')
        fornecedores = Fornecedor.objects.filter(pk__icontains=query).only('nome').only('doc').only('pk') | Fornecedor.objects.filter(nome__icontains=query).only('nome').only('doc').only('pk') | Fornecedor.objects.filter(razao_social__icontains=query).only('nome').only('doc').only('pk')
     
        
        if not fornecedores:
            response = HttpResponse('Não encontrado Fornecedor/Razão Social')
            response['HX-Trigger'] = 'errorFornecedores'   
            response['HX-Retarget'] = '#error_fornecedor'
            response['HX-Swap'] = 'innerHTML'
            return response
        
        context = {
               'fornecedores':fornecedores,
           }
        
        response = render(request, template_name , context)
        response['HX-Trigger'] = 'okFornecedores'            
        return response


@login_required(login_url='login/')
@csrf_exempt
def get_error(request):
    template_name = 'errors/error-input.html'           
    return render(request, template_name , {'ErrorMessage':'Error de Fornecedor'})


@login_required(login_url='login/')
@csrf_exempt
def get_forma_de_pagamento(request):
    formaPagamento = request.GET.get('selectFPagamento')
    
    if formaPagamento == '1':
        template_name = 'financeiro/fragmentos/pagamentos/vista-forma-de_pagamento.html'
        formPagamento = PagamentoVistaForm()
    elif formaPagamento == '2':
        template_name = 'financeiro/fragmentos/pagamentos/boleto-forma-de_pagamento.html'
        formPagamento = PagamentoVistaForm()
    else:
        template_name = 'financeiro/fragmentos/pagamentos/aberto_forma-de_pagamento.html'
        formPagamento = PagamentoVistaForm()
  
    
    context = {
       'formPagamento': formPagamento,
    }
    response = render(request, template_name , context)         
    return response
  

@login_required(login_url='login/')
@csrf_exempt
def salvar_nota_completa(request):
    global id_nota_em_processo
    
    if request.method == 'POST':
        try:
            # id_fornecedor = request.POST.get('fornecedor').split("· ID")[1]
            id_fornecedor = request.POST.get('fornecedor')
            fornecedor = Fornecedor.objects.get(id=int(id_fornecedor))
            form = DescricaoForm(request.POST)
            form.instance.fornecedor = fornecedor
            
            
            if form.is_valid():
                descricao_nota = form.save()
                print('\033[32m'+f'------------------- DESCRIÇÃO DE NOTA CRIADO: {descricao_nota.pk} --------------------'+'\033[0;0m') 
            else:
                response = HttpResponse(f"Erro ao Criar Nota Completa. Dados do Form: {form.errors}")
                response['HX-Retarget'] = 'body'
                response['HX-Swap'] = 'outerHTML'
                return response
                    
            id_nota = id_nota_em_processo
           
            if id_nota:
                notacompleta = NotaCompleta.objects.get(pk = int(id_nota))
                notacompleta.saida = descricao_nota
                notacompleta.usuario = request.user
                notacompleta.valor = notacompleta.itens.all().aggregate(total_itens = Sum(ExpressionWrapper(F("qtd") *  F("valor"),  output_field=DecimalField())))["total_itens"] #somando todos os valores dos itens desta nota
                print('\033[32m'+f'------------------- VALOR TOTAL ITENS Nº {notacompleta.valor} ADD A NOTA: {notacompleta.pk} --------------------'+'\033[0;0m') 
                notacompleta.save()
                print('\033[32m'+f'------------------- DESCRIÇÃO Nº {descricao_nota.pk} ADD A NOTA: {notacompleta.pk} --------------------'+'\033[0;0m') 
               
               
                id_nota_em_processo = None     
                return HttpResponseRedirect(f'nota/{notacompleta.pk}')
            else:
                raise NotaCompleta.DoesNotExist()
        
            
        except:
            response = HttpResponse(f"Erro no Formulário")
            response['HX-Retarget'] = 'body'
            response['HX-Swap'] = 'outerHTML'
            return response
          
          
@login_required(login_url='login/')
@csrf_exempt
def ver_nota_completa(request, pk):
    global valor_total_pre_save_a_vista
    global resumo_listagem_boletos
    
    resumo_listagem_boletos = list()
    
    template_name = 'financeiro/detalhes-saida.html'
    nota_atual = NotaCompleta.objects.get(pk=pk)
    valor_total_pre_save_a_vista = nota_atual.valor
   
    pagamento = None
    boletos = None
    situacao = ""
    
   
    if nota_atual.forma_pagamento == 1: #a vista
        pagamento = PagamentoVista.objects.get(conta=nota_atual)
        situacao = 'pagoVista'
    if nota_atual.forma_pagamento == 2: #por boleto
        boletos = ContaBoleto.objects.filter(conta=nota_atual)
        if boletos: 
            boletos_em_atrazo = ContaBoleto.objects.filter(conta=nota_atual).filter(pago=False).filter(data_vencimento__range=[datetime.min, datetime.now() - timedelta(days=1)])
            if boletos_em_atrazo:
                situacao = 'pagoBoletoAtrasado'
            else:
                situacao = 'pagoBoletoEmDia'    
        else:
            situacao = 'pagoBoletoFinalizado'   #TODO RESOLVER QUANDO TODOS OS BOLETOS FICAREM PAGOS, DAR NOTA FISCAL PAGAMENTO FINALIZADO
            
    print(f'------------------------------- {situacao}')
    context = {
            'nota_atual': nota_atual,
            'pagamento': pagamento,
            'situacao': situacao,
            'boletos': boletos
        }                       
    
    
    return render(request, template_name , context)


@login_required(login_url='login/')
def editar_saida(request, pk):
 
    validar_descricao_nota['data_emissao'] = True 
    validar_descricao_nota['centro_de_custo'] = True
    validar_descricao_nota['itens_nota'] = True
    
    template_name = 'financeiro/fragmentos/inserir-conta-a-pagar.html'
    
    if request.method == 'GET':
        nota = get_object_or_404(NotaCompleta, pk=pk)
        fornecedores = Fornecedor.objects.all()
        
        initial_dict = {
           'nota_fiscal': nota.saida.nota_fiscal,
           'data_emissao': nota.saida.data_emissao,
           'centro_de_custo': nota.saida.centro_de_custo,
           'descricao': nota.saida.descricao,
           
        }
        form = DescricaoForm(initial=initial_dict, instance=nota)
        
        
   
        context = {
        'form':form,
        'notacompleta' : nota,
        'fornecedores' : fornecedores,
        'fornecedor_atual' : nota.saida.fornecedor.pk,
        'edit': True
        
        }
        
        return render(request, template_name , context)
    
    
@login_required(login_url='login/')
@csrf_exempt
def salva_edicao_saida(request, pk):
 
    notacompleta = get_object_or_404(NotaCompleta, pk=pk)
    id_fornecedor = request.POST.get('fornecedor')
    fornecedor = Fornecedor.objects.get(id=int(id_fornecedor))

    form = DescricaoForm(request.POST or None)   
    form.instance.fornecedor = fornecedor 
    
    if form.is_valid():
        descricao_nota = form.save()
        notacompleta.saida = descricao_nota
        notacompleta.valor = notacompleta.itens.all().aggregate(total_itens = Sum(ExpressionWrapper(F("qtd") *  F("valor"),  output_field=DecimalField())))["total_itens"] #somando todos os valores dos itens desta nota
        notacompleta.save()
        
    return HttpResponseRedirect(f'/contas-a-pagar/nota/{notacompleta.pk}')
        
    
@login_required(login_url='login/')
@csrf_exempt
def get_valor_total(request):
    global valor_total_pre_save_a_vista
    valor_total_pre_save_a_vista = 0
    #Retirando a máscara de moeda para deixar os valores em numeros possiveis para serem somados
    valor_nota = request.GET.get('valor_').replace('.', '').replace(',', '.')
    valor_acrescimo =  request.GET.get('valor_acrescimo').replace('.', '').replace(',', '.')
    
    if valor_acrescimo == "":
        valor_acrescimo = 0
    
    locale.setlocale(locale.LC_MONETARY, 'pt_BR.UTF-8')  
    valor_total =  float(valor_nota) + float(valor_acrescimo)
    valor_total_pre_save_a_vista = valor_total
    print(f'Valor Total = {valor_total_pre_save_a_vista}')

    return HttpResponse(locale.currency(valor_total))


@login_required(login_url='login/')
@csrf_exempt
def get_resumo_boleto_mensal(request, pk):
    global resumo_listagem_boletos
    global pode_salvar_boleto
    
    pode_salvar_boleto = False
    template_name = 'financeiro/fragmentos/pagamentos/resumo-boletos-pagamento.html'
    nota_atual = NotaCompleta.objects.get(pk=pk)
    valor_total = 0
    
    #CRIANDO RESUMO ----------
    resumo_listagem_boletos = list()
    
    #VALIDAÇÃO DO NUMERO DE PARCELAS
    try: 
        n_parcelas = request.POST.get('n_parcelas')
        n_parcelas = int(n_parcelas)
        if not n_parcelas >= 1 or n_parcelas == "":
            template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
            response = render(request, template_name=template_name, context={'errorMensagem': 'Número de Parcelas INVÁLIDO'})
            response['HX-Trigger'] = "buttonError"
            pode_salvar_boleto = False
            return response       
    except ValueError:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Número de Parcelas INVÁLIDO'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        return response    
    #VALIDÇÃO DO VALOR
    try: 
        valor_parcelas = float(request.POST.get('valor_parcelas').replace('.', '').replace(',', '.'))
        if valor_parcelas <= 0:
            template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
            response = render(request, template_name=template_name, context={'errorMensagem': 'Valor INVÁLIDO'})
            response['HX-Trigger'] = "buttonError"
            pode_salvar_boleto = False
            return response        
    except ValueError:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Valor INVÁLIDO'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        return response        
    #VALIDÇÃO DA DATA
    try: 
        data_1_parcela = request.POST.get('data_1_parcela')
        data_1_parcela = datetime.strptime(data_1_parcela, '%Y-%m-%d')
        if data_1_parcela == "":
            template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
            response = render(request, template_name=template_name, context={'errorMensagem': 'Data INVÁLIDA'})
            response['HX-Trigger'] = "buttonError"
            pode_salvar_boleto = False
            return response
        
    except ValueError:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Data INVÁLIDA'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        return response
    
    #NUMERO DO DOCUMENTO
    doc_parcelas = request.POST.get('doc_parcela')
        

    for n in range(int(n_parcelas)):
        parcela = {'parcela':n+1, 'valor':locale.currency(valor_parcelas, grouping=True).replace('R$ ',""), 'data_vencimento':data_1_parcela + timedelta(days=n*30)}
        
        if not doc_parcelas == "":
            parcela['doc']= f'{doc_parcelas}-{n+1}'
        else:
            parcela['doc']= ''
            
        resumo_listagem_boletos.append(parcela)
        valor_total += valor_parcelas

    
    context = {
        'resumo': resumo_listagem_boletos,
        'num_parcelas': n_parcelas,
        'valor_total': locale.currency(valor_total, grouping=True),
        'nota_atual': nota_atual
    }   
    response = render(request, template_name , context)
    response['HX-Trigger'] = "buttonSave"
    pode_salvar_boleto = True
    return response


@login_required(login_url='login/')
@csrf_exempt
def atualizar_resumo_boleto_mensal(request, pk):
    global resumo_listagem_boletos
    global pode_salvar_boleto
    
    
    qnt_parcelas = int(request.POST.get('num_parcelaA'))
    doc_parcelas = request.POST.getlist('doc_parcelaA')
    
    print(f'----------------{doc_parcelas}')
    
    
    # #VALIDAÇÃO DO VALOR
    try: 
        valor_parcelas = request.POST.getlist('valor_parcelaA')
        if len(valor_parcelas) < qnt_parcelas:
            template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
            response = render(request, template_name=template_name, context={'errorMensagem': 'Valor VAZIO'})
            response['HX-Trigger'] = "buttonError"
            pode_salvar_boleto = False
            return response 
        else:
            for valor in valor_parcelas:
                valor = float(valor.replace('.', '').replace(',', '.'))
    
                if valor <= 0:
                    template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
                    response = render(request, template_name=template_name, context={'errorMensagem': 'Valor INVÁLIDO'})
                    response['HX-Trigger'] = "buttonError"
                    pode_salvar_boleto = False
                    return response        
    except ValueError:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Valor INVÁLIDO'})
        pode_salvar_boleto = False
        return response         
    
    #VALIDÇÃO DA DATA
    try: 
        datas_parcelas = request.POST.getlist('data_parcelaA')
        if len(datas_parcelas) < qnt_parcelas:
            template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
            response = render(request, template_name=template_name, context={'errorMensagem': 'Data VAZIA'})
            response['HX-Trigger'] = "buttonError"
            pode_salvar_boleto = False
            return response 
        else:
            for data in datas_parcelas:
                if data == "":
                    template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
                    response = render(request, template_name=template_name, context={'errorMensagem': 'Data INVÁLIDA'})
                    response['HX-Trigger'] = "buttonError"
                    pode_salvar_boleto = False
                    return response    
        
    except ValueError:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Data INVÁLIDA'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        return response
    
    
    #GUARDANDO E ENVIADO OS DADOS NOVAMENTE
    template_name = 'financeiro/fragmentos/pagamentos/resumo-boletos-pagamento.html'
    resumo_listagem_boletos = list()
    valor_total = 0
    nota_atual = NotaCompleta.objects.get(pk=pk)
  
    
    for n in range(int(qnt_parcelas)):
        valor = float(valor_parcelas[n].replace('.', '').replace(',', '.'))
        data = datetime.strptime(datas_parcelas[n], '%Y-%m-%d')
        parcela = {'parcela':n+1, 'valor':locale.currency(valor, grouping=True).replace('R$ ',""), 'data_vencimento':data}
        
        print(doc_parcelas[n])
        
        #TODO FIX resolver atualização de boletos no resumo, o doc vazio não entra na lista
        # if len(doc_parcelas) > 0:
        #     if doc_parcelas[n] != "":
        #         parcela['doc']= doc_parcelas[n]
        #     else:
        #         parcela['doc']= ''
        # else:
        #     parcela['doc']= ''
                
        resumo_listagem_boletos.append(parcela)
        valor_total += valor
    
    
    context = {
        'resumo': resumo_listagem_boletos,
        'num_parcelas': qnt_parcelas,
        'valor_total': locale.currency(valor_total, grouping=True),
        'nota_atual': nota_atual
    }   
    
    response = render(request, template_name , context)
    response['HX-Trigger'] = "buttonSave"
    pode_salvar_boleto = True
    return response

  
@login_required(login_url='login/')
@csrf_exempt
def salvar_boletos_mensal(request, pk):
    global pode_salvar_boleto
    global resumo_listagem_boletos
    
    print(resumo_listagem_boletos)
    
    if not pode_salvar_boleto:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Erro ao Salvar! Tentar novamente.'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        return response
    
    #SALVANDO BOLETOS NO BANCO
    try:
        qnt_parcelas = int(request.POST.get('num_parcelaA'))
        nota_atual = NotaCompleta.objects.get(pk=pk)
        
        for n in range(qnt_parcelas):
            ContaBoleto.objects.create(conta = nota_atual,
                                    parcela =  n+1,
                                    total_parcelas =  qnt_parcelas,
                                    doc = resumo_listagem_boletos[n]['doc'],
                                    valor = resumo_listagem_boletos[n]['valor'].replace(".","").replace(",","."),
                                    data_vencimento = resumo_listagem_boletos[n]['data_vencimento'],
                                    usuario = request.user,
                                    obs = "")
        
        nota_atual.pago = True
        nota_atual.forma_pagamento = 2 #por Boletos
        nota_atual.save()
        
        pode_salvar_boleto = False #resetar variavel
        return redirect(reverse('ver-nota-completa', kwargs={'pk':pk}))
    
    except (ValueError, ValidationErr):
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Erro ao Salvar! Tentar novamente.'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        return response    

        
@login_required(login_url='login/')
@csrf_exempt
def pagar_nota_a_vista(request, pk): 
    global valor_total_pre_save_a_vista
    print(f'Valor Total pago = {valor_total_pre_save_a_vista}')

    nota_atual = NotaCompleta.objects.get(pk=pk)
    form = PagamentoVistaForm(request.POST)
    
    if request.POST.get('valor_acrescimo'):
        valor_acrescimo =  request.POST.get('valor_acrescimo').replace('.', '').replace(',', '.')
    else:
        valor_acrescimo = 0
    
    #realizar pagamento
    if form.is_valid():
        form.instance.usuario = request.user
        form.instance.valor_pago = float(valor_total_pre_save_a_vista)
        form.instance.acrescimo = float(valor_acrescimo)
        nota_atual.pago = True
        nota_atual.forma_pagamento = 1  #tipo pagamento == 1 (a vista)
        nota_atual.save()
        form.instance.conta = nota_atual
        form.save()
        # print(f"VALIDO - {request.POST}")
        
        
    return redirect(reverse('ver-nota-completa', kwargs={'pk':nota_atual.pk}))


@login_required(login_url='login/')
@csrf_exempt
def excluir_pagamento_a_vista(request, pk): 

    nota_atual = NotaCompleta.objects.get(pk=pk)
    pagamento_vista = PagamentoVista.objects.filter(conta=nota_atual)
    
    try:
        pagamento_vista.delete()
        nota_atual.pago = False
        nota_atual.forma_pagamento = 0 #em aberto
        nota_atual.save()
    except:
        print('erro ao Excluir')
        
    return redirect(reverse('ver-nota-completa', kwargs={'pk':nota_atual.pk}))


@login_required(login_url='login/')
@csrf_exempt
def excluir_pagamento_boletos(request, pk):

    nota_atual = NotaCompleta.objects.get(pk=pk)
    pagamento_boletos = ContaBoleto.objects.filter(conta=nota_atual)
    print(pagamento_boletos)
    
    try:
        pagamento_boletos.delete()
        nota_atual.pago = False
        nota_atual.forma_pagamento = 0 #em aberto
        nota_atual.save()
    except:
        print('erro ao Excluir')
        
    return redirect(reverse('ver-nota-completa', kwargs={'pk':nota_atual.pk}))


@login_required(login_url='login/')
@csrf_exempt
def editar_pagamento_boletos(request, pk, template_name="financeiro/fragmentos/pagamentos/resumo-boletos-pagamento.html"):
    global pode_salvar_boleto
    
    pode_salvar_boleto = True
    
    nota_atual = NotaCompleta.objects.get(pk=pk)
    resumo = ContaBoleto.objects.filter(conta=nota_atual)
    total_valor = resumo.aggregate(total_valor=Sum('valor'))['total_valor']
   
    context = {
        'resumo': resumo,
        'nota_atual': nota_atual,
        'num_parcelas': resumo.count(),
        'valor_total': locale.currency(total_valor, grouping=True),
        'nota_atual': nota_atual
    }     
    
    return render(request, template_name , context)


@login_required(login_url='login/')
@csrf_exempt
def excluir_boleto_unico(request, pk, nota):

    boleto = ContaBoleto.objects.get(pk=pk)
    boleto.delete()
    
    
    nota_atual = NotaCompleta.objects.get(pk=nota)
    boletos = ContaBoleto.objects.filter(conta = nota_atual)
    
    if boletos:
        #REORDENAR PARCELAS
        num = 1
        for item in boletos:
            item.parcela = num
            num=num+1
            item.save()
    else:   
    #CASO CONTRARIO RETIRAR PAGAMENTO
        nota_atual.pago = False
        nota_atual.forma_pagamento = 0
        nota_atual.save()
    

    return HttpResponseRedirect(f'/contas-a-pagar/nota/{nota}')

@login_required(login_url='login/')
@csrf_exempt
def editar_pagamento_boleto(request, pk, nota, template_name="financeiro/fragmentos/editar-pagamento-boleto.html"):

    boleto = ContaBoleto.objects.get(pk=pk)
    nota_atual = NotaCompleta.objects.get(pk=nota)
    context = {
        'boleto': boleto,
        'nota_atual': nota_atual
    } 
    return render(request, template_name , context)


@login_required(login_url='login/')
@csrf_exempt
def salvar_editar_pagamento_boleto(request, pk, nota):

    boleto = ContaBoleto.objects.get(pk=pk)
   
    
    doc = request.POST.get('doc')
    data = request.POST.get('data_vencimento')
    valor = request.POST.get('valor').replace(".","").replace(",",".")
  
    if not data or data == "":
        response = HttpResponse('<span style="color:red"><i>Data Inválida</i></span>')
        response['HX-Retarget'] = '#error_data'
        response['HX-Swap'] = 'innerHTML'
        return response
    else:
        boleto.data_vencimento = datetime.strptime(data, '%Y-%m-%d') or boleto.data_vencimento
    
    if not valor or valor == "" or float(valor) <= 0:
        response = HttpResponse('<span style="color:red"><i>Valor Inválido</i></span>')
        response['HX-Retarget'] = '#error_valor'
        response['HX-Swap'] = 'innerHTML'
        return response
    else:
        boleto.valor = float(valor)
        
  
    boleto.doc = doc
    boleto.save()
    return HttpResponseRedirect(f'/contas-a-pagar/nota/{nota}')
    
        
@login_required(login_url='login/')
@csrf_exempt
def editar_pagamento_vista(request, pk, template_name="financeiro/fragmentos/editar-pagamento-vista.html"):

    nota_atual = NotaCompleta.objects.get(pk=pk)
    pagamento = PagamentoVista.objects.get(conta=nota_atual)

    context = {
        'pagamento': pagamento,
        'nota_atual':nota_atual
 
    }     
    
    return render(request, template_name , context)


@login_required(login_url='login/')
@csrf_exempt
def salvar_editar_pagamento_vista(request, pk, nota):

    pagamento = PagamentoVista.objects.get(pk=pk)
    data = request.POST.get('data_pagamento')
    acrescimo = request.POST.get('valor_acrescimo').replace(".","").replace(",",".")
    
    if not data or data == "":
        response = HttpResponse('<span style="color:red"><i>Data Inválida</i></span>')
        response['HX-Retarget'] = '#error_data'
        response['HX-Swap'] = 'innerHTML'
        return response
    else:
        pagamento.data_pagamento = datetime.strptime(data, '%Y-%m-%d') or pagamento.data_pagamento
        
    if not acrescimo or acrescimo == "":
        pagamento.acrescimo = float(0)
        pagamento.valor_pago = pagamento.conta.valor
    else:
        pagamento.acrescimo = float(acrescimo)
        pagamento.valor_pago = float(pagamento.conta.valor) + pagamento.acrescimo
        
    
    
    pagamento.save()
    return HttpResponseRedirect(f'/contas-a-pagar/nota/{nota}')


@login_required(login_url='login/')
@csrf_exempt
def excluir_saida(request, pk):
    if request.method == "DELETE":
        nota_atual = NotaCompleta.objects.get(pk=pk)

        try:
            nota_atual.saida.delete()
            nota_atual.itens.delete() #não funciona .clear()
            nota_atual.delete()
        except:
            print('erro ao Excluir')
            
        return HttpResponse("excluir com Sucesso")
    

@login_required(login_url='login/')
@csrf_exempt
def selecionar_forma_de_pagamento(request, pk):
    template_name = 'financeiro/fragmentos/pagamentos/modal-ver-formas-pagamentos.html'
    nota_atual = NotaCompleta.objects.get(pk=pk)
    form = PagamentoVistaForm()
    
    context = {
        'nota_atual': nota_atual,
        'form' : form
    }     
    
    return render(request, template_name , context)

  
@login_required(login_url='login/')
@csrf_exempt
def forma_de_pagamento_selecionada(request, pk):
    forma_escolhida = request.GET.get('select-forma-pagamento')
    nota_atual = NotaCompleta.objects.get(pk=pk)

    
 
    if forma_escolhida == '0':
        template_name = 'financeiro/fragmentos/pagamentos/vista-forma-de-pagamento.html'
        form = PagamentoVistaForm()
    elif forma_escolhida == '1':
        template_name = 'financeiro/fragmentos/pagamentos/boleto-forma-de-pagamento.html'
        form = PagamentoVistaForm()
    else:
        template_name = 'financeiro/fragmentos/pagamentos/aberto-forma-de-pagamento.html'
        form = PagamentoVistaForm()
        
    
    context = {
        'nota_atual': nota_atual,
        'form' : form, 
    }     
        
    response = render(request, template_name , context)
    response['HX-Trigger'] = "buttonError"
    return response


@login_required(login_url='login/')
@csrf_exempt
def pagar_boleto_unico(request, pk, nota, template_name="financeiro/fragmentos/pagamentos/pagar-boleto-unico.html"):
    
    nota_atual = NotaCompleta.objects.get(pk=nota)
    boleto = ContaBoleto.objects.get(pk=pk)
    
    context = {
        'nota_atual': nota_atual,
        'boleto' : boleto
    }     
    
    return render(request, template_name , context)

@login_required(login_url='login/')
@csrf_exempt
def salvar_pagar_boleto_unico(request, pk, nota, template_name="financeiro/fragmentos/pagamentos/pagar-boleto-unico.html"):
    
    nota_atual = NotaCompleta.objects.get(pk=nota)
    boleto = ContaBoleto.objects.get(pk=pk)  
    
    data = request.POST.get('data_pagamento')
    obs = request.POST.get('obs')
    acrescimo = request.POST.get('valor_acrescimo').replace(".","").replace(",",".")
    
    pagamento = PagamentoBoleto.objects.create(conta = nota_atual, boleto = boleto, usuario = request.user, obs = obs)
    
    if not data or data == "":
        response = HttpResponse('<span style="color:red"><i>Data Inválida</i></span>')
        response['HX-Retarget'] = '#error_data'
        response['HX-Swap'] = 'innerHTML'
        return response
    else:
        pagamento.data_pagamento = datetime.strptime(data, '%Y-%m-%d') or pagamento.data_pagamento
    
    if not acrescimo or acrescimo == "":
        pagamento.acrescimo = float(0)
        
    else:
        pagamento.acrescimo = float(acrescimo)
        pagamento.valor_pago = float(boleto.valor) + pagamento.acrescimo
    
    pagamento.save()
    
    boleto.pago = True
    boleto.save()
    return HttpResponseRedirect(f'/contas-a-pagar/nota/{nota}')

@login_required(login_url='login/')
@csrf_exempt
def excluir_pagamento_boleto_unico(request, pk, nota):
    
    boleto = ContaBoleto.objects.get(pk=pk)  
    pagamento = PagamentoBoleto.objects.get(boleto = boleto)
    
    pagamento.delete()
    
    boleto.pago = False
    boleto.save()
    return HttpResponseRedirect(f'/contas-a-pagar/nota/{nota}')