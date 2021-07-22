from obras.models import *
from decimal import Decimal
from financeiro.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls.base import reverse_lazy
from django.views.generic.base import TemplateView
from django.db.models import Sum

# Create your views here.

class DashboardSimo(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name= 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # retorna o dados do select de centros de Custos
        context['obras_list'] = Obra.objects.all()
        
        # gera e retorna os dados do centro de custo escolhido
        if self.request.GET.get('centro_custo_sel'):
            obra_select = Obra.objects.get(pk=self.request.GET.get('centro_custo_sel'))
        else:
            obra_select = Obra.objects.first()
        context['obra_select'] = obra_select
        saidas_obra_select = Pagamento.objects.filter(conta__centro_de_custo=obra_select).aggregate(Sum('valor'))['valor__sum']
        entrada_obra_select = Recebimento.objects.filter(centro_de_custo=obra_select).aggregate(Sum('valor'))['valor__sum']
        
        if saidas_obra_select:
            context['saidas_obra_select'] =  real_br_money_mask(saidas_obra_select)
        else:
            saidas_obra_select = Decimal(0)
            context['saidas_obra_select'] =  real_br_money_mask(saidas_obra_select)
            
        if entrada_obra_select:          
            context['entrada_obra_select'] =  real_br_money_mask(entrada_obra_select)
        else:
            entrada_obra_select = Decimal(0)
            context['entrada_obra_select'] =  real_br_money_mask(entrada_obra_select)
            
        context['saldo_obra_select'] = real_br_money_mask(entrada_obra_select - saidas_obra_select)
        
        # retorna a soma do dia especifico
        saidas_dia = Pagamento.objects.filter(data=datetime.now().strftime("%Y-%m-%d")).aggregate(Sum('valor'))['valor__sum']
        entrada_dia = Recebimento.objects.filter(data=datetime.now().strftime("%Y-%m-%d")).aggregate(Sum('valor'))['valor__sum']
        
        if saidas_dia:
            context['saidas_dia'] =  real_br_money_mask(saidas_dia)
        else:
            saidas_dia = Decimal(0)
            context['saidas_dia'] =  real_br_money_mask(saidas_dia)
            
        if entrada_dia:          
            context['entrada_dia'] =  real_br_money_mask(entrada_dia)
        else:
            entrada_dia = Decimal(0)
            context['entrada_dia'] =  real_br_money_mask(entrada_dia)
            
        context['saldo_dia'] = real_br_money_mask(entrada_dia - saidas_dia)
        
        
        # retorna a soma de todos os dados
        saidas_geral = Pagamento.objects.all().aggregate(Sum('valor'))['valor__sum']
        entradas_geral = Recebimento.objects.all().aggregate(Sum('valor'))['valor__sum']
        
        if saidas_geral:
            context['saidas_geral'] =  real_br_money_mask(saidas_geral)
        else:
            saidas_geral = Decimal(0)
            context['saidas_geral'] =  real_br_money_mask(saidas_geral)
            
        if entradas_geral:
            
            context['entradas_geral'] =  real_br_money_mask(entradas_geral)
        else:
            entradas_geral = Decimal(0)
            context['entradas_geral'] =  real_br_money_mask(entradas_geral)
            
        context['saldo_geral'] = real_br_money_mask(entradas_geral - saidas_geral)
       
        return context
        
def real_br_money_mask(my_value):
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')