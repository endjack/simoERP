from django.core.cache import cache
from financeiro.filters import ContasFilter, ContasPagasFilter
from datetime import datetime, date
from django.views.generic.base import TemplateView
from servicos.views import bcolors
from financeiro.forms import *
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls.base import reverse, reverse_lazy
from .models import *
from django.db.models import Sum
from django.conf import settings
from django.template.loader import render_to_string
import os
from django.http.response import HttpResponse
from weasyprint import HTML, CSS
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin


class ContasAPagarView(GroupRequiredMixin, LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    template_name = 'financeiro/contas-a-pagar.html'
 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)      
        context["contas_list"] = ContaPagamento.objects.filter(pago=False)
        context["contas_list_pagas"] = Pagamento.objects.all()

        first_date = date(1, 1, 1)
        today_date = datetime.today()
       
        contas_do_dia = ContaPagamento.objects.filter(pago=False).filter(vencimento=today_date)
        contas_atrasadas = ContaPagamento.objects.filter(pago=False).filter(vencimento__range=[first_date, today_date])
        context["contas_do_dia"] = contas_do_dia
        context["contas_atrasadas"] = contas_atrasadas
        context["contas_do_dia_SUM"] = sum(contas_do_dia.values_list('valor', flat=True))
        context["contas_atrasadas_SUM"] = sum(contas_atrasadas.values_list('valor', flat=True))
        return context     

