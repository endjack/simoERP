from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from obras.models import Obra,Local
from funcionarios.models import Funcionario
from engenharia.models import *
from django.views.decorators.csrf import csrf_exempt
from simo.settings import PROJECT_ROOT
from django.http import FileResponse
from django.http.response import HttpResponse, Http404
from weasyprint import HTML
from django.template.loader import render_to_string

@login_required(login_url='login/')
def home_engenharia(request, template_name = 'engenharia/home.html'):
    
    if request.method == 'GET':
    
        date = datetime.now()
        obras = Obra.objects.filter(concluido=False).filter(invisivel=False)        
             
        context = {
            'date': date,
            'obras':obras,
        }
        
        return render(request, template_name , context)

@login_required(login_url='login/')
def home_obras_ver_servicos(request, pk, template_name = 'engenharia/home_ordens.html'):
     
     if request.method == 'GET': 
   
   
        obra = Obra.objects.get(pk=pk)
        # ordens = OrdemServicoObras.objects.filter(obra=obra)
        ultimas_10 = OrdemServicoObras.objects.filter(obra=obra).order_by('-pk')[:10]
        # os_nao_iniciados = ordens.filter(situacao=0).count()
        # os_em_andamento= ordens.filter(situacao=1).count()
        # os_finalizados = ordens.filter(finalizado=True).count()
            
        context = {
     
            'obra': obra,
            'ordens': ultimas_10,
            # 'os_nao_iniciados': os_nao_iniciados,
            # 'os_em_andamento': os_em_andamento,
            # 'os_finalizados': os_finalizados,
        }

        
        return render(request, template_name , context)

@login_required(login_url='login/')
def ver_todas_os_por_obra(request, pk, template_name = 'engenharia/ver_todas_ordens.html'):
     
     if request.method == 'GET': 
   
   
        obra = Obra.objects.get(pk=pk)
        ordens = OrdemServicoObras.objects.filter(obra=obra)
        print(f'---------    > {ordens}')
        ordens_nao_finalizadas = ordens.filter(finalizado=False) 
        os_nao_iniciados = ordens_nao_finalizadas.filter(situacao=0).count()
        os_em_andamento= ordens_nao_finalizadas.filter(situacao=1).count()
        os_finalizados = ordens.filter(finalizado=True).count()
            
        context = {
     
            'obra': obra,
            'ordens': ordens,
            'os_nao_iniciados': os_nao_iniciados,
            'os_em_andamento': os_em_andamento,
            'os_finalizados': os_finalizados,
            'situacao': SITUAÇÃO,
            
        }

        
        return render(request, template_name , context)
        
@login_required(login_url='login/')
def obras_nova_orden_servico(request, pk, template_name = 'engenharia/nova_ordem_servico.html'):
    
    if request.method == 'GET':
            

        obra = Obra.objects.get(pk=pk)
        locais = Local.objects.all()
        situacao = SITUAÇÃO
              
        context = {

            'obra': obra,
            'locais': locais,
            'situacao': situacao,
            'editar': False,
        }
        
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def obras_salvar_nova_orden_servico(request, pk):
    
    
    date = datetime.now()
    obra = Obra.objects.get(pk=pk)
   
    
    if request.method == 'POST':
        
        data_recebida = datetime.strptime(request.POST.get('data_recebida'), '%Y-%m-%d') or None
        situacao = request.POST.get('situacao') or ''
        num_os = request.POST.get('num_os') or ''
        unidade = request.POST.get('unidade') or None
        local = request.POST.get('local') or None
        endereco = request.POST.get('endereco') or ''
        servicos = request.POST.get('servicos') or ''
        obs = request.POST.get('obs') or ''
        data_inicio = datetime.strptime(request.POST.get('data_inicio'), '%Y-%m-%d') or None
        data_prazo = datetime.strptime(request.POST.get('data_prazo'), '%Y-%m-%d') or None
         
        local_atual = Local.objects.get(pk=int(local)) 
       
        nova_ordem = OrdemServicoObras.objects.create(numero_os=int(num_os),
                                         solicitante=None,
                                         encarregado=None,
                                         servicos=servicos,
                                         local = local_atual,
                                         situacao=int(situacao),
                                         obra=obra,
                                         data_recebimento = data_recebida,
                                         data_inicio = data_inicio,
                                         data_prazo=data_prazo,
                                         obs=obs,
                                         )       
        
          
    return redirect('obra_detalhar_os', pk=pk, os=nova_ordem.pk)
    
