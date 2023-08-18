from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from estoque.models import *
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='login/')
@csrf_exempt
def inicio_estoquev2(request, template_name = 'estoque_v2/inicio_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'INICIO'
        
        context = {
            'menu_ativo' : _menu_ativo,
         
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
    
@login_required(login_url='login/')
@csrf_exempt
def requisicoes_estoquev2(request, template_name = 'estoque_v2/requisicoes_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'REQUISIÇÃO'
     
        context = {
            'menu_ativo' : _menu_ativo,
         
        }
        return render(request, template_name , context)
    
@login_required(login_url='login/')
@csrf_exempt
def cadastrar_estoquev2(request, template_name = 'estoque_v2/cadastrar_estoque.html'):

    if request.method == 'GET':
        _menu_ativo = 'CADASTRAR'
     
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