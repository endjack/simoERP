from datetime import datetime
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic.base import TemplateView
from funcionarios.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from funcionarios.models import *
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt

@login_required(login_url='login/')
@csrf_exempt
def procurar_pessoal(request, template_name="funcionarios/fragmentos/procurar/procurar_home.html"):
    if request.method == 'GET':
        menu_ativo = 'PROCURAR'
        lotacoes = Obra.objects.all()
        cargos = Cargo.objects.all()
        situacoes = FuncionarioV2.Situacao
        funcionarios = FuncionarioV2.objects.all().filter(situacao='ADMITIDO').order_by('nome')
        
        
        context = {
            'menu_ativo' : menu_ativo,
            'lotacoes' : lotacoes,
            'cargos' : cargos,
            'situacoes' : situacoes,
            'funcionarios' : funcionarios,
     
        }
        return render(request, template_name, context)

@login_required(login_url='login/')
@csrf_exempt   
def filtrar_funcionariosV2(request):
    
    if request.GET.get('filter') == 'local':
        template_name="funcionarios/fragmentos/local/resultados_procurar_local.html"
    else:
        template_name="funcionarios/fragmentos/procurar/resultados_procurar_funcionarios.html"
    
    if request.method == 'GET':


        lotacao = request.GET.get('lotacao')
        situacao = request.GET.get('situacao')
        
        queryFuncionario = Q()
        
        if request.GET.get('nome') not in ["", None]:
            nome = request.GET.get('nome')
            
            queryFuncionario &= Q(nome__icontains=nome) 

            print(f'PESQUISA ------------------------ Nome ---> {nome}') 
       
        if request.GET.get('cargo') not in ["", "-1", None]:
            cargo = Cargo.objects.get(pk=int(request.GET.get('cargo')))
            
            queryFuncionario &= Q(cargo=cargo) 

            print(f'PESQUISA ------------------------ Cargo ---> {cargo.cargo}')
       
        if request.GET.get('lotacao') not in ["", "-1", None]:
            lotacao = Obra.objects.get(pk=int(request.GET.get('lotacao')))
            
            queryFuncionario &= Q(lotacao=lotacao) 

            print(f'PESQUISA ------------------------ Lotação ---> {lotacao.nome}')
       
        if request.GET.get('situacao') not in ["", "-1", None]:
            
            queryFuncionario &= Q(situacao=situacao) 

            print(f'PESQUISA ------------------------ Lotação ---> {situacao}')
       
        funcionarios = FuncionarioV2.objects.all().filter(queryFuncionario).order_by('nome')
        
        context = {

            'funcionarios' : funcionarios,
     
        }
        return render(request, template_name, context)

@login_required(login_url='login/')
@csrf_exempt
def cadastrar_funcionarios_pessoal(request, pk=None, template_name= 'funcionarios/fragmentos/funcionarios/funcionarios_home.html'):
    if request.method == 'GET':
        #CADASTRAR NOVO
        menu_ativo = 'CADASTRARFUNCIONARIOS'
        tipo_contrato = FuncionarioV2.Contratos
        tipo_demissao = FuncionarioV2.TipoDemissao
        estado_civil = FuncionarioV2.EstadoCivil
        tipo_conta = FuncionarioV2.TipoConta
        tipo_pix = FuncionarioV2.TipoPix
        situacao = FuncionarioV2.Situacao
        cargos = Cargo.objects.all()
        obras = Obra.objects.all()
        bancos = Banco.objects.all()
        responsavel_direto = ResponsávelObraFuncionariov2.objects.all()
        start_inputs_dependents = 1
        
        #EDITAR FUNCIONÁRIO,
        funcionario_atual = None
        dependentes = None
        if pk:
          funcionario_atual = FuncionarioV2.objects.get(pk=pk)
          dependentes = DependenteFuncionariov2.objects.filter(funcionario=funcionario_atual)
        
        context = {
            'menu_ativo' : menu_ativo,
            'tipo_contrato' : tipo_contrato,
            'tipo_demissao' : tipo_demissao,
            'tipo_conta' : tipo_conta,
            'tipo_pix' : tipo_pix,
            'situacao' : situacao,
            'cargos' : cargos,
            'estado_civil' : estado_civil,
            'obras' : obras,
            'bancos' : bancos,
            'responsavel_direto' : responsavel_direto,
            'start_inputs_dependents' : start_inputs_dependents,
            'funcionario_atual' : funcionario_atual,
            'dependentes' : dependentes,
        }
        return render(request, template_name, context)
   
