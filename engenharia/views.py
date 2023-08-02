from datetime import datetime
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from obras.models import Obra,Local
from engenharia.models import *
from django.views.decorators.csrf import csrf_exempt
from simo.settings import PROJECT_ROOT
from django.http import FileResponse


@login_required(login_url='login/')
def home_engenharia(request, template_name = 'engenharia/home.html'):
    date = datetime.now()
    obras = Obra.objects.filter(concluido=False)
    
    if request.method == 'GET':
             
        context = {
            'date': date,
            'obras':obras,
        }

        
        return render(request, template_name , context)

@login_required(login_url='login/')
def home_obras_ver_servicos(request, pk, template_name = 'engenharia/home_ordens.html'):
    date = datetime.now()
    obra = Obra.objects.get(pk=pk)
    ordens = OrdemServicoObras.objects.filter(obra=obra)
    os_nao_iniciados = ordens.filter(situacao=0).count()
    os_em_andamento= ordens.filter(situacao=1).count()
    os_finalizados = ordens.filter(finalizado=True).count()
 
    if request.method == 'GET':
             
        context = {
            'date': date,
            'obra': obra,
            'ordens': ordens,
            'os_nao_iniciados': os_nao_iniciados,
            'os_em_andamento': os_em_andamento,
            'os_finalizados': os_finalizados,
        }

        
        return render(request, template_name , context)
        
@login_required(login_url='login/')
def obras_nova_orden_servico(request, pk, template_name = 'engenharia/nova_ordem_servico.html'):
    date = datetime.now()
    obra = Obra.objects.get(pk=pk)
    locais = Local.objects.all()
    situacao = SITUAÇÃO
 
    if request.method == 'GET':
             
        context = {
            'date': date,
            'obra': obra,
            'locais': locais,
            'situacao': situacao,
            'editar': False,
        }
        
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def obras_salvar_nova_orden_servico(request, pk, template_name = 'engenharia/home_ordens.html'):
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
        data_inicio = datetime.strptime(request.POST.get('data_inicio'), '%Y-%m-%d') or None
        data_prazo = datetime.strptime(request.POST.get('data_prazo'), '%Y-%m-%d') or None
         
        local_atual = Local.objects.get(pk=int(local)) 
       
        OrdemServicoObras.objects.create(numero_os=int(num_os),
                                         solicitante=None,
                                         encarregado=None,
                                         servicos=servicos,
                                         local = local_atual,
                                         situacao=int(situacao),
                                         obra=obra,
                                         data_recebimento = data_recebida,
                                         data_inicio = data_inicio,
                                         data_prazo=data_prazo
                                         )       
        
             
        context = {
            'date': date,
            'obra': obra,


        }
        
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def obras_editar_orden_servico(request, pk, os, template_name = 'engenharia/nova_ordem_servico.html'):

    date = datetime.now()
    obra = Obra.objects.get(pk=pk)
    locais = Local.objects.all()
    os = OrdemServicoObras.objects.get(pk=os)
 
    if request.method == 'GET':
             
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
def obras_salvar_editar_orden_servico(request, pk, os, template_name = 'engenharia/detalhar_ordem.html'):

    date = datetime.now()
    obra = Obra.objects.get(pk=pk)
    os_atual = OrdemServicoObras.objects.get(pk=os)
    categorias = CategoriaImagem.objects.filter(ordem_servico = os_atual).order_by('categoria')
    
    if request.method == 'POST':
        
        data_recebida = datetime.strptime(request.POST.get('data_recebida'), '%Y-%m-%d') or None
        situacao = request.POST.get('situacao') or ''
        num_os = request.POST.get('num_os') or ''
        unidade = request.POST.get('unidade') or None
        local = request.POST.get('local') or None
        endereco = request.POST.get('endereco') or ''
        servicos = request.POST.get('servicos') or ''
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
        
        os_atual.save()
                                                
        
             
        context = {
            
            'obra': obra,
            'ordem_atual': os_atual,
            'categorias': categorias,
        
        }
        
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def obras_detalhar_orden_servico(request, pk, os, template_name = 'engenharia/detalhar_ordem.html'):
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(pk=os)
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
        arquivos = ordem_atual.get_files_by_os().order_by('nome')
        
             
        context = {
      
            'obra': obra,
            'ordem_atual': ordem_atual,
            'categorias': categorias,
            'arquivos': arquivos,


        }
        
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def obras_imagens_orden_servico(request, pk, os, template_name = 'engenharia/imagens_ordem.html'):
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(pk=os)
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
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(pk=os)
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
            ordem_atual = OrdemServicoObras.objects.get(pk=os)
            
            categoria = request.POST.get('categoria') or ''
            
            CategoriaImagem.objects.create(categoria = categoria,
                                            ordem_servico = ordem_atual)
            
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
def obras_inserir_imagem_em_categoria_orden_servico(request, pk, os, template_name = 'engenharia/fragmentos/modal-inserir-imagem.html'):
        
        if request.method == 'GET':
        
            obra = Obra.objects.get(pk=pk)
            ordem_atual = OrdemServicoObras.objects.get(pk=os)
            categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
            
           
            context = {
        
                'obra': obra,
                'ordem_atual': ordem_atual,
                'categorias': categorias,

            }
            
            return render(request, template_name , context)

