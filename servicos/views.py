from clientes.models import Fiscal
from servicos.filters import ServicosFilter, ServicosFuncionarioFilter
from django.contrib import messages
from django.db import IntegrityError
from django.http.response import HttpResponseRedirect
from django.urls.base import reverse
from django.views.generic.edit import DeleteView, FormView, UpdateView
from django.views.generic.list import ListView
from servicos.models import Servico
from funcionarios.models import Funcionario
from django.shortcuts import get_object_or_404, render
from .forms import *
from django.urls  import reverse_lazy
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin
from django.core.cache import cache
import os




# Create your views here.
class bcolors:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

class OrdemServicoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']
    
    
    template_name = 'servicos/inserir-ordem.html'
    model = OrdemServico
    form_class = OrdemServicoForm

   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        context["lista_ordens"] = OrdemServico.objects.all()
           
        return context

    def get_form(self, *args, **kwargs): #//TODO ENVIAR QUERYSET POR TIPO DE USUARIO
        form= super().get_form(*args, **kwargs)
        if self.request.user.groups.filter(name='FiscalSESAD').exists():
            obra_atual = Obra.objects.filter(fiscal=1)
            obra_atual_ = Obra.objects.get(fiscal=1)
            form.fields['obra'].queryset= obra_atual
            form.fields['solicitante'].value = obra_atual_.fiscal.nome

        return form 
         
    def post(self, request, *args, **kwargs):
        # if request.method == "POST" and request.is_ajax():
        
        new_local = request.POST.get("new_local")
        if new_local:
            try:
                Local.objects.create(local=new_local)
                messages.add_message(
                        self.request, 
                        messages.SUCCESS,
                        'Local Adicionado!'
                    )    
            except IntegrityError:
                if 'unique constraint':
                    messages.add_message(
                        self.request, 
                        messages.WARNING,
                        f'Local: {request.POST.get("new_local")} Já Adicionado!'
                    )     
          
        
        return super().post(request, *args, **kwargs)
    
    def get_success_url(self):
        # if self.request.user.groups.filter(name='FiscalSESAD').exists():
        #     return reverse('salvar-ordem-servico', args=(self.object.id,))
        return reverse('inserir-servico', args=(self.object.id,))

class ServicoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']
        
    template_name = 'servicos/inserir-servico.html'
    model = Servico
    form_class = ServicoForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordem_atual = OrdemServico.objects.get(pk=self.kwargs.get('pk'))
        context["ordem_serv_atual"] = ordem_atual
        context['editar'] = False
        return context
    
    def form_valid(self, form):
        ordem_atual = OrdemServico.objects.get(pk=self.kwargs.get('pk'))
        form.instance.ordem = ordem_atual
        if form.instance.situacao != 'FINALIZADO':
            form.instance.finalizado = False
            form.instance.data_termino = None
        else:
            form.instance.finalizado = True
        print(form.instance.situacao)
        return super().form_valid(form)
    
    def get_success_url(self):
        ordem_atual = OrdemServico.objects.get(pk=self.kwargs.get('pk'))
        return reverse('inserir-funcionario-servico', kwargs={'id_ordem': ordem_atual.pk, 'pk':self.object.id})

class InserirFuncionarioServicoView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado']
    
    template_name = 'servicos/inserir-funcionario.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordem_atual = OrdemServico.objects.get(pk=self.kwargs.get('id_ordem'))
        servico_atual = Servico.objects.get(pk=self.kwargs.get('pk'))
        
        context["ordem_serv_atual"] = ordem_atual
        context["serv_atual"] = servico_atual
        context["form_funcionario"] = FuncionarioServicoForm
        context["form_fornecedor"] = FornecedorServicoForm
        
        
        #inserir Funcionários
        context["funcionarios_atual"] = FuncionarioServico.objects.filter(servico=servico_atual) 
        context["fornecedores_atual"] = FornecedorServico.objects.filter(servico=servico_atual)       
        
        return context   
    
    def post(self, request, **kwargs):
        servico_atual = Servico.objects.get(pk=kwargs.get('pk'))
        ordem_atual = OrdemServico.objects.get(pk=kwargs.get('id_ordem'))
        
        if 'addFuncionario' in request.POST:  
            form = FuncionarioServicoForm(request.POST)
            if form.is_valid():
                FuncionarioServico.objects.create(
                    servico = servico_atual,
                    funcionario = Funcionario.objects.get(pk=request.POST.get('funcionario'))
                )
        
        elif 'addFornecedor' in request.POST:  
            form = FornecedorServicoForm(request.POST)
            if form.is_valid():
                FornecedorServico.objects.create(
                    servico = servico_atual,
                    fornecedor = Fornecedor.objects.get(pk=request.POST.get('fornecedor'))
                )

        elif 'excluirFuncionario' in request.POST:         
                FuncionarioServico.objects.filter(pk=request.POST.get('excluirFuncionario')).delete()
                messages.add_message(
                    self.request, 
                    messages.ERROR,
                    'Funcionário Excluído!'
                ) 
        elif 'excluirFornecedor' in request.POST:         
                FornecedorServico.objects.filter(pk=request.POST.get('excluirFornecedor')).delete()
                messages.add_message(
                    self.request, 
                    messages.ERROR,
                    'Fornecedor Excluído!'
                )   
        return HttpResponseRedirect('/os/{}/{}/inserir-funcionario'.format(ordem_atual.pk, servico_atual.pk))
 
class ItensServicoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado']
    
    
    template_name = 'servicos/inserir-itens-servico.html'
    model = ItensServico
    form_class = ItemServicoForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordem_atual = OrdemServico.objects.get(pk=self.kwargs.get('id_ordem'))
        servico_atual = Servico.objects.get(pk=self.kwargs.get('pk'))
        funcionarios = FuncionarioServico.objects.filter(servico=servico_atual)
        itens_atuais = ItensServico.objects.filter(servico=servico_atual)
        context["ordem_serv_atual"] = ordem_atual     
        context["serv_atual"] = servico_atual
        context["itens_atuais"] = itens_atuais
               
        if funcionarios:
            ordem_atual.completo_funcionarios = True
            ordem_atual.save()
            context["funcionarios_atuais"] = funcionarios
            
            
        #excluir Item selecionado
        if 'excluirID' in self.request.GET:         
                ItensServico.objects.filter(id=self.request.GET.get('excluirID')).delete()
                messages.add_message(
                    self.request, 
                    messages.ERROR,
                    'Item Excluído!'
                )   
                            
        return context   
      
    def form_valid(self, form):
        servico_atual = Servico.objects.get(pk=self.kwargs.get('pk'))
        form.instance.servico = servico_atual 
        item = form.cleaned_data.get('item')
        qnt = form.cleaned_data.get('qnt')
        messages.add_message(
                    self.request, 
                    messages.SUCCESS,
                    f'{qnt} {item.unid_medida} {item.descricao} adicionado(s)'
                )   
        return super().form_valid(form)
       
    def get_success_url(self):
        ordem_atual = OrdemServico.objects.get(pk=self.kwargs.get('id_ordem'))
        servico_atual = Servico.objects.get(pk=self.kwargs.get('pk'))
        return reverse('inserir-itens-servico', kwargs = {'id_ordem': ordem_atual.pk, 'pk':servico_atual.pk})

class SalvarServicoView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']
    
    
    template_name = 'servicos/salvar-servico.html'
      
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_ordem = self.kwargs.get('pk')
        ordem_atual = OrdemServico.objects.get(pk=id_ordem)
        servico_atuais = Servico.objects.filter(ordem=ordem_atual)
    
                           
        context["ordem_serv_atual"] =  ordem_atual 
        context["serv_atuais"] = servico_atuais        
        return context 
                                                        
class FinalizarServicoView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado']
      
    template_name = 'servicos/finalizar-servico.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        servico_atual = Servico.objects.get(pk=kwargs.get('pk')) 
        context["serv_atual"] = servico_atual  
        
        return context
       
    def post(self, request, pk, id_ordem):
        context = {}
        servico_atual = Servico.objects.get(pk=self.kwargs.get('pk'))
        data_termino = self.request.POST.get('data_termino')
        if data_termino:
            servico_atual.finalizado = True
            servico_atual.situacao = 'FINALIZADO'
            servico_atual.data_termino= toDBFormat(data_termino)   
            servico_atual.obs = request.POST.get('obs') 
            servico_atual.save()
            context["finalizado"] = True
            context["data_termino"] = data_termino
                                            
        return HttpResponseRedirect('/salvar-ordem-servico/os/{}'.format(id_ordem))

class EditarServicoView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']
    
    model = Servico
    form_class = ServicoForm
    template_name = 'servicos/inserir-servico.html'  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordem_atual = OrdemServico.objects.get(pk=self.kwargs.get('id_ordem'))
        context["ordem_serv_atual"] =  ordem_atual
        context['editar'] = True
        return context
    
    def form_valid(self, form):
        if form.instance.situacao != 'FINALIZADO':
            form.instance.finalizado = False
            form.instance.data_termino = None
        else:
            form.instance.finalizado = True
        print(form.instance.situacao)
        return super().form_valid(form)
  
    def get_success_url(self):
        return reverse('salvar-ordem-servico', kwargs={'pk': self.kwargs.get('id_ordem')})
        
class ExcluirServicoView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):   
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']
    
        
    model = Servico
    template_name = 'servicos/excluir-servico-confirmar.html'
    
    def get_success_url(self):  
        return reverse('salvar-ordem-servico', kwargs={'pk': self.kwargs.get('id_ordem')})

class ExcluirOrdemDeServicoView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):   
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']
     
    model = OrdemServico
    success_url = reverse_lazy("listar-ordens")  