@login_required(login_url='login/')
@csrf_exempt
def obras_editar_orden_servico(request, pk, os, template_name = 'engenharia/nova_ordem_servico.html'):

    if request.method == 'GET':
        
        date = datetime.now()
        obra = Obra.objects.get(pk=pk)
        locais = Local.objects.all()
        os = OrdemServicoObras.objects.get(obra=obra,pk=os)
              
        context = {
            'date': date,
            'obra': obra,
            'locais': locais,
            'os': os,
            'situacao': SITUAÇÃO,
            'editar': True
       
        }
        
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def obras_salvar_editar_orden_servico(request, pk, os):
   
    obra = Obra.objects.get(pk=pk)
    os_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)

    
    if request.method == 'POST':
        
        data_recebida = datetime.strptime(request.POST.get('data_recebida'), '%Y-%m-%d') or None
        situacao = request.POST.get('situacao') or ''
        num_os = request.POST.get('num_os') or ''
        unidade = request.POST.get('unidade') or None
        local = request.POST.get('local') or None
        endereco = request.POST.get('endereco') or ''
        servicos = request.POST.get('servicos') or ''
        obs = request.POST.get('obs') or ''
        data_inicio = datetime.strptime(request.POST.get('data_inicio'), '%Y-%m-%d') or None
        data_prazo = datetime.strptime(request.POST.get('data_prazo'), '%Y-%m-%d') or None
         
        local_atual = Local.objects.get(pk=int(local)) 
       
        os_atual.numero_os=int(num_os)
        os_atual.solicitante=None
        os_atual.encarregado=None
        os_atual.servicos=servicos
        os_atual.local = local_atual
        os_atual.situacao=int(situacao)
        os_atual.data_recebimento = data_recebida
        os_atual.data_inicio = data_inicio
        os_atual.data_prazo=data_prazo
        os_atual.obs=obs
        
        
        os_atual.save()
                                                
        
    
    return redirect('obra_detalhar_os', pk=pk, os=os)
    
@login_required(login_url='login/')
@csrf_exempt
def obra_excluir_os(request, pk, os):
    
    if request.method == 'GET':
        obra = Obra.objects.get(pk=pk)
        os_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
        os_atual.get_funcionarios_by_os().delete()
        os_atual.get_imagens_by_os().delete()
        os_atual.get_files_by_os().delete()
        os_atual.get_rdos_by_os().delete()
        os_atual.delete()            
    
        return redirect('home_obra_os', pk=pk)

@login_required(login_url='login/')
@csrf_exempt
def obras_detalhar_orden_servico(request, pk, os, template_name = 'engenharia/detalhar_ordem.html'):
        
    if request.method == 'GET':
    
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
        arquivos = ordem_atual.get_files_by_os().order_by('nome')
        diarios = DiarioDeObraOs.objects.filter(ordem_servico = ordem_atual).order_by('-data')
        funcionariosOS = FuncionarioOS.objects.filter(ordem_servico = ordem_atual)
        
                
        context = {
        
            'obra': obra,
            'ordem_atual': ordem_atual,
            'categorias': categorias,
            'arquivos': arquivos,
            'diarios': diarios,
            'funcionariosOS': funcionariosOS,


        }
        
        return render(request, template_name , context)

@login_required(login_url='login/')
@csrf_exempt
def obras_finalizar_orden_servico(request, pk, os, template_name = 'engenharia/detalhar_ordem.html'):
    
    obra = Obra.objects.get(pk=pk)
    ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
    categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
    arquivos = ordem_atual.get_files_by_os().order_by('nome')
    diarios = DiarioDeObraOs.objects.filter(ordem_servico = ordem_atual).order_by('-data')
        
        
    if request.method == 'POST':
    
        data_recebida = datetime.strptime(request.POST.get('data_conclusao'), '%Y-%m-%d')
        
        
        ordem_atual.finalizado = True
        ordem_atual.data_conclusao = data_recebida
        ordem_atual.save()
        
        print(f'-------------------------OS Nº {ordem_atual.numero_os} - FINALIZADA')
        
                
    context = {
    
        'obra': obra,
        'ordem_atual': ordem_atual,
        'categorias': categorias,
        'arquivos': arquivos,
        'diarios': diarios,


    }
    
    return render(request, template_name , context)

