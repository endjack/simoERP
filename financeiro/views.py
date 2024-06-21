from django.core.cache import cache
from xml.dom import ValidationErr
from decimal import Decimal
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
from django.http.response import HttpResponseRedirect, HttpResponse
from django_htmx.http import trigger_client_event, HttpResponseClientRedirect
from .validations import validar_item_nota
from simo.utils import gerar_pdf_by_template
from django.contrib.sites.shortcuts import get_current_site


END_LOG = '\033[0;0m'
LOG_DANGER= '\033[31m'

#VARIÁVEIS GLOBAIS
valor_total_pre_save_a_vista = None
resumo_listagem_boletos = list()
pode_salvar_boleto = False
id_nota_em_processo = None

 


#GET /resumo-do-dia/
@login_required(login_url='login/')
def home_resumo_do_dia(request, template_name = 'financeiro/resumo-do-dia.html'):
    """
    Retorna a página inicial do financeiro
    """
    today_date = datetime.now()
    
    if request.method == 'GET':
        try:
            contas_do_dia_boleto = ContaBoleto.objects.filter(data_vencimento=today_date).filter(pago=False).order_by('data_vencimento')
            contas_do_dia_nota = NotaCompleta.objects.filter(saida__data_emissao=today_date).filter(pago=False).order_by('saida__data_emissao')


            total_valor = contas_do_dia_boleto.aggregate(total_valor=Sum('valor'))['total_valor']
            total_valor_nota = contas_do_dia_nota.aggregate(total_valor=Sum('valor'))['total_valor']
    
            #VALIDAÇÃO 'total_valor'
            if not total_valor:
                total_valor = 0         
                
            if not total_valor_nota:
                total_valor_nota = 0
                
            
        
            context = {
                'contas_do_dia': contas_do_dia_boleto,
                'total_boletos': locale.currency(total_valor, grouping=True),
                'contas_do_dia_nota': contas_do_dia_nota,
                'total_valor_nota': locale.currency(total_valor_nota, grouping=True),
                'total_dia': locale.currency(total_valor+total_valor_nota, grouping=True),
                }
        
            return render(request, template_name , context)
        
        except ContaPagamento.DoesNotExist:
            raise Http404("ERRO: Conta não existe!")
    else:
      return HttpResponse(f'Metodo Errado!') 
    
#GET /contas-a-pagar/
@login_required(login_url='login/')
def contas_a_pagar(request): 
    template_name = 'financeiro/contas-a-pagar.html'
    
    cache.delete('filtro_notas_boletos_cache')  
    
    if request.method == 'GET':
        try:
            context = {
                'filter': ContasFilter()
                }
        
            return render(request, template_name , context)
        
        except ContaPagamento.DoesNotExist:
            raise Http404("ERRO: Conta não existe!")
        
#GET /contas-a-pagar/
@login_required(login_url='login/')
def contas_atrasadas(request, template_name = 'financeiro/resumo-atrasados.html'): 
    
    if request.method == 'GET': 
        today_date = datetime.now()  
        
        notas_em_atrazo = NotaCompleta.objects.filter(saida__data_emissao__range=[datetime.min, today_date - timedelta(days=1)]).filter(pago=False).order_by('saida__data_emissao')
        boletos_em_atrazo = ContaBoleto.objects.filter(data_vencimento__range=[datetime.min, today_date - timedelta(days=1)]).filter(pago=False).order_by('data_vencimento')

       
        total_valor_em_atraso_nota = notas_em_atrazo.aggregate(total_valor=Sum('valor'))['total_valor']
        total_valor_em_atraso = boletos_em_atrazo.aggregate(total_valor=Sum('valor'))['total_valor']


        if not total_valor_em_atraso:
            total_valor_em_atraso = 0
        
        if not total_valor_em_atraso_nota:
            total_valor_em_atraso_nota = 0
        
        context = {
                'boletos_em_atrazo': boletos_em_atrazo, 
                'total_valor_em_atraso': locale.currency(total_valor_em_atraso, grouping=True),
                'notas_em_atrazo': notas_em_atrazo, 
                'total_valor_em_atraso_nota': locale.currency(total_valor_em_atraso_nota, grouping=True),
                'total_atrazo': locale.currency(total_valor_em_atraso+total_valor_em_atraso_nota, grouping=True),
                }
        
        
        return render(request, template_name , context)       
  