#EXCLUIR FUNCIONÁRIO NA PAGINA DE EDITAR
@login_required(login_url='login/')
@csrf_exempt   
def excluir_funcionarios_pessoal(request, pk):
    
    FuncionarioV2.objects.get(pk=pk).delete()
    print(f'-------------EXCLUIDO FUNCIONÁRIO')
    
    return redirect(reverse('procurar_pessoal'))  
    
#EXCLUIR DEPENDENTE DE FUNCIONÁRIO NA PAGINA DE EDITAR
@login_required(login_url='login/')
@csrf_exempt  
def excluir_dependente(request, pkDep, pk):

    DependenteFuncionariov2.objects.get(pk=pkDep).delete()
    print(f'-------------EXCLUIDO DEPENDENDE')
        
    return HttpResponse("Dependente Excluído <button onClick='window.location.reload();'><i class='fas fa-sync-alt'></i></button>")
 
    
    
@login_required(login_url='login/')
@csrf_exempt
def add_funcionario_v2(request, pk=None):
    
    menu_ativo = 'CADASTRARFUNCIONARIOS'
    if pk:
        funcionario_atual = FuncionarioV2.objects.get(pk=pk)
    else:
        funcionario_atual = None
    
    
    if request.htmx:
        #validar Nome vazio
        if request.POST.get('nome') == "":
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Campo 'Nome' Vazio"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        
        #validar Nome Pequeno
        elif len(request.POST.get('nome')) <= 3:
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Campo 'Nome' muito curto"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            nome = request.POST.get('nome')
            
        
         #validar CPF
        if request.POST.get('cpf') == "":
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Campo 'CPF' Vazio"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        
        # validar CPF incompleto
        elif len(request.POST.get('cpf')) != 14:
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Campo 'CPF' inválido"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            cpf = request.POST.get('cpf')
            
            
        #validar Data de Nascimento
        if request.POST.get('data_nascimento') == "":
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Campo 'Data de Nascimento' Vazio"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            data_nascimento = datetime.strptime(request.POST.get('data_nascimento'), '%Y-%m-%d')
            
        #validar Endereço
        if request.POST.get('endereco') == "":
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Campo 'Endereço' Vazio"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            endereco = request.POST.get('endereco')
               
         
        #validar estado_civil
        if request.POST.get('estado_civil') in ['','-1', None]:
             context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Selecione um 'Estado Civil'"
            }
            
             response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
             response['HX-Retarget'] = '#error-container'
             return response
        else:
            estado_civil = request.POST.get('estado_civil')
         
         
        #validar Matricula
        if request.POST.get('matricula') == "":
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Campo 'Matrícula' Vazio"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            matricula = request.POST.get('matricula')  
            
            
        #validar Tipo de Contrato
        if request.POST.get('tipo_contrato') in ['','-1', None] :
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Selecione Tipo de Contrato"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            tipo_contrato = request.POST.get('tipo_contrato')   
            
            if tipo_contrato == 'DETERMINADO':
                 #validar data_inicio_prorrogacao
                if request.POST.get('data_inicio_prorrogacao') in ['','-1', None] :
                    context = {
                    'menu_ativo' : menu_ativo,
                    'text_error': "Campo 'Início Prorrogação' Vazio"
                    }
                    
                    response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                    response['HX-Retarget'] = '#error-container'
                    return response
                else:
                    data_inicio_prorrogacao = datetime.strptime(request.POST.get('data_inicio_prorrogacao'), '%Y-%m-%d')
                 #validar data_fim_prorrogacao
                if request.POST.get('data_fim_prorrogacao') in ['','-1', None] :
                    context = {
                    'menu_ativo' : menu_ativo,
                    'text_error': "Campo 'Fim Prorrogação' Vazio"
                    }
                    
                    response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                    response['HX-Retarget'] = '#error-container'
                    return response
                else:
                    data_fim_prorrogacao = datetime.strptime(request.POST.get('data_fim_prorrogacao'), '%Y-%m-%d')
            else:
                data_inicio_prorrogacao = None
                data_fim_prorrogacao = None

        #validar Data de Admissão
        if request.POST.get('data_admissao') == "":
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Campo 'Data de Admissão' Vazio"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            data_admissao = datetime.strptime(request.POST.get('data_admissao'), '%Y-%m-%d')
            
            
        #validar Cargo
        if request.POST.get('cargo') in ['','-1', None] :
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Selecione Cargo"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            cargo = Cargo.objects.get(pk = int(request.POST.get('cargo'))) 
            
        #validar Salário
        if request.POST.get('salario') in ['','0', None] :
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Campo 'Salário' Vazio ou Inválido"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            salario = float(request.POST.get('salario').replace('.','').replace(',','.'))
            
            
            
        #validar Lotação
        if request.POST.get('lotacao') in ['','-1', None] :
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Selecione Lotação/Centro de Custo"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            lotacao = Obra.objects.get(pk = int(request.POST.get('lotacao')))
            
        #validar Situacao
        data_demissao = None
        tipo_demissao = '-' #DEFAULT
        data_inicio_afastamento = None
        data_fim_afastamento = None
        if request.POST.get('situacao') in ['','-1', None] :
            context = {
            'menu_ativo' : menu_ativo,
            'text_error': "Selecione Situação"
             }
            
            response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
            response['HX-Retarget'] = '#error-container'
            return response
        else:
            situacao = request.POST.get('situacao')
            if situacao == 'DEMITIDO' :
                 #validar data_demissao
                if request.POST.get('data_demissao') in ['','-1', None] :
                    context = {
                    'menu_ativo' : menu_ativo,
                    'text_error': "Campo 'Data de Rescisão' Vazio"
                    }
                    
                    response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                    response['HX-Retarget'] = '#error-container'
                    return response
                else:
                    data_demissao = datetime.strptime(request.POST.get('data_demissao'), '%Y-%m-%d')
                 #validar tipo_demissao
                if request.POST.get('tipo_demissao') in ['','-1', None] :
                    context = {
                    'menu_ativo' : menu_ativo,
                    'text_error': "Selecione Tipo de Rescisão"
                    }
                    
                    response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                    response['HX-Retarget'] = '#error-container'
                    return response
                else:
                    tipo_demissao = request.POST.get('tipo_demissao')
                   
            elif situacao == 'AFASTADO INSS - POR DOENÇA' or situacao == 'AFASTADO INSS - POR ACIDENTE':
                 #validar data_inicio_afastamento
                if request.POST.get('data_inicio_afastamento') in ['','-1', None] :
                    context = {
                    'menu_ativo' : menu_ativo,
                    'text_error': "Campo 'Início Afastamento' Vazio"
                    }
                    
                    response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                    response['HX-Retarget'] = '#error-container'
                    return response
                else:
                    data_inicio_afastamento = datetime.strptime(request.POST.get('data_inicio_afastamento'), '%Y-%m-%d')
                 #validar data_fim_afastamento
                if request.POST.get('data_fim_afastamento') in ['','-1', None] :
                    context = {
                    'menu_ativo' : menu_ativo,
                    'text_error': "Campo 'Fim Afastamento' Vazio"
                    }
                    
                    response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                    response['HX-Retarget'] = '#error-container'
                    return response
                else:
                    data_fim_afastamento = datetime.strptime(request.POST.get('data_fim_afastamento'), '%Y-%m-%d')

        
        #validar Responsavel direto
        if request.POST.get('responsavel_direto') in ['','-1', None]:
            responsavel_direto = None
        else:
            responsavel_direto = ResponsávelObraFuncionariov2.objects.get(pk = int(request.POST.get('responsavel_direto')))  
            
        #validar Banco
        if request.POST.get('banco') in ['','-1', None]:
            banco = None
        else:
            banco = Banco.objects.get(pk = int(request.POST.get('banco')))
             
            
        #validar tipo_responsavel
        if request.POST.get('tipo_responsavel') == 'on':
            tipo_responsavel = True 
            
            
        else:
            tipo_responsavel = False
            
        #validar analfabeto
        if request.POST.get('analfabeto') == 'on':
            analfabeto = True 
        else:
            analfabeto = False
            
        #validar adicional
        if request.POST.get('adicional') == '':
            adicional = 0
        else:
            adicional = float(request.POST.get('adicional').replace('.','').replace(',','.'))  

        print(f"-------------------------- Adicional = {adicional}")
        
        
        #validar foto
        if funcionario_atual is not None:
            if funcionario_atual.foto is None and request.FILES.get('imagem') not in ['', None]:
                foto = request.FILES.get('imagem')
            elif funcionario_atual.foto is not None and request.FILES.get('imagem') not in ['', None]:
                foto = request.FILES.get('imagem')        
            elif funcionario_atual.foto is None and request.FILES.get('imagem') in ['', None]:
                foto = None
            else:
                foto = funcionario_atual.foto
        else:
                foto = request.FILES.get('imagem')   
        
        #validar tipo de Conta
        tipo_conta = request.POST.get('tipo_conta')
        if tipo_conta in [-1, '-1', None]:
            tipo_conta = ''
            
            
        #validar tipo PIX
        tipo_pix = request.POST.get('tipo_pix')
        if tipo_pix in [ -1, '-1', None]:
            tipo_pix = ''
               
        rg = request.POST.get('rg', '')
        nome_mae = request.POST.get('nome_mae', '')
        nome_pai = request.POST.get('nome_pai', '')
        ctps = request.POST.get('ctps', '')
        cnh = request.POST.get('cnh', '')
        categoria_cnh = request.POST.get('categoria_cnh', '')
        cep_endereco = request.POST.get('cep_endereco', '')
        telefone1 = request.POST.get('telefone1', '')
        telefone2 = request.POST.get('telefone2', '')
              
        agencia = request.POST.get('agencia')
        
        conta = request.POST.get('conta')
        operacao = request.POST.get('operacao')
        pix = request.POST.get('pix')
        
        
        esocial = request.POST.get('esocial')
   
        obs = request.POST.get('obs')
        
        
        form_values = {
            'foto' : foto,
            'nome' : nome,
            'cpf' : cpf,
            'rg' : rg,
            'nome_mae' : nome_mae,
            'nome_pai' : nome_pai,
            'estado_civil' : estado_civil,
            'ctps' : ctps,
            'cnh' : cnh,
            'categoria_cnh' : categoria_cnh,
            'data_nascimento' : data_nascimento,
            'endereco' : endereco,
            'cep_endereco' : cep_endereco,
            'telefone1' : telefone1,
            'telefone2' : telefone2,
            'matricula' : matricula,
            'tipo_contrato' : tipo_contrato,
            'data_admissao' : data_admissao,
            'data_inicio_prorrogacao' : data_inicio_prorrogacao,
            'data_fim_prorrogacao' : data_fim_prorrogacao,
            'cargo' : cargo,
            'salario' : salario,
            'adicional' : adicional,
            'lotacao' : lotacao,
            'tipo_responsavel' : tipo_responsavel,
            'situacao' : situacao,
            'data_inicio_afastamento' : data_inicio_afastamento ,
            'data_fim_afastamento' : data_fim_afastamento,
            'data_demissao' : data_demissao,
            'tipo_demissao' : tipo_demissao,            
            'banco' : banco, 
            'agencia' : agencia,
            'tipo_conta' : tipo_conta,
            'conta' : conta,
            'op' : operacao,
            'pix' : pix,
            'tipo_pix' : tipo_pix,
            'esocial' : esocial,
            'analfabeto' : analfabeto,
            'responsavel_direto' : responsavel_direto,
            'obs' : obs,          
        }
        
        

        #CRIAR OU EDITAR NOVO FUNCIONÁRIO
        funcionario_atual, created = FuncionarioV2.objects.update_or_create(pk=pk,
                                                                            defaults= {**form_values})
        #SE 'created' FOR TRUE: CRIA UM NOVO FUNCIONÁRIO   
        if created:   
        #    funcionario_atual = FuncionarioV2.objects.create(**form_values)
           print(f"----- CRIADO FUNCIONÁRIO COM SUCESSO ---- Nome: {nome}")   
        else:
           print(f"----- EDITADO FUNCIONÁRIO COM SUCESSO ---- Nome: {nome}")  
        
        
    
    
    #validar Dependentes e CPF
    
    nomes_dependentes = request.POST.getlist('nome_dependente') 
    cpfs_dependentes = request.POST.getlist('cpf_dependente')
    
    
    for (nome_dependente, cpf_dependente) in zip(nomes_dependentes,cpfs_dependentes):
        nome_v = False
        cpf_v = False

        if nome_dependente != "":
            if len(nome_dependente) <= 3:
                context = {
                'menu_ativo' : menu_ativo,
                'text_error': "Campo 'Nome do Dependente' muito curto"
                }
                nome_v = False
                response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                response['HX-Retarget'] = '#error-container'
                return response
            elif cpf_dependente == "" or len(cpf_dependente) != 14:
                context = {
                'menu_ativo' : menu_ativo,
                'text_error': "Campo 'CPF do Dependente' Vazio ou Inválido"
                }
                nome_v = False
                response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                response['HX-Retarget'] = '#error-container'
                return response
            else:
                nome_v = True
                pass
        
        if cpf_dependente != "":
            if nome_dependente == "" or len(nome_dependente) <= 3:
                context = {
                'menu_ativo' : menu_ativo,
                'text_error': "Campo 'Nome do Dependente' Vazio ou muito curto"
                }
                cpf_v = False
                response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                response['HX-Retarget'] = '#error-container'
                return response
            elif cpf_dependente == "" or len(cpf_dependente) != 14:
                context = {
                'menu_ativo' : menu_ativo,
                'text_error': "Campo 'CPF do Dependente' Vazio ou Inválido"
                }
                cpf_v = False
                response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                response['HX-Retarget'] = '#error-container'
                return response  
            else:
                cpf_v = True
                pass 
               
        # Criar DEPENDENTES no for
        if cpf_v == True and nome_v == True:
            dep, created = DependenteFuncionariov2.objects.update_or_create(funcionario = funcionario_atual, 
                                                nome = nome_dependente, 
                                                cpf = cpf_dependente)      
            print(f"----- CRIADO (EDIT:{created}) DEPENDENTE COM SUCESSO ---- Nome: {dep.nome}")  
        
    #Criar TIPO Responsável
    if tipo_responsavel:
        resp, created = ResponsávelObraFuncionariov2.objects.update_or_create(responsavel = funcionario_atual)
        print(f"----- CRIADO (EDIT:{created}) RESPONSÁVEL COM SUCESSO ---- Nome: {resp.responsavel.nome}") 
        
        
    return redirect(reverse('procurar_pessoal'))  

