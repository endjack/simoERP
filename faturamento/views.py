from django.db.models.aggregates import Sum
from faturamento.filters import FaturamentoFilter
from django.views.generic.base import TemplateView
from faturamento.models import *
from faturamento.forms import *
from django.shortcuts import render
from django.urls.base import reverse, reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.core.cache import cache

# Create your views here.
class FaturamentoView(TemplateView):
    template_name = 'faturamento/listar-faturamentos.html'
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 

        if self.request.GET.get('obra'):
            obra = self.request.GET.get('obra')
            cache.set('obra_faturamento', obra, 600)

        faturamentos = Faturamento.objects.all()     
        context["faturamento_list"] = faturamentos
        filter_list = FaturamentoFilter(self.request.GET, queryset= faturamentos )
        cache.set('filter_faturamento', filter_list, 600)
        
        context["filter"] = filter_list

        valor_total = sum(filter_list.qs.values_list('valor', flat=True))
        valor_saldo = sum(filter_list.qs.values_list('saldo', flat=True))

        cache.set('valor_total', valor_total, 600)
        cache.set('valor_pago', valor_total - valor_saldo, 600)
        cache.set('saldo_faturamento', valor_saldo, 600)

        context["valor_total"] = valor_total
        context["valor_pago"] = valor_total - valor_saldo
        context["saldo_faturamento"] = valor_saldo

        return context     

class InserirFaturamentoView(CreateView):
    template_name = 'faturamento/inserir-faturamento.html'
    model = Faturamento
    form_class = FaturamentoForm
    success_url = reverse_lazy('listar-faturamentos')
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class EditarFaturamentoView(UpdateView):
    template_name = 'faturamento/inserir-faturamento.html'
    model = Faturamento
    form_class = FaturamentoForm
    success_url = reverse_lazy('listar-faturamentos')

class ExcluirFaturamentoView(DeleteView):
    model = Faturamento
    success_url = reverse_lazy('listar-faturamentos')


class ImprimirFaturamentoView(TemplateView):
    template_name = 'faturamento/imprimir-faturamento.html'
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["filter"] = cache.get('filter_faturamento')
        if cache.get('obra_faturamento'):    
            context["obra_faturamento"] = Obra.objects.get(pk=cache.get('obra_faturamento'))      
        context["valor_total"] = cache.get('valor_total')
        context["valor_pago"] = cache.get('valor_pago')
        context["saldo_faturamento"] = cache.get('saldo_faturamento')
        return context 