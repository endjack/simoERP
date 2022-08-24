from django.views.generic.base import TemplateView
from funcionarios.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from funcionarios.models import *
from django.shortcuts import render


# FUNCIONÁRIOS.
class InserirFuncionarioView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    
    template_name = 'funcionarios/inserir-funcionario.html'
    model = Funcionario
    form_class = InserirFuncionarioForm
    success_url = reverse_lazy('inserir-funcionario')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["funcionarios_list"] = Funcionario.objects.all()
        context["editar"] = False
        return context

class EditarFuncionarioView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')

    template_name = 'funcionarios/inserir-funcionario.html'
    model = Funcionario
    form_class = InserirFuncionarioForm
    success_url = reverse_lazy('inserir-funcionario')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editar"] = True
        return context

class ExcluirFuncionarioView(DeleteView): 
    login_url = reverse_lazy('login')

    model = Funcionario
    success_url = reverse_lazy('inserir-funcionario')


class DetalharFuncionarioView(TemplateView):
    pass


#CARGOS
class InserirCargoView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    
    template_name = 'funcionarios/inserir-cargo.html'
    model = Cargo
    form_class = InserirCargoForm
    success_url = reverse_lazy('inserir-cargo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cargos_list"] = Cargo.objects.all()
        context["editar"] = False
        return context

class EditarCargoView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')

    template_name = 'funcionarios/inserir-cargo.html'
    model = Cargo
    form_class = InserirCargoForm
    success_url = reverse_lazy('inserir-cargo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editar"] = True
        return context

class ExcluirCargoView(DeleteView): 
    login_url = reverse_lazy('login')

    model = Cargo
    success_url = reverse_lazy('inserir-cargo')


class DetalharCargoView(TemplateView):
    pass




def autocompletefuncionario(request):
    query = request.GET.get('term')
    query_set = Funcionario.objects.filter(nome__icontains=query)
    myList=[]
    myList += [x.nome+' - COD: '+x.matricula for x in query_set]
    return JsonResponse(myList,safe=False)