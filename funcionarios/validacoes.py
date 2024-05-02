from django.shortcuts import render


def validar_formulario_add_funcionario(request):
       
    #validar Nome vazio
    if request.POST.get('nome') == "":
        context = {
        'text_error': "Campo 'Nome' Vazio"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response

    #validar Nome Pequeno
    elif len(request.POST.get('nome')) <= 3:
        context = {

        'text_error': "Campo 'Nome' muito curto"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response
    else:
        print('Nome:', request.POST.get('nome'))

        

        #validar CPF
    if request.POST.get('cpf') == "":
        context = {
        'text_error': "Campo 'CPF' Vazio"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response

    # validar CPF incompleto
    elif len(request.POST.get('cpf')) != 14:
        context = {
        'text_error': "Campo 'CPF' inválido"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response       
        
    #validar Data de Nascimento
    if request.POST.get('data_nascimento') == "":
        context = {
        'text_error': "Campo 'Data de Nascimento' Vazio"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response
        
    #validar Endereço
    if request.POST.get('endereco') == "":
        context = {
        'text_error': "Campo 'Endereço' Vazio"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response
        
        
    #validar Matricula
    if request.POST.get('matricula') == "":
        context = {
        'text_error': "Campo 'Matrícula' Vazio"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response
        
        
    #validar Tipo de Contrato
    if request.POST.get('tipo_contrato') in ['','-1', None] :
        context = {
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
                'text_error': "Campo 'Início Prorrogação' Vazio"
                }
                
                response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                response['HX-Retarget'] = '#error-container'
                return response
                #validar data_fim_prorrogacao
            if request.POST.get('data_fim_prorrogacao') in ['','-1', None] :
                context = {
                'text_error': "Campo 'Fim Prorrogação' Vazio"
                }
                
                response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                response['HX-Retarget'] = '#error-container'
                return response


    #validar Data de Admissão
    if request.POST.get('data_admissao') == "":
        context = {
        'text_error': "Campo 'Data de Admissão' Vazio"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response
        
        
    #validar Cargo
    if request.POST.get('cargo') in ['','-1', None] :
        context = {
        'text_error': "Selecione Cargo"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response

        
    #validar Salário
    if request.POST.get('salario') in ['','0', None] :
        context = {
        'text_error': "Campo 'Salário' Vazio ou Inválido"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response

                
    #validar Lotação
    if request.POST.get('lotacao') in ['','-1', None] :
        context = {
        'text_error': "Selecione Lotação/Centro de Custo"
            }
        
        response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
        response['HX-Retarget'] = '#error-container'
        return response
        
    #validar Situacao
    if request.POST.get('situacao') in ['','-1', None] :
        context = {
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
                'text_error': "Campo 'Data de Rescisão' Vazio"
                }
                
                response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                response['HX-Retarget'] = '#error-container'
                return response
                #validar tipo_demissao
            if request.POST.get('tipo_demissao') in ['','-1', None] :
                context = {
                'text_error': "Selecione Tipo de Rescisão"
                }
                
                response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                response['HX-Retarget'] = '#error-container'
                return response

            
        elif situacao == 'AFASTADO INSS - POR DOENÇA' or situacao == 'AFASTADO INSS - POR ACIDENTE':
                #validar data_inicio_afastamento
            if request.POST.get('data_inicio_afastamento') in ['','-1', None] :
                context = {
                'text_error': "Campo 'Início Afastamento' Vazio"
                }
                
                response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                response['HX-Retarget'] = '#error-container'
                return response
                #validar data_fim_afastamento
            if request.POST.get('data_fim_afastamento') in ['','-1', None] :
                context = {
                'text_error': "Campo 'Fim Afastamento' Vazio"
                }
                
                response =  render(request, template_name='funcionarios/fragmentos/funcionarios/error_form_funcionario.html', context=context)
                response['HX-Retarget'] = '#error-container'
                return response

