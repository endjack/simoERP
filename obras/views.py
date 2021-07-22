from obras.models import Obra
from django.urls.base import reverse_lazy
from django.views.generic.list import ListView
from obras.forms import *
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


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


class InserirLocalView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    template_name = 'obras/inserir-local.html'
    form_class = InserirLocalForm
    success_url = reverse_lazy('inserir-local')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["locais_list"] = Local.objects.all()
        return context
    

