from django.urls.base import reverse_lazy
from fornecedores.forms import FornecedorForm
from financeiro.models import Pagamento
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from django.views.generic.edit import DeleteView, UpdateView
from .models import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class ListarFornecedorView(TemplateView):
    template_name = "fornecedores/lista-fornecedores.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["list_fornecedores"] = Fornecedor.objects.all()
        return context
    
class DetalharFornecedorView(TemplateView):
    template_name = "fornecedores/fornecedor.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fornecedor_atual = Fornecedor.objects.get(pk=self.kwargs.get('pk'))
        context["fornecedor"] = fornecedor_atual
        context["contas_list_pagas"] = Pagamento.objects.filter(conta__fornecedor=fornecedor_atual)
        
        return context

class InserirFornecedorView(CreateView):
    template_name = "fornecedores/incluir-fornecedor.html"
    model = Fornecedor
    form_class = FornecedorForm
    success_url = reverse_lazy('listar-fornecedores')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['titulo'] = 'Inserir Novo Fornecedor'
        
        return context
       
    
    def form_valid(self, form):               
        if self.request.POST.get('faz_nota') != None :  # o ckeckbox return 'on' ou None
            form.instance.faz_nota = True                        
        return super().form_valid(form)
              
class EditarFornecedorView(UpdateView):
    template_name = "fornecedores/incluir-fornecedor.html"
    model = Fornecedor
    form_class = FornecedorForm
    success_url = reverse_lazy('listar-fornecedores')
    fornecedor_atual = None
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        EditarFornecedorView.fornecedor_atual = Fornecedor.objects.get(pk=self.kwargs.get('pk'))
        context['titulo'] = 'Editar Fornecedor - {}'.format(EditarFornecedorView.fornecedor_atual.nome)
        
        if EditarFornecedorView.fornecedor_atual.faz_nota:   
            context['checked'] = 'checked'
        
        return context
    
    def form_valid(self, form):               
        if self.request.POST.get('faz_nota') != None :  # o ckeckbox return 'on' ou None
            form.instance.faz_nota = True                        
        return super().form_valid(form)
    
class ExcluirFornecedorView(DeleteView):
    model = Fornecedor
    success_url = reverse_lazy('listar-fornecedores')
    