@login_required(login_url='login/')
@csrf_exempt         
def detalhar_funcionario_v2(request, pk, template_name= 'funcionarios/fragmentos/funcionarios/detalhar_funcionario.html'):
    if request.method == 'GET':
        menu_ativo = 'PROCURAR'
        funcionario_atual = FuncionarioV2.objects.get(pk = pk)
        dependentes = DependenteFuncionariov2.objects.filter(funcionario = funcionario_atual)
    
        context = {
            'menu_ativo' : menu_ativo,
            'funcionario_atual' : funcionario_atual,
            'dependentes' : dependentes,
        }
        return render(request, template_name, context)



@login_required(login_url='login/')
@csrf_exempt    
def local_trabalho_pessoal(request, template_name= 'funcionarios/fragmentos/local/local_de_trabalho_home.html'):
    if request.method == 'GET':
        menu_ativo = 'LOCALDETRABALHO'
        funcionarios = FuncionarioV2.objects.all()
        localidades_distintas = LocalDeTrabalhoFuncionario.objects.values_list('local__local').distinct()
        localidades = Local.objects.all()
        
        funcionarios_livres = FuncionarioV2.get_funcionarios_livres()

        context = {
            'menu_ativo' : menu_ativo,
            'localidades' : localidades,
            'funcionarios' : funcionarios,
            'localidades_distintas' : localidades_distintas,
            'funcionarios_livres' : funcionarios_livres,
        }
        return render(request, template_name, context)
    