@login_required(login_url='login/')
@csrf_exempt
def obras_mudar_finalizar_orden_servico(request, pk, os, template_name = 'engenharia/detalhar_ordem.html'):
    
    obra = Obra.objects.get(pk=pk)
    ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
    categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
    arquivos = ordem_atual.get_files_by_os().order_by('nome')
    diarios = DiarioDeObraOs.objects.filter(ordem_servico = ordem_atual).order_by('-data')
        
        
    ordem_atual.finalizado = False
    ordem_atual.data_conclusao = None
    ordem_atual.situacao = 1
    ordem_atual.save()
    
    print(f'-------------------------OS Nº {ordem_atual.numero_os} mudada para EM ANDAMENTO')
    
                
    context = {
    
        'obra': obra,
        'ordem_atual': ordem_atual,
        'categorias': categorias,
        'arquivos': arquivos,
        'diarios': diarios,


    }
    
    return render(request, template_name , context)

#--------------------------
#---------------------------VIEWS IMAGENS EM ORDEM DE SERVIÇO
#--------------------------

@login_required(login_url='login/')
@csrf_exempt
def obras_imagens_orden_servico(request, pk, os, template_name = 'engenharia/imagens_ordem.html'):
        
    if request.method == 'GET':
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
        imagens = ImagemOS.objects.filter(ordem_servico = ordem_atual)
             
        context = {
      
            'obra': obra,
            'ordem_atual': ordem_atual,
            'categorias': categorias,
            'imagens': imagens,


        }
        
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def obras_imagens_inserir_categoria_orden_servico(request, pk, os, template_name = 'engenharia/fragmentos/modal-inserir-categoria.html'):
        
    if request.method == 'GET':    
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
        imagens = ImagemOS.objects.filter(ordem_servico = ordem_atual)
             
        context = {
      
            'obra': obra,
            'ordem_atual': ordem_atual,
            'categorias': categorias,
            'imagens': imagens,


        }
        
        return render(request, template_name , context)

@login_required(login_url='login/')
@csrf_exempt    
def obras_imagens_salvar_categoria_orden_servico(request, pk, os, template_name = 'engenharia/imagens_ordem.html'):
        
        
    if request.method == 'POST':
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
        categoria = request.POST.get('categoria') or ''
        CategoriaImagem.objects.create(categoria = categoria,
                                        ordem_servico = ordem_atual)
        

    return redirect('obra_imagens_os', pk=pk, os=os)


@login_required(login_url='login/')
@csrf_exempt   
def obras_inserir_imagem_em_categoria_orden_servico(request, pk, os, template_name = 'engenharia/fragmentos/modal-inserir-imagem.html'):
        
        if request.method == 'GET':
        
            obra = Obra.objects.get(pk=pk)
            ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
            categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
            
           
            context = {
        
                'obra': obra,
                'ordem_atual': ordem_atual,
                'categorias': categorias,

            }
            
            return render(request, template_name , context)


@login_required(login_url='login/')
@csrf_exempt    
def obras_salvar_imagem_em_categoria_orden_servico(request, pk, os):
        
    if request.method == 'GET':
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
        rdo_atual = None
        template_name = 'engenharia/detalhar_rdo.html'
        
        context = {
    
            'obra': obra,
            'ordem_atual': ordem_atual,
            'categorias': categorias,
            'rdo_atual': rdo_atual,

        }
        
        return render(request, template_name , context)
            
        
    if request.method == 'POST':
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
        categoria_rdo= request.POST.get('rdo_id') or ''
        
        if categoria_rdo == '':
            categoria_imagem = request.POST.get('categoria') or ''
            categoria_atual = CategoriaImagem.objects.get(categoria = categoria_imagem, ordem_servico = ordem_atual)
            url = redirect('obra_imagens_os', pk=pk, os=os)
        else:
            rdo_atual = DiarioDeObraOs.objects.get(pk=categoria_rdo)
            
            if not rdo_atual.fotos:
                categoria_atual = CategoriaImagem.objects.create(categoria = f'Diário De Obra ({rdo_atual.data.strftime("%d/%m/%Y")})',
                                                                ordem_servico = ordem_atual) 
                rdo_atual.fotos = categoria_atual
                rdo_atual.save() 
            else:
                categoria_atual = rdo_atual.fotos
            
            url = redirect('detalhar_rdo_rdo_orden_servico', pk=pk, os=os, rdo=rdo_atual.pk)    
            
        # UPLOAD DE IMAGENS
        imagens = request.FILES.getlist('imagem') or None
        
        print(f'--------------------{imagens}')
        
        if imagens is not None:
            for image in imagens:   
                ImagemOS.objects.create(categoria = categoria_atual, 
                                        imagem = image,
                                        ordem_servico = ordem_atual)
        else:
            response = HttpResponse('<span style="color:red"><i>Sem imagem</i></span>')
            response['HX-Retarget'] = '#error_imagem'
            response['HX-Swap'] = 'innerHTML'
            return response
                    
        return url

           