class DetalharServicoView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']

    template_name = 'servicos/detalhar-servico.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordem_atual = OrdemServico.objects.get(pk=self.kwargs.get('id_ordem'))
        servico_atual = Servico.objects.get(pk=self.kwargs.get('pk'))
        
        context["ordem_serv_atual"] = ordem_atual
        context["serv_atual"] = servico_atual    
        
        return context 

    def get_success_url(self):
        ordem_atual = OrdemServico.objects.get(pk=self.kwargs.get('id_ordem'))
        servico_atual = Servico.objects.get(pk=self.kwargs.get('pk'))
        return reverse('inserir-itens-servico', kwargs = {'id_ordem': ordem_atual.pk, 'pk':servico_atual.pk})

class ListServicosView(GroupRequiredMixin, LoginRequiredMixin, ListView):   
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']
    
    model = Servico
    template_name = "servicos/listar-servicos.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not 'descricao' in self.request.GET:
            objects = Servico.objects.filter(situacao="EM ANDAMENTO")
        else:
            objects = Servico.objects.all()

        filter_list = ServicosFilter(self.request.GET, queryset= objects )
        cache.set('filter', filter_list, 600)
        context["filter"] = filter_list  
  
   
        return context

class ListFuncionarioServicosView(GroupRequiredMixin, LoginRequiredMixin, ListView):   
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado']
      
    model = FuncionarioServico
    template_name = "servicos/listar-servicos-funcionario.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if not 'funcionario' in self.request.GET:
            objects = FuncionarioServico.objects.none()
        else:
            objects = FuncionarioServico.objects.all()
                   
        filter_list = ServicosFuncionarioFilter(self.request.GET, queryset= objects)
        cache.set('filter_funcionarios', filter_list, 600)
        context["filter"] = filter_list 

        return context

class ImprimirListaFuncionarioServicosView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado']

    template_name = 'servicos/imprimir-lista-servicos-funcionario.html'
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_list = cache.get('filter_funcionarios')
        
        context["filter"] = filter_list
        return context

class ImprimirServicoView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']

    template_name = 'servicos/imprimir-os-servico.html'
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ordem_atual = OrdemServico.objects.get(pk=self.kwargs.get('id_ordem'))
        servico_atual = Servico.objects.get(pk=self.kwargs.get('pk'))
        
        context["ordem_serv_atual"] = ordem_atual
        context["serv_atual"] = servico_atual    
        
        return context 
  
class ListOrdensView(GroupRequiredMixin, LoginRequiredMixin, ListView):   
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']
    
    
    model = OrdemServico
    template_name = "servicos/listar-ordens.html"
    context_object_name = 'lista_ordens'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # query = self.request.GET.get('local')
        
        # if query != None:
        #     context['lista_servicos_filtrados']  = Servico.objects.filter(ordem__local=query)
        #     context['label_filtro'] = 'Filtrando por Local: {}'.format(Local.objects.get(pk=query))
        # else:
        #   context['lista_servicos_filtrados']  = Servico.objects.all() 
        #   context['label_filtro'] = 'Todos os Serviços'
           
        # context['lista_ordens'] = OrdemServico.objects.all()
        # context['lista_servicos_finalizados'] = Servico.objects.filter(finalizado=True)
        # context['form']  =  FiltrarOrdem(self.request.POST or None)
        
        return context

class AnexarImagensServicoView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']
     
    template_name = 'servicos/anexar-imagens-servicos.html'
  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        servico_atual = Servico.objects.get(pk=kwargs.get('idServ')) 
        context["ordem_atual"] = OrdemServico.objects.get(pk=self.kwargs.get('pk'))
        context["serv_atual"] = servico_atual 
        
        fotos = FotosServico.objects.filter(servico =servico_atual)
        
        # print(f"------------------------------> {fotos}")
         
        try:
            for im in fotos:
                file_path = im.foto.url
                if os.path.exists(file_path):
                    print("----------------->Existe")
                else:
                    print("_________________>NÃO EXISTE")
        except FileNotFoundError:
            print("IMAGEM NÃO ENCONTRADA")
            fotos = None
                    
                        
        context["fotos_serv_atual"] = fotos   
        return context
       
    
    def post(self, request, pk, idServ):
        servico_atual = Servico.objects.get(pk=self.kwargs.get('idServ')) 
        files = request.FILES.getlist('files')
    
        for img in files:
            a = FotosServico.objects.create(servico=servico_atual, foto=img)
        
        return HttpResponseRedirect('/anexar-imagens-servicos/os/{}/servico/{}'.format(pk, idServ))
        #return reverse('anexar-imagens-servicos', kwargs={'pk': pk, 'idServ:': idServ})

class DeletarImagemServicoView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']
    
    
    model = FotosServico
              
    def get_success_url(self):      
        return reverse('anexar-imagens-servicos', kwargs = {'pk': self.kwargs.get('id_ordem'), 'idServ':self.kwargs.get('idServ')})

class ImprimirListaServicosView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Engenharia', u'Encarregado', u'FiscalSESAD']

    template_name = 'servicos/imprimir-servicos.html'
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_list = cache.get('filter')
        
        context["filter"] = filter_list
        return context



def toDBFormat(dateString):
    dataBD = dateString.split('/')
    return str(dataBD[2])+'-'+str(dataBD[1])+'-'+str(dataBD[0])