#GET /contas-a-pagar/inserir     
@login_required(login_url='login/')
def inserir_nova_conta_a_pagar(request, template_name = 'financeiro/fragmentos/inserir-conta-a-pagar.html'):
    
    if request.method == 'GET':        
        return render(request, template_name , {})
        
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
def filtro_contas_a_pagar(request,  template_name = 'financeiro/fragmentos/resultados-contas-a-pagar.html'):
             
                  

        check_pago = request.GET.get('check_pago') 
        check_nao_pago = request.GET.get('check_nao_pago') 
        
        # descricao = request.GET.get('descricao') or ''
        # valor_busca = request.GET.get('valor').replace(".","").replace(",",".")
        # fornecedor = request.GET.get('fornecedor') or ''
        # initial_date_aux = request.GET.get('data') or '0001-01-01' # datetime.min is 1
        # end_date_aux = request.GET.get('data_f') or '9999-12-31' # datetime.max is 9999
       
        queryConta = Q()
        queryNota = Q()
        
        if request.GET.get('descricao') != "":
            descricao = request.GET.get('descricao')
            
            queryConta &= Q(conta__saida__nota_fiscal__icontains=descricao) 
            queryConta |= Q(doc__icontains=descricao) 
            
            queryNota &= Q(saida__nota_fiscal__icontains=descricao)
            
            print(f'PESQUISA ------------------------ descricao/cod ---> {descricao}')
        
        if request.GET.get('valor') != "":
            valor_busca = request.GET.get('valor')
            
            queryConta &= Q(valor__icontains=valor_busca.replace(".","").replace(",","."))
            
            queryNota &= Q(valor__icontains=valor_busca)
            
            print(f'PESQUISA ------------------------ Valor ---> {valor_busca}')
       
        if request.GET.get('fornecedor')  != "": 
            fornecedor = request.GET.get('fornecedor')  
                   
            queryConta &= Q(conta__saida__fornecedor__nome__icontains=fornecedor)
            
            queryNota &= Q(saida__fornecedor__nome__icontains=fornecedor)
            
            print(f'PESQUISA ------------------------ fornecedor ---> {fornecedor}')
        
        if request.GET.get('data') != "" and  request.GET.get('data_f') != "": 
            initial_date_aux = request.GET.get('data') 
            initial_date = datetime.strptime(initial_date_aux, '%Y-%m-%d')
            end_date_aux = request.GET.get('data_f')
            end_date = datetime.strptime(end_date_aux, '%Y-%m-%d')
            
            queryConta &= Q(data_vencimento__range=[initial_date, end_date])
            
            queryNota &= Q(saida__data_emissao__range=[initial_date, end_date])
            
            print(f'PESQUISA ------------------------ data inicial ---> {initial_date}')  
            print(f'PESQUISA ------------------------ data final ---> {end_date}')              
 
        
        
        objectsConta = ContaBoleto.objects.all().filter(queryConta).order_by('data_vencimento')                                                          
        objectsNota = NotaCompleta.objects.all().filter(queryNota).order_by('saida__data_emissao')  
        
               
        if check_pago == 'on' and check_nao_pago == None:
                print('------------------ PAGO: ON --------- NÃO PAGO: OFF')
            
                objectsConta = objectsConta.filter(pago=True)
                objectsNota = objectsNota.filter(pago=True)
        
        elif check_nao_pago == 'on' and check_pago == None:
                print('------------------ PAGO: OFF --------- NÃO PAGO: ON')
            
                objectsConta = objectsConta.filter(pago=False)
                objectsNota = objectsNota.filter(pago=False) 

                       
        total_valor_boletos = 0
        total_valor_desconto = 0  
        total_acresc = 0
                   
        if objectsConta:
            total_valor_boletos = objectsConta.aggregate(total_valor = Sum('valor'))['total_valor']
        
        total_valor_notas = 0    
        if objectsNota:
            total_valor_notas = objectsNota.aggregate(total_valor = Sum('valor'))['total_valor']
            total_valor_desconto = objectsNota.aggregate(total_valor = Sum('desconto'))['total_valor']
            # total_valor_acres = objectsNota.filter(pago=True).aggregate(total_valor = Sum('acrescimo'))['total_valor']
              
        print(f'-----------------------------RESULTADO BOLETO {objectsConta}')
        print(f'-----------------------------RESULTADO NOTA {objectsNota}')
         
        context = {
                'boletos': objectsConta,
                'contas': objectsNota,
                # 'total_acresc': locale.currency(total_valor_acres, grouping=True), # fazer a Logica depois
                'total_desconto': locale.currency(total_valor_desconto, grouping=True), # fazer a Logica depois
                'total_valor_boletos': total_valor_boletos,
                'total_valor_notas': total_valor_notas,
                'total_geral': locale.currency((total_valor_boletos or 0 )+(total_valor_notas or 0), grouping=True),
                }
         
        cache.set('filtro_notas_boletos_cache', context)      

             
     
        return render(request, template_name , context)