@login_required(login_url='login/')
@csrf_exempt    
def obras_excluir_imagem_orden_servico(request, pk, os, im, template_name = 'engenharia/imagens_ordem.html'):
    
          
    if request.method == 'POST':
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)

        try:
            imagem_atual =     ImagemOS.objects.get(ordem_servico= ordem_atual,pk=im) 
        except ImagemOS.DoesNotExist:
            raise Http404("IMAGEM JÁ DELETADA OU NÃO EXISTE!")
        

        print(f'---------- IMAGEM DELETADA {imagem_atual}---------------------')
        imagem_atual.delete()
    
        return redirect('obra_imagens_os', pk=pk, os=os)

       
@login_required(login_url='login/')
@csrf_exempt    
def obras_excluir_imagem_orden_servico_em_rdo(request, pk, os, im, rdo, template_name = 'engenharia/detalhar_rdo.html'):
             
        if request.method == 'POST':
            obra = Obra.objects.get(pk=pk)
            ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
            try:
                imagem_atual =     ImagemOS.objects.get(ordem_servico= ordem_atual, pk=im) 
            except ImagemOS.DoesNotExist:
                raise Http404("IMAGEM JÁ DELETADA OU NÃO EXISTE!")
            

            print(f'---------- IMAGEM DELETADA {imagem_atual}---------------------')
            imagem_atual.delete()
        
    
            return redirect('detalhar_rdo_rdo_orden_servico', pk=pk, os=os, rdo=rdo)
    
        
@login_required(login_url='login/')
@csrf_exempt    
def obras_editar_categoria_imagem_orden_servico(request, pk, os, im, template_name = 'engenharia/imagens_ordem.html'):
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
        
        if request.method == 'POST':
        
            categoria_post = request.POST.get('nova_categoria') or '' 
            imagem_atual = ImagemOS.objects.get(ordem_servico = ordem_atual, pk=im) 
            categoria_atual = CategoriaImagem.objects.get(ordem_servico = ordem_atual, categoria = categoria_post)
            

            print(f'-EDITADO IMAGEM {imagem_atual.imagem.name}----------- CATEGORIA ANTES: {imagem_atual.categoria.categoria} --------CATEGORIA DEPOIS: {categoria_atual} --')
            
            
            # MUDAR CATEGORIA DA IMAGEM
            imagem_atual.categoria = categoria_atual
            imagem_atual.save()
       
        context = {
    
            'obra': obra,
            'ordem_atual': ordem_atual,
            'categorias': categorias,

        }
        
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt    
def obras_editar_categoria_orden_servico(request, pk, os, cat, template_name = 'engenharia/imagens_ordem.html'):
        
        
        if request.method == 'POST':
            obra = Obra.objects.get(pk=pk)
            ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
        
            categoria_atual = CategoriaImagem.objects.get(ordem_servico = ordem_atual, pk = cat)
            categoria_edit = request.POST.get('edit_categoria') or '' 
            
            # EDITAR CATEGORIA
            categoria_atual.categoria = categoria_edit
            categoria_atual.save()

            print(f'-EDITADO CATEGORIA {categoria_edit} --------CATEGORIA DEPOIS: {categoria_atual.categoria} --')
        
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
       
        context = {
    
            'obra': obra,
            'ordem_atual': ordem_atual,
            'categorias': categorias,

        }
        
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt    
def obras_excluir_categoria_orden_servico(request, pk, os, cat, template_name = 'engenharia/imagens_ordem.html'):
        
        
        if request.method == 'POST':
            obra = Obra.objects.get(pk=pk)
            ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
        
            categoria_atual = CategoriaImagem.objects.get(ordem_servico = ordem_atual, pk = cat)
            categoria_para_deletar = categoria_atual.categoria

            
            # EXCLUIR IMAGENS
            imagens = categoria_atual.get_imagens_by_category()
            imagens.delete()
            
            # EXCLUIR CATEGORIA
            categoria_atual.delete()
            
            print(f'-DELETADO CATEGORIA {categoria_para_deletar}')
            
            return redirect('obra_imagens_os', pk=pk, os=os)
 
        
