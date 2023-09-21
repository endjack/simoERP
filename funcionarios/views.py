from django.http import HttpResponse
from django.views.generic.base import TemplateView
from funcionarios.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import JsonResponse
from django.urls.base import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from funcionarios.models import *
from django.shortcuts import render


def procurar_pessoal(request, template_name="funcionarios/fragmentos/procurar/procurar_home.html"):
    if request.method == 'GET':
        menu_ativo = 'PROCURAR'
        
        context = {
            'menu_ativo' : menu_ativo
        }
        return render(request, template_name, context)


def cadastrar_funcionarios_pessoal(request, template_name= 'funcionarios/fragmentos/funcionarios/funcionarios_home.html'):
    if request.method == 'GET':
        menu_ativo = 'CADASTRARFUNCIONARIOS'
        tipo_contrato = FuncionarioV2.Contratos
        tipo_demissao = FuncionarioV2.TipoDemissao
        tipo_conta = FuncionarioV2.TipoConta
        tipo_pix = FuncionarioV2.TipoPix
        situacao = FuncionarioV2.Situacao
        cargos = Cargo.objects.all()
        obras = Obra.objects.all()
        bancos = Banco.objects.all()
        responsavel_direto = ResponsávelObraFuncionariov2.objects.all()
        start_inputs_dependents = 1
        
        context = {
            'menu_ativo' : menu_ativo,
            'tipo_contrato' : tipo_contrato,
            'tipo_demissao' : tipo_demissao,
            'tipo_conta' : tipo_conta,
            'tipo_pix' : tipo_pix,
            'situacao' : situacao,
            'cargos' : cargos,
            'obras' : obras,
            'bancos' : bancos,
            'responsavel_direto' : responsavel_direto,
            'start_inputs_dependents' : start_inputs_dependents,
        }
        return render(request, template_name, context)



def cadastrar_cargo_pessoal(request, template_name= 'funcionarios/fragmentos/cargos/cargos_home.html'):
    if request.method == 'GET':
        menu_ativo = 'CADASTRARCARGOS'
    
        context = {
            'menu_ativo' : menu_ativo
        }
        return render(request, template_name, context)


def impressoes_pessoal(request, template_name= 'funcionarios/fragmentos/impressoes/impressoes_home.html'):
    if request.method == 'GET':
        menu_ativo = 'IMPRESSÃO'
   
        context = {
            'menu_ativo' : menu_ativo
        }
        return render(request, template_name, context)


def relatorios_pessoal(request, template_name= 'funcionarios/fragmentos/relatorios/relatorios_home.html'):
    if request.method == 'GET':
        menu_ativo = 'RELATÓRIO'
    
        context = {
            'menu_ativo' : menu_ativo
        }
        return render(request, template_name, context)
    
    
def add_inputs_dependente(request, id, template_name= 'funcionarios/fragmentos/funcionarios/novo_dependente.html'):
    if request.method == 'GET':
        context = {
            'start_inputs_dependents' : id+1,
            'anterior_inputs' : id
        }
        return render(request, template_name, context)
    
def clear_element(request):
        return HttpResponse('')







































#---------------------------------------------------------ANTIGO-----------------------------------------------#

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