@login_required(login_url='login/')
@csrf_exempt
def gerar_pdf_resultado_contas_e_boletos(request, template_name="financeiro/impressoes/resultado_notas_e_boletos_pdf.html"):
    
    if request.method == 'GET':
        current_domain = get_current_site(request).domain
        context = {
            'context' : cache.get('filtro_notas_boletos_cache'),

            'current_domain' : current_domain,
        }
        filename = 'resultados_notas_boletos.pdf'

    
        return gerar_pdf_by_template(template_name, context, filename) 

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
            
    # print(f'------------------------------- {situacao}')
    context = {
            'nota_atual': nota_atual,
            'pagamento': pagamento,
            'situacao': situacao,
            'boletos': boletos
        }                       
    
    response = render(request, template_name , context)
    response['HX-Push-Url'] = reverse('ver-nota-completa',kwargs={'pk':nota_atual.pk})
    return response

@login_required(login_url='login/')
def editar_saida(request, pk, template_name = 'financeiro/fragmentos/inserir-conta-a-pagar.html'):
    
    if request.method == 'GET':
        nota = get_object_or_404(NotaCompleta, pk=pk)
        
       
        context = {
        'nota_atual' : nota,
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
    # global resumo_listagem_boletos
    # global pode_salvar_boleto
    
    cache.set('pode_salvar_boleto', False) # salvo por 3 horas
    
    template_name = 'financeiro/fragmentos/pagamentos/resumo-boletos-pagamento.html'
    nota_atual = NotaCompleta.objects.get(pk=pk)
    valor_total = 0
    
    #CRIANDO RESUMO ----------
    resumo_listagem_boletos = list()
    cache.set('resumo_listagem_boletos', resumo_listagem_boletos)
    
    #VALIDAÇÃO DO NUMERO DE PARCELAS
    try: 
        n_parcelas = request.POST.get('n_parcelas')
        n_parcelas = int(n_parcelas)
        if not n_parcelas >= 1 or n_parcelas == "":
            template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
            response = render(request, template_name=template_name, context={'errorMensagem': 'Número de Parcelas INVÁLIDO'})
            response['HX-Trigger'] = "buttonError"
            pode_salvar_boleto = False
            cache.set('pode_salvar_boleto', False)
            return response       
    except ValueError:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Número de Parcelas INVÁLIDO'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        cache.set('pode_salvar_boleto', False)
        return response    
    #VALIDÇÃO DO VALOR
    try: 
        valor_parcelas = float(request.POST.get('valor_parcelas').replace('.', '').replace(',', '.'))
        if valor_parcelas <= 0:
            template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
            response = render(request, template_name=template_name, context={'errorMensagem': 'Valor INVÁLIDO'})
            response['HX-Trigger'] = "buttonError"
            pode_salvar_boleto = False
            cache.set('pode_salvar_boleto', False)
            return response        
    except ValueError:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Valor INVÁLIDO'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        cache.set('pode_salvar_boleto', False)
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
            cache.set('pode_salvar_boleto', False)
            return response
        
    except ValueError:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Data INVÁLIDA'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        cache.set('pode_salvar_boleto', False)
        return response
    
    #NUMERO DO DOCUMENTO
    doc_parcelas = request.POST.get('doc_parcela')
        

    for n in range(int(n_parcelas)):
        parcela = {'parcela':n+1, 'valor':locale.currency(valor_parcelas, grouping=True).replace('R$ ',""), 'data_vencimento':data_1_parcela + timedelta(days=n*30)}
        
        if not doc_parcelas == "":
            parcela['doc']= f'{doc_parcelas}-{n+1}'
        else:
            parcela['doc']= ''
        
        resumo_listagem_boletos = list(cache.get('resumo_listagem_boletos'))
        resumo_listagem_boletos.append(parcela)
        cache.set('resumo_listagem_boletos', resumo_listagem_boletos)
        
        valor_total += valor_parcelas

    pode_salvar_boleto = True
    cache.set('pode_salvar_boleto', True)
    
    context = {
        'resumo': resumo_listagem_boletos,
        'num_parcelas': n_parcelas,
        'valor_total': locale.currency(valor_total, grouping=True),
        'nota_atual': nota_atual
    }   
    
    response = render(request, template_name , context)
    response['HX-Trigger'] = "buttonSave"
    
    print(f'STATUS (pós get Resumo) - PODE SALVAR BOLETOS? -------------> {cache.get("pode_salvar_boleto")}')
    
    return response


@login_required(login_url='login/')
@csrf_exempt
def atualizar_resumo_boleto_mensal(request, pk):
    # global resumo_listagem_boletos
    # global pode_salvar_boleto
    
    print(f'STATUS (pré atualizar) - PODE SALVAR BOLETOS? -------------> {cache.get("pode_salvar_boleto")}')
    
    qnt_parcelas = int(request.POST.get('num_parcelaA'))
    
    
    print(f'QUANTIDADE DE PARCELAS ----------------> {qnt_parcelas}')
    
    
    # #VALIDAÇÃO DO DOC
    doc_parcelas = request.POST.getlist('doc_parcelaA')
    if len(doc_parcelas) < qnt_parcelas:
        dif = int(qnt_parcelas) - len(doc_parcelas)
        for x in range(dif):
            doc_parcelas.append('-')
        
    print(f'DOC PARCELAS ---------------> {doc_parcelas}')
    # #VALIDAÇÃO DO VALOR
    try: 
        valor_parcelas = request.POST.getlist('valor_parcelaA')
        if len(valor_parcelas) < qnt_parcelas:
            template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
            response = render(request, template_name=template_name, context={'errorMensagem': 'Valor VAZIO'})
            response['HX-Trigger'] = "buttonError"
            pode_salvar_boleto = False
            cache.set('pode_salvar_boleto', False)
            return response 
        else:
            for valor in valor_parcelas:
                valor = float(valor.replace('.', '').replace(',', '.'))
    
                if valor <= 0:
                    template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
                    response = render(request, template_name=template_name, context={'errorMensagem': 'Valor INVÁLIDO'})
                    response['HX-Trigger'] = "buttonError"
                    pode_salvar_boleto = False
                    cache.set('pode_salvar_boleto', False)
                    return response        
    except ValueError:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Valor INVÁLIDO'})
        pode_salvar_boleto = False
        cache.set('pode_salvar_boleto', False)
        return response         
    
    print(f'VALOR PARCELAS ---------------> {valor_parcelas}')
    #VALIDÇÃO DA DATA
    try: 
        datas_parcelas = request.POST.getlist('data_parcelaA')
        if len(datas_parcelas) < qnt_parcelas:
            template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
            response = render(request, template_name=template_name, context={'errorMensagem': 'Data VAZIA'})
            response['HX-Trigger'] = "buttonError"
            pode_salvar_boleto = False
            cache.set('pode_salvar_boleto', False)
            return response 
        else:
            for data in datas_parcelas:
                if data == "":
                    template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
                    response = render(request, template_name=template_name, context={'errorMensagem': 'Data INVÁLIDA'})
                    response['HX-Trigger'] = "buttonError"
                    pode_salvar_boleto = False
                    cache.set('pode_salvar_boleto', False)
                    return response    
        
    except ValueError:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Data INVÁLIDA'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        cache.set('pode_salvar_boleto', False)
        return response
    
    print(f'DATAS PARCELAS ---------------> {datas_parcelas}')
    #GUARDANDO E ENVIADO OS DADOS NOVAMENTE
    template_name = 'financeiro/fragmentos/pagamentos/resumo-boletos-pagamento.html'
    resumo_listagem_boletos_atualizado = list()
    
    valor_total = 0
    nota_atual = NotaCompleta.objects.get(pk=pk)
  
    
    for n in range(int(qnt_parcelas)):
        valor = float(valor_parcelas[n].replace('.', '').replace(',', '.'))
        doc = doc_parcelas[n]
        if not doc or doc == "" :
            doc = '-'
        data = datetime.strptime(datas_parcelas[n], '%Y-%m-%d')
        parcela = {'parcela':n+1, 'doc': doc,'valor':locale.currency(valor, grouping=True).replace('R$ ',""), 'data_vencimento':data}
        
                
        resumo_listagem_boletos_atualizado.append(parcela)
        valor_total += valor
   
    cache.set('resumo_listagem_boletos', resumo_listagem_boletos_atualizado)
    
    pode_salvar_boleto = True
    cache.set('pode_salvar_boleto', True)
    
    context = {
        'resumo': resumo_listagem_boletos_atualizado,
        'num_parcelas': qnt_parcelas,
        'valor_total': locale.currency(valor_total, grouping=True),
        'nota_atual': nota_atual
    }   
    
    response = render(request, template_name , context)
    response['HX-Trigger'] = "buttonSave"
    
    print(f'STATUS (pós atualizar) - PODE SALVAR BOLETOS? -------------> {cache.get("pode_salvar_boleto")}')
    return response

  
@login_required(login_url='login/')
@csrf_exempt
def salvar_boletos_mensal(request, pk):
    # global pode_salvar_boleto
    # global resumo_listagem_boletos
    status_salvar = cache.get('pode_salvar_boleto')
    
    print(f'STATUS (pré salvar) - PODE SALVAR BOLETOS? -------------> {status_salvar}')
    
    if not status_salvar:
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': f'Erro ao Salvar! Tentar novamente.(Salvar Boleto:{pode_salvar_boleto}'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        cache.set('pode_salvar_boleto', False)
        return response
    
    #SALVANDO BOLETOS NO BANCO
    try:
        resumo_listagem_boletos = list(cache.get('resumo_listagem_boletos'))
        qnt_parcelas = int(request.POST.get('num_parcelaA'))
        nota_atual = NotaCompleta.objects.get(pk=pk)
        
        for n in range(qnt_parcelas):
            n_doc = resumo_listagem_boletos[n]['doc']
            if not n_doc or n_doc == '':
                n_doc = '-'
            ContaBoleto.objects.create(conta = nota_atual,
                                    parcela =  n+1,
                                    total_parcelas =  qnt_parcelas,
                                    doc = n_doc,
                                    valor = resumo_listagem_boletos[n]['valor'].replace(".","").replace(",","."),
                                    data_vencimento = resumo_listagem_boletos[n]['data_vencimento'],
                                    usuario = request.user,
                                    obs = "")
        
        nota_atual.pago = True
        nota_atual.forma_pagamento = 2 #por Boletos
        nota_atual.save()
        
        pode_salvar_boleto = False #resetar variavel
        cache.set('pode_salvar_boleto', False)
        return redirect(reverse('ver-nota-completa', kwargs={'pk':pk}))
    
    except (ValueError, ValidationErr):
        template_name = 'financeiro/fragmentos/pagamentos/error-mensagem.html'
        response = render(request, template_name=template_name, context={'errorMensagem': 'Erro ao Salvar! Tentar novamente.'})
        response['HX-Trigger'] = "buttonError"
        pode_salvar_boleto = False
        cache.set('pode_salvar_boleto', False)
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
        print(f"DELETADO - DETALHES DA NOTA")
        nota_atual = NotaCompleta.objects.get(pk=pk)

        try:
            itens = nota_atual.itens.all()
            for item in itens:
               n = item.pk
               ItensNota.delete(item)
               print(f'DELETADO ITEM -------------> {n}')
               
            n = nota_atual.saida.pk
            nota_atual.saida.delete()
            print(f'DELETADO DESCRIÇÃO DA NOTA -------------> {n}')
            n = nota_atual.pk
            nota_atual.delete()
            print(f'DELETADO NOTA -------------> {n}')
            return render(request, template_name = 'financeiro/resumo-do-dia.html', context={})
            
        except:
            print('erro ao Excluir')
            return HttpResponse(f'Erro ao Excluir ----> Nota Cód: {nota_atual.pk}')
    else:
      return HttpResponse(f'Metodo Errado!')      
    

@login_required(login_url='login/')
@csrf_exempt
def selecionar_forma_de_pagamento(request, pk, template_name = 'financeiro/fragmentos/pagamentos/modal-ver-formas-pagamentos.html'):
    
    if request.method == "GET":
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


@login_required(login_url='login/')
@csrf_exempt
def inserir_descricao_saida(request, template_name='financeiro/fragmentos/modal-inserir-descricao-nota.html'):
    
    if request.method == 'GET':
        fornecedores = Fornecedor.objects.all()     
        centros_custo = Obra.objects.all()
        
        context = {
            'fornecedores': fornecedores,
            'centros_custo': centros_custo
            }
        return render(request, template_name, context)
    
@login_required(login_url='login/')
@csrf_exempt
def editar_descricao_saida(request, pk, nota, template_name='financeiro/fragmentos/modal-inserir-descricao-nota.html'):
    
    if request.method == 'GET':
        fornecedores = Fornecedor.objects.all()     
        centros_custo = Obra.objects.all()
        descricao = DescricaoNota.objects.get(pk=pk)
        nota_atual = NotaCompleta.objects.get(pk=nota)
        
        context = {
            'fornecedores': fornecedores,
            'centros_custo': centros_custo,
            'descricao': descricao,
            'nota_atual': nota_atual,
            }
        return render(request, template_name, context)

    
@login_required(login_url='login/')
@csrf_exempt
def salvar_descricao_saida(request, template_name='financeiro/fragmentos/inserir-conta-a-pagar.html'):
    fornecedor = request.POST.get('fornecedor')
    print(fornecedor)
    #validação fornecedor
    if not fornecedor or fornecedor == "":
        response = HttpResponse(f"<span style='color:red'><i>Fornecedor Inválido</i></span>")
        response['HX-Retarget'] = '#error_fornecedor'
        response['HX-Swap'] = 'innerHTML'
        return response
    else:
        fornecedor = Fornecedor.objects.get(pk = int(fornecedor))
   
    data_emissao = request.POST.get('data_emissao')
    print(data_emissao)
    
    #validação data_emissao
    if not data_emissao or data_emissao == "":
        response = HttpResponse(f"<span style='color:red'><i>Data Inválida</i></span>")
        response['HX-Retarget'] = '#error_data_emissao'
        response['HX-Swap'] = 'innerHTML'
        return response
    else:
        data_emissao = datetime.strptime(data_emissao, '%Y-%m-%d')
    
    centro_de_custo = Obra.objects.get(pk = int(request.POST.get('centro-de-custo')))
    descricao = request.POST.get('descricao')
    nota_fiscal = request.POST.get('nota_fiscal')
    
    nova_descricao = DescricaoNota.objects.create(
        descricao = descricao,
        nota_fiscal = nota_fiscal,
        fornecedor = fornecedor,
        data_emissao = data_emissao,
        centro_de_custo = centro_de_custo
    )
    nota_atual = NotaCompleta.objects.create(
        usuario = request.user,
        saida = nova_descricao
    )
    
    context = {
        'descricao' : nova_descricao,
        'nota_atual' : nota_atual,
    }
    response = HttpResponseClientRedirect(reverse("editar-saida", kwargs={'pk':nota_atual.pk}))
    response['HX-Trigger'] = 'closeModalDescricao'
    # response['HX-Push-Url'] = reverse('editar-saida',kwargs={'pk':nota_atual.pk})
    return response


@login_required(login_url='login/')
@csrf_exempt    
def salvar_editar_descricao_saida(request, pk, nota, template_name='financeiro/fragmentos/descricao-nota-inserir.html'):
    
    fornecedor = request.POST.get('fornecedor')
    
    #validação fornecedor
    if not fornecedor or fornecedor == "":
        response = HttpResponse(f"<span style='color:red'><i>Fornecedor Inválido</i></span>")
        response['HX-Retarget'] = '#error_fornecedor'
        response['HX-Swap'] = 'innerHTML'
        return response
    else:
        fornecedor = Fornecedor.objects.get(pk = int(fornecedor))
        print(fornecedor)
   
    data_emissao = request.POST.get('data_emissao')
    print(data_emissao)
    
    #validação data_emissao
    if not data_emissao or data_emissao == "":
        response = HttpResponse(f"<span style='color:red'><i>Data Inválida</i></span>")
        response['HX-Retarget'] = '#error_data_emissao'
        response['HX-Swap'] = 'innerHTML'
        return response
    else:
        data_emissao = datetime.strptime(data_emissao, '%Y-%m-%d')
    
    centro_de_custo = Obra.objects.get(pk = int(request.POST.get('centro-de-custo')))
    descricao_ = request.POST.get('descricao')
    nota_fiscal = request.POST.get('nota_fiscal')
    
    descricao = DescricaoNota.objects.get(pk=pk)
    descricao.descricao = descricao_
    descricao.nota_fiscal = nota_fiscal
    descricao.data_emissao = data_emissao
    descricao.centro_de_custo = centro_de_custo
    descricao.fornecedor = fornecedor

    descricao.save()
    nota_atual =  NotaCompleta.objects.get(pk=nota)
    
    context = {
        'descricao' : descricao,
        'nota_atual' : nota_atual
    }
    response = HttpResponseClientRedirect(reverse("editar-saida", kwargs={'pk':nota_atual.pk}))
    response['HX-Trigger'] = 'closeModalDescricao'
    return response


@login_required(login_url='login/')
@csrf_exempt
def inserir_itens_saida(request, pk, template_name='financeiro/fragmentos/modal-inserir-itens.html'):
    
    if request.method == 'GET':

        nota_atual = NotaCompleta.objects.get(pk=pk)
        unid_medidas = UNIDADES
        
        context = {
            'nota_atual': nota_atual,
            'unid_medidas' : unid_medidas
            }
        return render(request, template_name, context)
    
@login_required(login_url='login/')
@csrf_exempt
def salvar_itens_saida(request, pk, template_name='financeiro/fragmentos/itens-nota-inserir.html'):
    
    if request.method == 'POST':
        nota_atual = NotaCompleta.objects.get(pk=pk)
        
        descricao = request.POST.get('descricao')
        qtd = request.POST.get('qtd')
        unid_medida = request.POST.get('unidade')
        valor = request.POST.get('valor').replace(".","").replace(",",".")
        
        #VALIDANDO QUANTIDADE
        if not qtd or float(qtd) <=0:
            response = HttpResponse(f"<span style='color:red'><i>Qtd Inválida</i></span>")
            response['HX-Retarget'] = '#error_qtd'
            response['HX-Swap'] = 'innerHTML'
            return response
        else:
            qtd = float(qtd)
            
        #VALIDANDO QUANTIDADE
        if not valor or float(valor) <=0:
            response = HttpResponse(f"<span style='color:red'><i>Valor Inválido</i></span>")
            response['HX-Retarget'] = '#error_valor'
            response['HX-Swap'] = 'innerHTML'
            return response
        else:
            valor = float(valor)
            
        
        novo_item = ItensNota.objects.create(
            descricao = descricao,
            unid_medida = unid_medida,
            qtd = qtd,
            valor = valor
            
        ) 
        nota_atual.itens.add(novo_item)
        nota_atual.valor = nota_atual.get_valor_total_itens()
        nota_atual.save()
              
        print(F'------------------ ITEM {novo_item.pk} SALVO COM SUCESSO NA NOTA {nota_atual.pk}')
        
                 
        context = {
            'nota_atual': nota_atual,
            }
        
        
        response = render(request, template_name, context)
        response['HX-Trigger'] = 'closeModalItens'
        return response
    else:
        HttpResponse(f"Erro ao Salvar")     


@login_required(login_url='login/')
@csrf_exempt
def excluir_iten_saida(request, pk, nota, template_name='financeiro/fragmentos/itens-nota-inserir.html'):
    
    item = ItensNota.objects.get(pk=pk)
    item.delete()
    nota_atual = NotaCompleta.objects.get(pk = nota)
    nota_atual.valor = nota_atual.get_valor_total_itens() 
    nota_atual.save()
    
    context = {
        'nota_atual': nota_atual
    }
    
    response = render(request, template_name, context)
    response['HX-Trigger'] = 'itemNotaExcluido'
    return response
   

@login_required(login_url='login/')
@csrf_exempt
def inserir_desconto_conta_a_pagar(request, pk,):
    
    if request.method == 'GET':
        desconto_atual = request.GET.get('desconto', 0)
        nota_atual = NotaCompleta.objects.get(pk = pk)
        nota_atual.desconto = Decimal(desconto_atual.replace(".","").replace(",","."))
        
        nota_atual.valor = nota_atual.get_valor_total_itens() - nota_atual.desconto
        
        nota_atual.save()
    
        print(f'--------------Inserido Desconto de R$ {desconto_atual}')

        return redirect("ver-nota-completa", pk=pk)


##RELATÓRIOS FINANCEIRO

@login_required(login_url='login/')
@csrf_exempt
def relatorios_inicio(request, template_name='financeiro/relatorios/relatorios-inicio.html'):
    
    if request.method == 'GET':

        context = {
 
        }
        return render(request, template_name, context)
    
    
@login_required(login_url='login/')
@csrf_exempt
def get_relatorio_selecionado(request):
    
    if request.method == 'GET':

        relatorio_escolhido = request.GET.get('select-relatorios')
    

        if relatorio_escolhido == '1':
            template_name = 'financeiro/relatorios/fragmentos/busca-item-avancado.html'
            print(F'------------------ RELATÓRIO POR ITEM AVANÇADO')
            
        elif relatorio_escolhido == '2':
            template_name = 'financeiro/relatorios/fragmentos/relatorio-fornecedor.html'
            print(F'------------------ RELATÓRIO FORNECEDOR')
            
        elif relatorio_escolhido == '3':
            template_name = 'financeiro/relatorios/fragmentos/relatorio-periodo-especifico.html'
            print(F'------------------ RELATÓRIO POR PERÍODO')
                  
        else:
            template_name = 'financeiro/relatorios/fragmentos/busca-item-avancado.html'
            print(F'------------------ OUTRO RELATÓRIO')
           
            
        context = {
      
        } 
            
        return render(request, template_name, context)
    
@login_required(login_url='login/')
@csrf_exempt
def get_itens_por_descricao(request, template_name='financeiro/relatorios/fragmentos/resultados-relatorio-itens.html'):
    
    if request.method == 'GET':
        
        query = request.GET.get('descricao')
        itens = ItensNota.objects.filter(descricao__icontains=query).only('descricao')

        context = {
            'itens' : itens
        }
        return render(request, template_name, context)