@login_required(login_url='login/')
@csrf_exempt    
def dowload_imagens_categoria_orden_servico(request, pk, os, cat):
        
        categoria_atual = CategoriaImagem.objects.get(pk = cat)
   

        # import zipfile
        # # DOWNLOAD DE IMAGENS EM ZIP
        # imagens = categoria_atual.get_imagens_by_category()
        
        # print(f'{imagens}')
       
        # z = zipfile.ZipFile(f'{categoria_atual}_imagens.zip', 'w', zipfile.ZIP_DEFLATED)
        
        
        
        # for im in imagens:
        #     filepath = os.path.join(PROJECT_ROOT, im.imagem.url)
        #     z.write(filepath)
           
            
        # z.close()        
      
        
        return FileResponse('z')


#--------------------------
#---------------------------VIEWS DOCUMENTOS EM ORDEM DE SERVIÇO
#--------------------------
    
@login_required(login_url='login/')
@csrf_exempt
def documentos_orden_servico(request, pk, os, template_name = 'engenharia/documentos_ordem.html'):

    if request.method == 'GET':
    
        date = datetime.now()
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        arquivos = ordem_atual.get_files_by_os().order_by('nome')
        
        context = {
            'date': date,
            'obra': obra,
            'ordem_atual': ordem_atual,
            'arquivos': arquivos,
        }
        return render(request, template_name , context)
            
    
@login_required(login_url='login/')
@csrf_exempt
def salvar_documento_os(request, pk, os, template_name = 'engenharia/documentos_ordem.html'):
    print('----------')
    print(f'---------> VIEW: salvar_documento_os') 
    print('----------')
           
  
    obra = Obra.objects.get(pk=pk)
    ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        

    if request.method == 'POST':
        
        # UPLOAD FILES
        file_field = request.FILES["upload_file"] or None
        file_name = request.POST.get('nome_file') or '' 
               
         
        file = DocumentoOS.objects.create(file = file_field, 
                                   nome = file_name,
                                   ordem_servico = ordem_atual)
        
        if(file.nome == ''):
            file.nome = file.filename()
            file.save()
            
        print(f'-UPLOAD DE DOCUMENTO {file.nome} -------- URL: {file.filename()} --')
     
        
    arquivos = ordem_atual.get_files_by_os().order_by('nome')
        
    context = {
     
        'obra': obra,
        'ordem_atual': ordem_atual,
        'arquivos': arquivos,
    }
    return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def excluir_arquivo_os(request, pk, os, file, template_name = 'engenharia/documentos_ordem.html'):
    print('----------')
    print(f'---------> VIEW: excluir_arquivo_os') 
    print('----------')
        
    if request.method == 'GET':
   
    
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        file_atual = DocumentoOS.objects.get(ordem_servico = ordem_atual, pk=file)

        print(f'-DELETADO {file_atual.filename}---------------------')
        
        file_atual.delete()
        
        arquivos = ordem_atual.get_files_by_os().order_by('nome')
            
        context = {
          
            'obra': obra,
            'ordem_atual': ordem_atual,
            'arquivos': arquivos,
        }
        return render(request, template_name , context)
    