@login_required(login_url='login/')
@csrf_exempt    
def obras_salvar_imagem_em_categoria_orden_servico(request, pk, os, template_name = 'engenharia/imagens_ordem.html'):
        
        if request.method == 'POST':
    
            obra = Obra.objects.get(pk=pk)
            ordem_atual = OrdemServicoObras.objects.get(pk=os)
            categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
            
            
            categoria_imagem = request.POST.get('categoria') or ''
    
            categoria_atual = CategoriaImagem.objects.get(categoria = categoria_imagem)
            
            # UPLOAD DE IMAGENS
            imagens = request.FILES.getlist('imagem') or None
            
            for image in imagens:   
                ImagemOS.objects.create(categoria = categoria_atual, 
                                                imagem = image,
                                                ordem_servico = ordem_atual)
        
        
            context = {
        
                'obra': obra,
                'ordem_atual': ordem_atual,
                'categorias': categorias,

            }
            
            return render(request, template_name , context)
        
        
@login_required(login_url='login/')
@csrf_exempt    
def obras_excluir_imagem_orden_servico(request, pk, os, im, template_name = 'engenharia/imagens_ordem.html'):
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(pk=os)
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
        imagem_atual = ImagemOS.objects.get(pk=im)

        print(f'-DELETADO {imagem_atual}---------------------')
        
        imagem_atual.delete()
    
        context = {
    
            'obra': obra,
            'ordem_atual': ordem_atual,
            'categorias': categorias,

        }
        
        return render(request, template_name , context)
    
        
@login_required(login_url='login/')
@csrf_exempt    
def obras_editar_categoria_imagem_orden_servico(request, pk, os, im, template_name = 'engenharia/imagens_ordem.html'):
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(pk=os)
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
        categoria_post = request.POST.get('nova_categoria') or '' 
        imagem_atual = ImagemOS.objects.get(pk=im) 
        categoria_atual = CategoriaImagem.objects.get(categoria = categoria_post)
        

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
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(pk=os)
        categoria_atual = CategoriaImagem.objects.get(pk = cat)
        
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
        
        obra = Obra.objects.get(pk=pk)
        ordem_atual = OrdemServicoObras.objects.get(pk=os)
        categoria_atual = CategoriaImagem.objects.get(pk = cat)
        categoria_para_deletar = categoria_atual.categoria

        
        # EXCLUIR IMAGENS
        imagens = categoria_atual.get_imagens_by_category()
        imagens.delete()
        
        # EXCLUIR CATEGORIA
        categoria_atual.delete()
        
        print(f'-DELETADO CATEGORIA {categoria_para_deletar}')
        
        categorias = CategoriaImagem.objects.filter(ordem_servico = ordem_atual).order_by('categoria')
       
        context = {
    
            'obra': obra,
            'ordem_atual': ordem_atual,
            'categorias': categorias,

        }
        
        return render(request, template_name , context)
    
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
    
@login_required(login_url='login/')
@csrf_exempt
def documentos_orden_servico(request, pk, os, template_name = 'engenharia/documentos_ordem.html'):

    date = datetime.now()
    obra = Obra.objects.get(pk=pk)
    ordem_atual = OrdemServicoObras.objects.get(pk=os)
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
        
    date = datetime.now()
    obra = Obra.objects.get(pk=pk)
    ordem_atual = OrdemServicoObras.objects.get(pk=os)
    

 
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
            'date': date,
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
        
    date = datetime.now()
    obra = Obra.objects.get(pk=pk)
    ordem_atual = OrdemServicoObras.objects.get(pk=os)
    file_atual = DocumentoOS.objects.get(pk=file)

    print(f'-DELETADO {file_atual.filename}---------------------')
    
    file_atual.delete()
    
    arquivos = ordem_atual.get_files_by_os().order_by('nome')
        
    context = {
        'date': date,
        'obra': obra,
        'ordem_atual': ordem_atual,
        'arquivos': arquivos,
    }
    return render(request, template_name , context)
        