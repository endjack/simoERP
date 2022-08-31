from django.core.files.base import ContentFile
from django.forms.models import model_to_dict
from django.http.response import JsonResponse
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tarefas.models import Tarefa
from tarefas.forms import TarefasForm
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def home_index(request):
    
    context = {
             'tarefas': Tarefa.objects.all().filter(usuario=request.user)
         }
    
    template_name = 'home.html'
    return render(request, template_name , context)

@csrf_exempt
def criar_tarefas(request):
    
    context = {
             'form': TarefasForm()
         }
    
    template_name = 'tarefas/fragmentos/modal-criar-tarefa.html'
    return render(request, template_name , context)

@csrf_exempt
def salvar_tarefa(request):
    form = TarefasForm(request.POST)
    criado = False
        
    if form.is_valid():
        form.instance.usuario = request.user      
        from django.utils import timezone
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

@csrf_exempt
def ver_tarefa(request, pk):
    tarefa = Tarefa.objects.get(pk=pk)
    template_name = 'tarefas/ver-tarefa.html'
    
    context = {
             'tarefa': tarefa,
             'tarefas': Tarefa.objects.all().filter(usuario=request.user),
         }
    return render(request, template_name , context)








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

    
   