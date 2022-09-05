from tarefas.models import Tarefa
from tarefas.forms import TarefasForm
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import Http404


@login_required(login_url='login/')
@csrf_exempt
def home_index(request):
    """
    Retorna a página inicial do sistema
    """

    today_date = datetime.now()
    try:
        eventos_do_dia = Tarefa.objects.all().filter(usuario=request.user).filter(data_inclusao__date__lte=today_date).filter(data_conclusao__date__gte=today_date).filter(feito=False)
        tarefas = Tarefa.objects.all().filter(usuario=request.user).filter(feito=False)
        tarefa_exibir = Tarefa.objects.all().filter(feito=False).latest('pk')
    
        context = {
                'tarefas': tarefas,
                'eventos_do_dia': eventos_do_dia,
                'tarefa_exibir': tarefa_exibir
            }
    
        template_name = 'home.html'
        return render(request, template_name , context)
    
    except Tarefa.DoesNotExist:
        raise Http404("ERRO: Evento não existe!")
    

@login_required(login_url='login/')
@csrf_exempt
def criar_tarefas(request):
    
    context = {
             'form': TarefasForm()
         }
    
    template_name = 'tarefas/fragmentos/modal-criar-tarefa.html'
    return render(request, template_name , context)

@login_required(login_url='login/')
@csrf_exempt
def salvar_tarefa(request):
    form = TarefasForm(request.POST)
    criado = False
    
    try:  
        if form.is_valid():
            form.instance.usuario = request.user
            form.instance.cor = request.POST.get('bttColor')
            if not form.instance.data_conclusao:
                form.instance.data_conclusao = form.instance.data_inclusao
                
            
            novo = form.save()
            texto = f"<i class='fas fa-check'></i> Salvo com Sucesso (id: {novo.pk})"
            criado = True
        
        template_name = 'tarefas/fragmentos/modal-criar-tarefa.html'
        
        context = {
                'tarefas': Tarefa.objects.all().filter(usuario=request.user),
                'texto': texto,
                'novo': novo,
                'form': TarefasForm(),
                'criado': criado
            }
        
        return render(request, template_name , context)
    except Tarefa.DoesNotExist:
        raise Http404("ERRO: Evento não pode ser salvo!")

@login_required(login_url='login/')
@csrf_exempt
def ver_tarefa(request, pk):
    template_name = 'tarefas/ver-tarefa.html'
    try:
        tarefa = Tarefa.objects.get(pk=pk)
        context = {
                'tarefa': tarefa,
                'tarefas': Tarefa.objects.all().filter(usuario=request.user).filter(feito=False),
                'tarefas_finalizadas': Tarefa.objects.all().filter(usuario=request.user).filter(feito=True),
            }
        return render(request, template_name , context)
    except Tarefa.DoesNotExist:
        raise Http404("ERRO: Evento não existe!")

@login_required(login_url='login/')
@csrf_exempt
def excluir_tarefa(request, pk):
    template_name = 'tarefas/fragmentos/ver-tarefa-detalhes.html'
    try:
        Tarefa.objects.filter(pk=pk).delete()
        
        context = {
                'tarefas': Tarefa.objects.all().filter(usuario=request.user),
            }
        return render(request, template_name , context)
    except Tarefa.DoesNotExist:
        raise Http404("ERRO: Evento não existe ou já foi excluído!")
    
@login_required(login_url='login/')
@csrf_exempt
def ver_tarefa_detalhes(request, pk):
    try:
        template_name = 'tarefas/fragmentos/ver-tarefa-detalhes.html'
        
        context = {
                'tarefa': Tarefa.objects.get(pk=pk),
            }
        return render(request, template_name , context)
    except Tarefa.DoesNotExist:
        raise Http404("ERRO: Evento não existe ou já foi excluído!")
    
@login_required(login_url='login/')
@csrf_exempt
def editar_tarefa(request, pk):
    form = TarefasForm()
    try:
        template_name = 'tarefas/fragmentos/editar-tarefa-detalhes.html'
        
        context = {
                'tarefa_edit': Tarefa.objects.get(pk=pk),
                'form': form
            }
        return render(request, template_name , context)
    except Tarefa.DoesNotExist:
        raise Http404("ERRO: Evento não existe ou já foi excluído!")
    
@login_required(login_url='login/')
@csrf_exempt
def salvar_edicao_tarefa(request, pk):
    obj = Tarefa.objects.get(pk=pk)
    form = TarefasForm(request.POST, instance=obj)
    template_name = 'tarefas/fragmentos/ver-tarefa-detalhes.html'
    
    try:  
        if form.is_valid():
            
            form.instance.usuario = request.user
            form.instance.cor = request.POST.get('btt_editColor')
            
            if not form.instance.data_conclusao:
                form.instance.data_conclusao = form.instance.data_inclusao
                          
            form.save()
        
            context = {
                'tarefa': Tarefa.objects.get(pk=pk),
            }
        
            return render(request, template_name , context)
    except Tarefa.DoesNotExist:
       
        raise Http404("ERRO: Tarefa Não existe!")
    
    else:

        raise Http404("ERRO: Evento não pode ser salvo!") 
   
@login_required(login_url='login/')
@csrf_exempt
def marcar_realizar_tarefa(request, pk):
    template_name = 'tarefas/fragmentos/ver-tarefa-detalhes.html'
    
    try: 
        obj = Tarefa.objects.get(pk=pk)    
        if obj.feito:
            obj.feito = False
        else:
            obj.feito = True        
        
        obj.save()
    
        context = {
            'tarefa': Tarefa.objects.get(pk=pk),
        }
    
        return render(request, template_name , context)
    except Tarefa.DoesNotExist:
        raise Http404("ERRO: Tarefa Não existe!")
    

   