@login_required(login_url='login/')
@csrf_exempt    
def associar_funcionario_local(request, template_name= 'funcionarios/fragmentos/local/local_de_trabalho_home.html'):
    
    if request.method == 'POST':
        menu_ativo = 'LOCALDETRABALHO'
        
        funcionario_aux = request.POST['funcionario'] 
        local_aux = request.POST['local'] 
        print(f"{funcionario_aux} - {local_aux}")
        funcionario_atual = None
        local_atual = None
        
        
        if funcionario_aux not in ['', '-1', None]:
            funcionario_atual = FuncionarioV2.objects.get(pk=int(funcionario_aux))
            
            
                
            #CHECK-BOX SEM LOCAL DEFINIDO
            sem_local_definido_checkbox = request.POST.get('sem_local_definido_checkbox', False)
            
            if sem_local_definido_checkbox is False and local_aux not in ['', '-1', None]:
                local_atual = Local.objects.get(pk=int(local_aux))    
                #ASSOCIAR
                if LocalDeTrabalhoFuncionario.objects.filter(funcionario=funcionario_atual).exists():
                    update_func = LocalDeTrabalhoFuncionario.objects.get(funcionario= funcionario_atual)
                    update_func.local = local_atual
                    update_func.save()
                
                else:
                    LocalDeTrabalhoFuncionario.objects.create(funcionario= funcionario_atual, local = local_atual)
                
            
            elif sem_local_definido_checkbox is not False:
                    update_func = LocalDeTrabalhoFuncionario.objects.get(funcionario= funcionario_atual)
                    update_func.delete()
            else:
                return HttpResponse("Erro: Local não Encontrado!")
                
        else:
            return HttpResponse("Erro: Funcionário não Encontrado!")
        
        context = {
            'menu_ativo' : menu_ativo
        }
        return redirect(reverse('local_trabalho_pessoal'))  

       