class ContasPagasView(GroupRequiredMixin, LoginRequiredMixin,TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    template_name = 'financeiro/contas-pagas.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        contas_pagas = Pagamento.objects.all()     
        context["contas_pagas_SUM"] = sum(contas_pagas.values_list('valor', flat=True))

        #filtros
        filter_list = ContasPagasFilter(self.request.GET, queryset= contas_pagas )    
        context["filter"] = filter_list 
        return context  

class InserirContasAPagarView(GroupRequiredMixin, LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    template_name = 'financeiro/inserir-conta.html'
    model = ContaPagamento
    form_class = ContaPagamentoForm
    success_url = reverse_lazy('contas-a-pagar')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contas_list"] = ContaPagamento.objects.filter(pago=False)
        context["contas_list_pagas"] = Pagamento.objects.all()
        return context
      
    def form_valid(self, form):      
        form.instance.usuario = self.request.user
        form.instance.valor = 0
        print(bcolors.OK + "VALORRRR - {}".format(self.request.POST.get('valor')) + bcolors.RESET) 
        form.instance.valor = float(form.cleaned_data['valor'])
        return super().form_valid(form)
      
class EditarContasAPagarView(GroupRequiredMixin, LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    template_name = 'financeiro/inserir-conta.html'
    model = ContaPagamento
    form_class = ContaPagamentoForm
    success_url = reverse_lazy('contas-a-pagar')
        
class ExcluirContasAPagarView(GroupRequiredMixin, LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    model = ContaPagamento
    success_url = reverse_lazy('contas-a-pagar')

class PagamentoView(GroupRequiredMixin, LoginRequiredMixin,CreateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    template_name = 'financeiro/pagamento.html'
    model = Pagamento
    form_class = PagamentoForm
    success_url = reverse_lazy('contas-a-pagar')

    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        conta_atual = ContaPagamento.objects.get(pk=self.kwargs.get('pk'))
         
        context["conta_atual"] = conta_atual
        return context
    
    def form_valid(self, form):
        conta_atual = ContaPagamento.objects.get(pk=self.kwargs.get('pk'))
        form.instance.conta = conta_atual
        form.instance.valor_original = conta_atual.valor
                
        if form.instance.valor_original <= form.instance.valor:  # o ckeckbox return 'on' ou None
            conta_atual.valor = form.instance.valor
            conta_atual.pago = True
            conta_atual.save()
        else:
            conta_atual.pago = False
            conta_atual.valor -= form.instance.valor 
            conta_atual.save()
                   
        return super().form_valid(form)

class EditarPagamentoView(GroupRequiredMixin, LoginRequiredMixin,UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    template_name = 'financeiro/pagamento.html'
    model = Pagamento
    form_class = PagamentoForm
    success_url = reverse_lazy('contas-a-pagar')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        pagamento_atual = Pagamento.objects.get(pk=self.kwargs.get('pk'))
        context['mostrar_conta'] = 'display: none;'
        
        if pagamento_atual.total:   
            context['checked'] = 'checked'
        
        return context
    
    def form_valid(self, form):
        pagamento_atual = Pagamento.objects.get(pk=self.kwargs.get('pk'))
        form.instance.valor_original = pagamento_atual.valor
        form.instance.conta = pagamento_atual.conta
                
        if form.instance.valor_original <= form.instance.valor:  # o ckeckbox return 'on' ou None
            conta_atual.valor = form.instance.valor
            pagamento_atual.conta.pago = True
            pagamento_atual.conta.save()
        else:
            pagamento_atual.conta.pago = False
            pagamento_atual.conta.valor -= form.instance.valor 
            pagamento_atual.conta.save()
                           
        return super().form_valid(form)

class ExcluirPagamentoView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    model = Pagamento
    success_url = reverse_lazy('contas-a-pagar')
    
    def delete(self, *args, **kwargs):
        # TODO conta do pagamento voltar para ser "à pagar"
        object = self.get_object()
        object.conta.pago = False
        object.conta.valor = object.valor_original
        object.conta.save()
        print(bcolors.WARNING + "CONTA EXCLUIDA - {}".format(object.conta.descricao) + bcolors.RESET)
        return super(ExcluirPagamentoView, self).delete(*args, **kwargs)

class RelatoriosCostasAPagarView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):  
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    template_name = 'financeiro/relatorios-contas-a-pagar.html'
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objects = ContaPagamento.objects.filter(pago=False)

        dados_form = self.request.GET
        cache.set('dados_form_contas_a_pagar', dados_form, 600)  
        
        filter_list = ContasFilter(dados_form, queryset= objects )
        cache.set('filter_contas_a_pagar', filter_list, 600)  

        valor_total = sum(filter_list.qs.values_list('valor', flat=True))
        cache.set('valor_total_contas_a_pagar', valor_total, 600) 

        context["valor_total"] = valor_total
        context["filter"] = filter_list

                
        if dados_form.get('fornecedor'):
            context["form_fornecedor"] = Fornecedor.objects.get(pk = dados_form.get('fornecedor'))
        else:
            context["form_fornecedor"] = 'Todos os Fornecedores'

        if dados_form.get('centro_de_custo'):
            context["form_centro_custo"] = Obra.objects.get(pk = dados_form.get('centro_de_custo'))
        else:
            context["form_centro_custo"] = 'Todos os Centros de Custo'
        
        if dados_form.get('data_inicial'):
            context["form_data_inicial"] = dados_form.get('data_inicial')
        
        if dados_form.get('data_final'):
            context["form_data_final"] = dados_form.get('data_final')
        return context       

class ImprimirRelatoriosCostasAPagarView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    template_name = 'financeiro/imprimir-contas-a-pagar.html'
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filter_list = cache.get('filter_contas_a_pagar')
        valor_total = cache.get('valor_total_contas_a_pagar')
        dados_form = cache.get('dados_form_contas_a_pagar') 
        
        context["filter"] = filter_list
        context["valor_total"] = valor_total
        
        
        if dados_form.get('fornecedor'):
            context["form_fornecedor"] = Fornecedor.objects.get(pk = dados_form.get('fornecedor'))
        else:
            context["form_fornecedor"] = 'Todos os Fornecedores'

        if dados_form.get('centro_de_custo'):
            context["form_centro_custo"] = Obra.objects.get(pk = dados_form.get('centro_de_custo'))
        else:
            context["form_centro_custo"] = 'Todos os Centros de Custo'
        
        if dados_form.get('data_inicial'):
            context["form_data_inicial"] = dados_form.get('data_inicial')
        
        if dados_form.get('data_final'):
            context["form_data_final"] = dados_form.get('data_final')
 
        return context



class ContasAReceberView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    template_name = 'financeiro/contas-a-receber.html'
    model = Recebimento
    form_class = RecebimentoForm
    success_url = reverse_lazy('contas-a-receber')
 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False      
        context["contas_a_receber_list"] = Recebimento.objects.all()
        return context   

class EditarRecebimentoView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    template_name = 'financeiro/contas-a-receber.html'
    model = Recebimento
    form_class = RecebimentoForm
    success_url = reverse_lazy('contas-a-receber')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        context["is_edit"] = True   
        return context

class ExcluirRecebimentoView(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    model = Recebimento
    success_url = reverse_lazy('contas-a-receber')

class GerarPDFContasView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Financeiro',]

    login_url = reverse_lazy('login')  
    contextPDF= {}
       
    def get(self, request):                 
        try:
            objects = ContaPagamento.objects.all()
            filter_list = ContasFilter(self.request.GET, queryset= objects )
            total = filter_list.qs.aggregate(Sum('valor'))['valor__sum']
            
            total = real_br_money_mask(total)
            
            if self.request.GET.get('dados_banco') == '2':
                self.contextPDF['dados_banco'] = True
            else:
                self.contextPDF['dados_banco'] = False
            self.contextPDF["filter"] = filter_list
            self.contextPDF['total'] = total
            self.contextPDF['usuario'] = self.request.user.get_username()
            
        except:
            context = {"modo_aba": "",}
            messages.warning(self.request, "ERRO: Não foi possível gerar o PDF")
            return render(request, 'financeiro/pdf-relatorio.html', context) 
        
            
        html = render_to_string("financeiro/pdf-relatorio.html", self.contextPDF)

    
        css_url = os.path.join(settings.PROJECT_ROOT, 'static\\css\\bootstrap.min.css')
        pdf = HTML(string=html,base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])

        return HttpResponse(pdf, content_type='application/pdf')
    
def real_br_money_mask(my_value):
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')