#View Relatório Diário de Obra -----------------------------------------------------

    
@login_required(login_url='login/')
@csrf_exempt
def rdo_orden_servico(request, pk, os, template_name = 'engenharia/rdo_ordem.html'):

    if request.method == 'GET':
    
   
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        diarios = DiarioDeObraOs.objects.filter(ordem_servico = ordem_atual).order_by('-data')
  
        
        context = {
    
            'obra': obra,
            'ordem_atual': ordem_atual,
            'diarios': diarios,

          
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def salvar_rdo_orden_servico(request, pk, os, template_name = 'engenharia/rdo_ordem.html'):
    

    obra = Obra.objects.get(pk=pk)
    ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)


    if request.method == 'POST':
        
        data_RDO = datetime.strptime(request.POST.get('data'), '%Y-%m-%d') or None
        tempo_manha = request.POST.get('tempo_manha') or ''
        tempo_tarde = request.POST.get('tempo_tarde') or ''
        mao_de_obra = request.POST.get('mao_de_obra') or ''
        equipamentos = request.POST.get('equipamentos') or ''
        atividades = request.POST.get('atividades') or ''
        ocorrencias = request.POST.get('ocorrencias') or ''
        usuario = request.user
        
        
        DiarioDeObraOs.objects.create(
            data=data_RDO,
            atividades = atividades,
            usuario = usuario,
            ordem_servico = ordem_atual,
            tempo_manha = tempo_manha,
            tempo_tarde = tempo_tarde,
            equipamentos = equipamentos,
            mao_de_obra = mao_de_obra,
            ocorrencias = ocorrencias,
            fotos = None 
        )
    
        diarios = DiarioDeObraOs.objects.filter(ordem_servico = ordem_atual).order_by('-data')
        
    context = {
        'obra': obra,
        'ordem_atual': ordem_atual,
        'diarios': diarios,
        

    }
    return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def editar_rdo_orden_servico(request, pk, os, template_name = 'engenharia/rdo_ordem.html'):
    

    obra = Obra.objects.get(pk=pk)
    ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)


    if request.method == 'POST':
        
        data_RDO = datetime.strptime(request.POST.get('data'), '%Y-%m-%d') or None
        tempo_manha = request.POST.get('tempo_manha') or ''
        tempo_tarde = request.POST.get('tempo_tarde') or ''
        mao_de_obra = request.POST.get('mao_de_obra') or ''
        equipamentos = request.POST.get('equipamentos') or ''
        atividades = request.POST.get('atividades') or ''
        ocorrencias = request.POST.get('ocorrencias') or ''
        usuario = request.user
        
        
        DiarioDeObraOs.objects.create(
            data=data_RDO,
            atividades = atividades,
            usuario = usuario,
            ordem_servico = ordem_atual,
            tempo_manha = tempo_manha,
            tempo_tarde = tempo_tarde,
            equipamentos = equipamentos,
            mao_de_obra = mao_de_obra,
            ocorrencias = ocorrencias,
            fotos = None 
        )
    
        diarios = DiarioDeObraOs.objects.filter(ordem_servico = ordem_atual).order_by('-data')
        
    context = {
        'obra': obra,
        'ordem_atual': ordem_atual,
        'diarios': diarios,
        

    }
    return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def salvar_editar_rdo_orden_servico(request, pk, os, rdo, template_name = 'engenharia/detalhar_rdo.html'):

    obra = Obra.objects.get(pk=pk)
    ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
    rdo_atual = DiarioDeObraOs.objects.get(ordem_servico = ordem_atual, pk=rdo)


    if request.method == 'POST':
        
        data_RDO = datetime.strptime(request.POST.get('data_editar'), '%Y-%m-%d') or None
        tempo_manha = request.POST.get('tempo_manha_editar') 
        tempo_tarde = request.POST.get('tempo_tarde_editar') or ''
        mao_de_obra = request.POST.get('mao_de_obra_editar') or ''
        equipamentos = request.POST.get('equipamentos_editar') or ''
        atividades = request.POST.get('atividades_editar') or ''
        ocorrencias = request.POST.get('ocorrencias_editar') or ''
 
        
        rdo_atual.data=data_RDO
        rdo_atual.atividades = atividades
        rdo_atual.tempo_manha = tempo_manha
        rdo_atual.tempo_tarde = tempo_tarde
        rdo_atual. equipamentos = equipamentos
        rdo_atual.mao_de_obra = mao_de_obra
        rdo_atual.ocorrencias = ocorrencias
        
        rdo_atual.save()
    

        context = {
            'obra': obra,
            'ordem_atual': ordem_atual,
            'rdo_atual': rdo_atual,
        }
        return render(request, template_name , context)


@login_required(login_url='login/')
@csrf_exempt
def detalhar_rdo_rdo_orden_servico(request, pk, os, rdo, template_name = 'engenharia/detalhar_rdo.html'):

    if request.method == 'GET':
    
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        rdo_atual = DiarioDeObraOs.objects.get(ordem_servico = ordem_atual, pk = rdo)
  
        context = {
          
            'obra': obra,
            'ordem_atual': ordem_atual,
            'rdo_atual': rdo_atual,

          
        }
        
        return render(request, template_name , context)