@login_required(login_url='login/')
@csrf_exempt    
def imprimir_locais_funcionarios(request, template_name= 'funcionarios/fragmentos/local/impressao_local_de_trabalho_home.html'):
    if request.method == 'GET':
        menu_ativo = 'LOCALDETRABALHO'
        funcionarios = FuncionarioV2.objects.all()
        localidades_distintas = LocalDeTrabalhoFuncionario.objects.values_list('local__local').distinct()
        localidades = Local.objects.all()
        
        funcionarios_livres = FuncionarioV2.get_funcionarios_livres()

        context = {
            'menu_ativo' : menu_ativo,
            'localidades' : localidades,
            'funcionarios' : funcionarios,
            'localidades_distintas' : localidades_distintas,
            'funcionarios_livres' : funcionarios_livres,
        }
        return render(request, template_name, context)
    
    
@login_required(login_url='login/')
@csrf_exempt    
def cadastrar_cargo_pessoal(request, template_name= 'funcionarios/fragmentos/cargos/cargos_home.html'):
    if request.method == 'GET':
        menu_ativo = 'CADASTRARCARGOS'
    
        context = {
            'menu_ativo' : menu_ativo
        }
        return render(request, template_name, context)

@login_required(login_url='login/')
@csrf_exempt
def impressoes_pessoal(request, template_name= 'funcionarios/fragmentos/impressoes/impressoes_home.html'):
    if request.method == 'GET':
        menu_ativo = 'IMPRESSÃO'
   
        context = {
            'menu_ativo' : menu_ativo
        }
        return render(request, template_name, context)

