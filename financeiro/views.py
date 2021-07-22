from financeiro.filters import ContasFilter
from django.views.generic.base import TemplateView
from servicos.views import bcolors
from financeiro.forms import *
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls.base import reverse, reverse_lazy
from .models import *
from django.db.models import Sum
# imports para Geração de PDF
from django.conf import settings
from django.template.loader import render_to_string
import os
from django.http.response import HttpResponse
from weasyprint import HTML, CSS
from django.contrib import messages


class CostasAPagarView(TemplateView):
    template_name = 'financeiro/contas-a-pagar.html'
 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)      
        context["contas_list"] = ContaPagamento.objects.filter(pago=False)
        context["contas_list_pagas"] = Pagamento.objects.all()
        return context     

class InserirCostasAPagarView(CreateView):
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
      
class EditarContasAPagarView(UpdateView):
    template_name = 'financeiro/inserir-conta.html'
    model = ContaPagamento
    form_class = ContaPagamentoForm
    success_url = reverse_lazy('contas-a-pagar')
        
class ExcluirContasAPagarView(DeleteView):
    model = ContaPagamento
    success_url = reverse_lazy('contas-a-pagar')

class PagamentoView(CreateView):
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
                
        if self.request.POST.get('total') != None :  # o ckeckbox return 'on' ou None
            form.instance.valor = conta_atual.valor
            conta_atual.pago = True
            conta_atual.save()
        else:
            conta_atual.pago = False
            conta_atual.valor -= form.instance.valor 
            conta_atual.save()
                   
        
        return super().form_valid(form)

class EditarPagamentoView(UpdateView):
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
                
        if self.request.POST.get('total') != None :  # o ckeckbox return 'on' ou None
            form.instance.valor = pagamento_atual.valor
            pagamento_atual.conta.pago = True
            pagamento_atual.conta.save()
        else:
            pagamento_atual.conta.pago = False
            pagamento_atual.conta.valor -= form.instance.valor 
            pagamento_atual.conta.save()
                           
        return super().form_valid(form)

class ExcluirPagamentoView(DeleteView):
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

class ResumosCostasAPagarView(TemplateView):     
    template_name = 'financeiro/contas-resumos.html'
     
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objects = ContaPagamento.objects.all()
        filter_list = ContasFilter(self.request.GET, queryset= objects )
        
        if self.request.GET.get('dados_banco') == '2':
            context['dados_banco'] = True
        else:
            context['dados_banco'] = False
        
        context["filter"] = filter_list
        context["contas_list"] = ContaPagamento.objects.filter(pago=False)
        context["contas_list_pagas"] = Pagamento.objects.all()
        return context       

class ContasAReceberView(CreateView):
    template_name = 'financeiro/contas-a-receber.html'
    model = Recebimento
    form_class = RecebimentoForm
    success_url = reverse_lazy('contas-a-receber')
 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False      
        context["contas_a_receber_list"] = Recebimento.objects.all()
        return context   

class EditarRecebimentoView(UpdateView):
    template_name = 'financeiro/contas-a-receber.html'
    model = Recebimento
    form_class = RecebimentoForm
    success_url = reverse_lazy('contas-a-receber')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)     
        context["is_edit"] = True   
        return context

class ExcluirRecebimentoView(DeleteView):
    model = Recebimento
    success_url = reverse_lazy('contas-a-receber')

class GerarPDFContasView(TemplateView):
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