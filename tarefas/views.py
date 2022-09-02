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

    today_date = datetime.now()
    try:
        eventos_do_dia = Tarefa.objects.all().filter(usuario=request.user).filter(data_inclusao__date__lte=today_date).filter(data_conclusao__date__gte=today_date)
        tarefas = Tarefa.objects.all().filter(usuario=request.user)
    
        context = {
                'tarefas': tarefas,
                'eventos_do_dia': eventos_do_dia
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
                'form': TarefasForm(),
                'criado': criado
            }
        
        return render(request, template_name , context)
    except Tarefa.DoesNotExist:
        raise Http404("ERRO: Evento não pode ser salvo!")

@login_required(login_url='login/')
@csrf_exempt
def ver_tarefa(request, pk):
    try:
        tarefa = Tarefa.objects.get(pk=pk)
        template_name = 'tarefas/ver-tarefa.html'
        
        context = {
                'tarefa': tarefa,
                'tarefas': Tarefa.objects.all().filter(usuario=request.user).order_by('-pk')[:10],
            }
        return render(request, template_name , context)
    except Tarefa.DoesNotExist:
        raise Http404("ERRO: Evento não existe!")

@login_required(login_url='login/')
@csrf_exempt
def excluir_tarefa(request, pk):
    try:
        template_name = 'tarefas/fragmentos/ver-tarefa-detalhes.html'
        
        context = {
                'tarefas': Tarefa.objects.all().filter(usuario=request.user),
            }
        return render(request, template_name , context)
    except Tarefa.DoesNotExist:
        raise Http404("ERRO: Evento não existe ou já foi excluído!")







# class TarefasView(LoginRequiredMixin, TemplateView):
#     login_url = reverse_lazy('login')
    
#     template_name = 'home.html'
   
#     def get(self, *args):
#         context = {
#             'form':TarefasForm,
#             'editar': False,
#             'tarefas': Tarefa.objects.all().filter(usuario=self.request.user).order_by('-data_inclusao')
#         }
#         return render(self.request, self.template_name , context)
        
    
#     def post(self, *args):  
#         form = TarefasForm(self.request.POST)
        
#         if form.is_valid():
#             form.instance.usuario = self.request.user      
#             from django.utils import timezone
#             form.instance.data_inclusao = timezone.now()
#             nova_tarefa = form.save()

#             return JsonResponse({'tarefa': model_to_dict(nova_tarefa)}, status=200)
#         else:
        
#             return redirect('dashboard')
            
# class DeleteTarefaView(LoginRequiredMixin, DeleteView):
#     login_url = reverse_lazy('login')
    
#     model = Tarefa
#     success_url = reverse_lazy("dashboard") 
    
#     def get(self, request, *args, **kwargs): #Delete sem confirmação (Reescrever o GET())
#         return self.post(request, *args, **kwargs)

# class EditarTarefaView(LoginRequiredMixin, UpdateView):
#     login_url = reverse_lazy('login')
    
#     template_name = 'home.html'
#     model = Tarefa
#     success_url = reverse_lazy('dashboard')
#     form_class = TarefasForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tarefas'] =  Tarefa.objects.all().filter(usuario=self.request.user).order_by('-data_inclusao')
#         context['editar'] =  True
        
#         return context

    
   