@login_required(login_url='login/')
@csrf_exempt
def relatorios_pessoal(request, template_name= 'funcionarios/fragmentos/relatorios/relatorios_home.html'):
    if request.method == 'GET':
        menu_ativo = 'RELATÓRIO'
    
        context = {
            'menu_ativo' : menu_ativo
        }
        return render(request, template_name, context)

      
def add_inputs_dependente(request, id, template_name= 'funcionarios/fragmentos/funcionarios/novo_dependente.html'):
    if request.method == 'GET':
        context = {
            'start_inputs_dependents' : id+1,
            'anterior_inputs' : id
        }
        return render(request, template_name, context)
    
def clear_element(request):
        return HttpResponse('')







































#---------------------------------------------------------ANTIGO-----------------------------------------------#

# FUNCIONÁRIOS.
class InserirFuncionarioView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    
    template_name = 'funcionarios/inserir-funcionario.html'
    model = Funcionario
    form_class = InserirFuncionarioForm
    success_url = reverse_lazy('inserir-funcionario')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["funcionarios_list"] = Funcionario.objects.all()
        context["editar"] = False
        return context

class EditarFuncionarioView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')

    template_name = 'funcionarios/inserir-funcionario.html'
    model = Funcionario
    form_class = InserirFuncionarioForm
    success_url = reverse_lazy('inserir-funcionario')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editar"] = True
        return context

class ExcluirFuncionarioView(DeleteView): 
    login_url = reverse_lazy('login')

    model = Funcionario
    success_url = reverse_lazy('inserir-funcionario')


class DetalharFuncionarioView(TemplateView):
    pass


#CARGOS
class InserirCargoView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    
    template_name = 'funcionarios/inserir-cargo.html'
    model = Cargo
    form_class = InserirCargoForm
    success_url = reverse_lazy('inserir-cargo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cargos_list"] = Cargo.objects.all()
        context["editar"] = False
        return context

class EditarCargoView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')

    template_name = 'funcionarios/inserir-cargo.html'
    model = Cargo
    form_class = InserirCargoForm
    success_url = reverse_lazy('inserir-cargo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editar"] = True
        return context

class ExcluirCargoView(DeleteView): 
    login_url = reverse_lazy('login')

    model = Cargo
    success_url = reverse_lazy('inserir-cargo')


class DetalharCargoView(TemplateView):
    pass




def autocompletefuncionario(request):
    query = request.GET.get('term')
    query_set = Funcionario.objects.filter(nome__icontains=query)
    myList=[]
    myList += [x.nome+' - COD: '+x.matricula for x in query_set]
    return JsonResponse(myList,safe=False)