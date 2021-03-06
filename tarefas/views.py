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

class TarefasView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    
    template_name = 'home.html'
   
    def get(self, *args):
        context = {
            'form':TarefasForm,
            'editar': False,
            'tarefas': Tarefa.objects.all().filter(usuario=self.request.user).order_by('-data_inclusao')
        }
        return render(self.request, self.template_name , context)
        
    
    def post(self, *args):  
        form = TarefasForm(self.request.POST)
        
        if form.is_valid():
            form.instance.usuario = self.request.user      
            from django.utils import timezone
            form.instance.data_inclusao = timezone.now()
            nova_tarefa = form.save()

            return JsonResponse({'tarefa': model_to_dict(nova_tarefa)}, status=200)
        else:
        
            return redirect('dashboard')
            
class DeleteTarefaView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    
    model = Tarefa
    success_url = reverse_lazy("dashboard") 
    
    def get(self, request, *args, **kwargs): #Delete sem confirmação (Reescrever o GET())
        return self.post(request, *args, **kwargs)

class EditarTarefaView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    
    template_name = 'home.html'
    model = Tarefa
    success_url = reverse_lazy('dashboard')
    form_class = TarefasForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tarefas'] =  Tarefa.objects.all().filter(usuario=self.request.user).order_by('-data_inclusao')
        context['editar'] =  True
        
        return context

    
   