@login_required(login_url='login/')
@csrf_exempt
def excluir_rdo_orden_servico(request, pk, os, rdo, template_name = 'engenharia/rdo_ordem.html'):

    if request.method == 'GET':
    
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(pk=os)
        rdo_atual = DiarioDeObraOs.objects.get(pk = rdo)
        
        
        if request.GET.getlist('excluir_fotos'):
            try:
                del_categoria = rdo_atual.fotos.delete()
            finally:
                rdo_atual.delete()
                pass
            
        else:
            try:
                rdo_atual.delete()
            finally:
                pass
        
        
        diarios = DiarioDeObraOs.objects.filter(ordem_servico = ordem_atual).order_by('-data')
        context = {
          
            'obra': obra,
            'ordem_atual': ordem_atual,
            'diarios': diarios,

          
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def hx_verificar_numero_os(request):

    if request.method == 'GET':
    
        numero_obra = request.GET.get('num_obra')
        numero_os_input = request.GET.get('num_os')
        
        numero_livre = OrdemServicoObras.objects.filter(obra=int(numero_obra)).filter(numero_os = int(numero_os_input))
        
        if numero_livre:
            return HttpResponse('Nº de Ordem de Serviço já Existe!')
        else:  
            return HttpResponse('')
    
    
@login_required(login_url='login/')
@csrf_exempt
def hx_filtrar_os(request, pk, template_name = 'engenharia/fragmentos/resultados_filter_ver_todas_os.html'):

    if request.method == 'GET':
        
        situacao =  int(request.GET.get('situacao'))
              
        obra = Obra.objects.get(pk=pk)
        ordens = OrdemServicoObras.objects.filter(obra=obra)
        ordens_nao_finalizadas = ordens.filter(finalizado=False) 
        
        if situacao == 0:
            ordens = ordens_nao_finalizadas.filter(situacao=0)  #Não Iniciado             
        elif situacao == 1:
            ordens = ordens_nao_finalizadas.filter(situacao=1) #Em andamento              
        elif situacao == 2:
            ordens = ordens_nao_finalizadas.filter(situacao=2)  #Pendente             
        elif situacao == 3:
            ordens = ordens_nao_finalizadas.filter(situacao=3)  #Paralisado                        
        elif situacao == -9:
            ordens = ordens.filter(finalizado=True)  #Finalizados             
        else:
            pass  #todos            
      
        
        context = {
          
            'obra': obra,
            'ordens': ordens,

          
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def imprimir_relatorio_fotografico_manut_viaria(request, pk, os, template_name = 'engenharia/fragmentos/impressoes/imprimir_rel_fotos_modelo_viario.html'):

    if request.method == 'GET':
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra = obra, pk=os)
        data_inicio = datetime.strptime(request.GET.get('data_relatorio_inicio'), '%Y-%m-%d')
        data_final = datetime.strptime(request.GET.get('data_relatorio_fim'), '%Y-%m-%d')
        data_relatorio = datetime.strptime(request.GET.get('data_relatorio'), '%Y-%m-%d')
        
        
        context = {
            
            'obra': obra,
            'ordem_atual': ordem_atual,
            'data_inicio': data_inicio,
            'data_final': data_final,
            'data_relatorio': data_relatorio,

            
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def imprimir_relatorio_fotografico_semsur(request, pk, os, template_name = 'engenharia/fragmentos/impressoes/imprimir_rel_fotos_modelo_semsur.html'):

    if request.method == 'GET':
        localidade = request.GET.get('localidade')
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra = obra, pk=os)
        data_inicio = datetime.strptime(request.GET.get('data_relatorio_inicio'), '%Y-%m-%d')
        data_final = datetime.strptime(request.GET.get('data_relatorio_fim'), '%Y-%m-%d')
        data_relatorio = datetime.strptime(request.GET.get('data_relatorio'), '%Y-%m-%d')
        
        if localidade == "" or localidade == None:
            localidade = ordem_atual.local.local
        
        
        context = {
            
            'obra': obra,
            'ordem_atual': ordem_atual,
            'data_inicio': data_inicio,
            'data_final': data_final,
            'data_relatorio': data_relatorio,
            'localidade': localidade,

            
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def imprimir_ordem_servico_individual(request, pk, os, template_name = 'engenharia/fragmentos/impressoes/imprimir_ordem_servico_individual.html'):

    if request.method == 'GET':
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
     
        
        
        context = {
            
            'obra': obra,
            'ordem_atual': ordem_atual,
            'categoriasOS': categorias,
   
     

            
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def imprimir_rdo_individual(request, pk, os, rdo, template_name = 'engenharia/fragmentos/impressoes/imprimir_rdo_individual.html'):

    if request.method == 'GET':
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra,pk=os)
        rdo_atual = DiarioDeObraOs.objects.get(pk = rdo)
        
        
        context = {
            
            'obra': obra,
            'ordem_atual': ordem_atual,
            'rdo_atual': rdo_atual,
     

            
        }
        return render(request, template_name , context)


    
@login_required(login_url='login/')
@csrf_exempt
def gerar_pdf_rdo_individual(request, pk, os, rdo, template_name = 'engenharia/fragmentos/impressoes/imprimir_rdo_individual.html'):


    if request.method == 'GET':
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        rdo_atual = DiarioDeObraOs.objects.get(ordem_servico = ordem_atual, pk = rdo)
        
        context = {
            
            'obra': obra,
            'ordem_atual': ordem_atual,
            'rdo_atual': rdo_atual,
     
            
        }
        
        return render(request, template_name , context)
  
        
#------------------------------------------------------------- DIARIO DE OBRA CONTRATO------------------------------------------------  


@login_required(login_url='login/')
@csrf_exempt
def ver_diario_obra_contrato(request, pk, template_name = 'engenharia/ver_diarios_obra_contrato.html'):


    if request.method == 'GET':
        obra = Obra.objects.get(pk=pk)
        diarios = DiarioDeObraContrato.objects.filter(obra=obra)
        
   
        context = {
            
            'obra': obra,
            'diarios': diarios,
            
        }
        
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def salvar_diario_obra_contrato(request, pk):

    if request.method == 'POST':
        obra = Obra.objects.get(pk=pk)
        
        data = datetime.strptime(request.POST.get('data'), '%Y-%m-%d') or None
        tempo_manha = request.POST.get('tempo_manha') 
        tempo_tarde = request.POST.get('tempo_tarde') or ''
        mao_de_obra = request.POST.get('mao_de_obra') or ''
        equipamentos = request.POST.get('equipamentos') or ''
        atividades = request.POST.get('atividades') or ''
        ocorrencias = request.POST.get('ocorrencias') or ''
 
        DiarioDeObraContrato.objects.create(
                        obra = obra,
                        data=data,
                        atividades = atividades,
                        tempo_manha = tempo_manha,
                        tempo_tarde = tempo_tarde,
                        equipamentos = equipamentos,
                        mao_de_obra = mao_de_obra,
                        ocorrencias = ocorrencias
                        )
      
        
        
        return redirect('ver_diario_obra_contrato', pk=pk)   


@login_required(login_url='login/')
@csrf_exempt
def detalhar_do_contrato(request, pk, do, template_name = 'engenharia/diariodeobracontrato/detalhar_do_contrato.html'):

    if request.method == 'GET':
        obra = Obra.objects.get(pk=pk)
        do_atual = DiarioDeObraContrato.objects.get(pk=do)
        
        context = {
            
            'obra': obra,
            'do_atual':do_atual

            
        }
        
        return render(request, template_name , context)





        

#------------------------------------------------------------- FUNCIONÁRIOS----------------------------------------------------------
        
@login_required(login_url='login/')
@csrf_exempt
def funcionarios_imagens_os(request, pk, os, template_name = 'engenharia/funcionarios_ordem.html'):

    if request.method == 'GET':
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        funcionarios = Funcionario.objects.all()
        funcionariosOS = FuncionarioOS.objects.filter(ordem_servico = ordem_atual)
        
        context = {
            
            'obra': obra,
            'ordem_atual': ordem_atual,
            'funcionarios': funcionarios,
            'funcionariosOS': funcionariosOS,
    
                
            }
            
        return render(request, template_name , context)  

        
@login_required(login_url='login/')
@csrf_exempt
def inserir_funcionarios_imagens_os(request, pk, os, func, template_name = 'engenharia/funcionarios_ordem.html'):
     
    if request.method == 'POST':
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        funcionario_atual = Funcionario.objects.get(pk = func)  
        FuncionarioOS.objects.create(funcionario = funcionario_atual, ordem_servico = ordem_atual)
        
        return redirect('funcionarios_imagens_os', pk=pk, os=os)    
    
  
        
@login_required(login_url='login/')
@csrf_exempt
def excluir_funcionarios_imagens_os(request, pk, os, func, template_name = 'engenharia/funcionarios_ordem.html'):

    if request.method == 'POST':
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(obra=obra, pk=os)
        funcionario_atual = FuncionarioOS.objects.get(ordem_servico = ordem_atual,pk = func)
        funcionario_atual.delete()
        
    return redirect('funcionarios_imagens_os', pk=pk, os=os)