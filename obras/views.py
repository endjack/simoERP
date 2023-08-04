from obras.models import Obra
from django.urls.base import reverse_lazy
from django.views.generic.list import ListView
from obras.forms import *
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse



# Create your views here.

class InserirObraView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = 'obras/inserir-obra.html'
    form_class = InserirObraForm
    success_url = reverse_lazy('inserir-obra')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obras_list"] = Obra.objects.all()
        return context


class BuscarObraListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Obra
    template_name = 'obras/ver-obras.html'

    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = ''
        if query != None:
            object_list = Obra.objects.filter(Q(nome__icontains=query))
        return  object_list


def inserir_local(request, template_name ='obras/inserir-local.html'):
    
    locais = Local.objects.all().order_by('local')
    
    if request.method == 'POST':
        local = request.POST.get('local') or ''
        endereco = request.POST.get('endereco') or ''

               
        Local.objects.create(local=local, endereco = endereco)
        locais = Local.objects.all().order_by('local')
        
        
                
    context = {
       'locais': locais
    }
    
    return render(request, template_name , context)

def editar_local(request, pk, template_name ='obras/inserir-local.html'):
    

    if request.method == 'POST':
        local = request.POST.get('local') or ''
        endereco = request.POST.get('endereco') or ''


        local_atual = Local.objects.get(pk=pk)
        local_atual.local = local
        local_atual.endereco = endereco
        local_atual.save()
        
        locais = Local.objects.all().order_by('local')
               
        context = {
        'locais': locais
        }
        
        return render(request, template_name , context)

def excluir_local(request, pk, template_name ='obras/inserir-local.html'):
    
    
    if request.method == 'GET':
        local_atual = Local.objects.get(pk=pk)
        local_atual.delete()
 
    
    locais = Local.objects.all().order_by('local')     
                
    context = {
       'locais': locais
    }
    
    return render(request, template_name , context)

def get_locais(request, template_name ='engenharia/fragmentos/endereco_input_fragment.html'):
    
    local_selecionado = request.GET.get('local')

    local = Local.objects.get(pk=int(local_selecionado))  
                
    context = {
       'local': local
    }
    
    return render(request, template_name , context)


