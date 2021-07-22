from django.views.generic.base import TemplateView
from recibos.models import ReciboFornecedor
from django.shortcuts import render
from .forms import *
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls.base import reverse, reverse_lazy
# imports para Geração de PDF
from django.conf import settings
from django.template.loader import render_to_string
import os
from django.http.response import HttpResponse
from weasyprint import HTML, CSS
from num2words import num2words

# Create your views here.


class InserirReciboFornecedorView(CreateView):
    template_name = 'financeiro/inserir-recibo.html'
    model = ReciboFornecedor
    form_class = ReciboForm
    success_url = reverse_lazy('inserir-recibo')
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recibos_list"] = ReciboFornecedor.objects.all()
        context["editar"] = False
        return context

class EditarReciboFornecedorView(UpdateView):
    template_name = 'financeiro/inserir-recibo.html'
    model = ReciboFornecedor
    form_class = ReciboForm
    success_url = reverse_lazy('inserir-recibo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["editar"] = True
        return context

class ExcluirReciboFornecedorView(DeleteView): 
    model = ReciboFornecedor
    template_name = 'financeiro/recibofornecedor_confirm_delete.html'
    success_url = reverse_lazy('inserir-recibo')

class ImprimirReciboFornecedorView(TemplateView):
    template_name = 'financeiro/pdf-recibo.html'
       
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recibo_atual = ReciboFornecedor.objects.get(pk=kwargs.get('pk'))
        context["recibo_atual"] = recibo_atual
        context["usuario_atual"] = self.request.user
        context["data_atual"] = data_de_hoje_por_extenso_pt_BR(recibo_atual.data)
        context["por_extenso"] = number_to_long_number(real_br_money_mask(recibo_atual.valor))
        return context
   

# class PDFReciboFornecedorView(TemplateView):
#     login_url = reverse_lazy('login')  
#     contextPDF= {}
       
#     def get(self, request, pk):                 
#         try:
#             recibo_atual = ReciboFornecedor.objects.get(pk=pk)

#             self.contextPDF["recibo_atual"] = recibo_atual
#             self.contextPDF["usuario_atual"] = request.user
#             self.contextPDF["data_atual"] = data_de_hoje_por_extenso_pt_BR(recibo_atual.data)
#             self.contextPDF["por_extenso"] = number_to_long_number(real_br_money_mask(recibo_atual.valor))
#             # self.contextPDF["por_extenso"] = number_to_long_number(recibo_atual.valor)
            
#         except:
#             context = {"modo_aba": "",}
#             return render(request, 'financeiro/inserir-recibo.html', context) 
           
#         html = render_to_string("financeiro/pdf-recibo.html", self.contextPDF)

    
#         css_url = os.path.join(settings.PROJECT_ROOT, 'static\\css\\bootstrap.min.css')
#         pdf = HTML(string=html,base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)], presentational_hints=True)

#         return HttpResponse(pdf, content_type='application/pdf')

def data_de_hoje_por_extenso_pt_BR(data):
    from datetime import datetime
    import locale
    locale.setlocale(locale.LC_TIME, "pt_BR.UTF-8")
    return datetime.strftime(data,"%A, %d de %B de %Y")
    
def real_br_money_mask(my_value):
    a = '{:,.2f}'.format(float(my_value))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')

def number_to_long_number(number_p):
    if number_p.find(',')!=-1:
        number_p = number_p.split(',')
        number_p1 = int(number_p[0].replace('.',''))
        number_p2 = int(number_p[1])
    else:
        number_p1 = int(number_p.replace('.',''))
        number_p2 = 0    

    if number_p1 == 1:
        aux1 = ' real'
    else:
        aux1 = ' reais'

    if number_p2 == 1:
        aux2 = ' centavo'
    else:
        aux2 = ' centavos'

    text1 = ''
    if number_p1 > 0:
        text1 = num2words(number_p1,lang='pt_BR') + str(aux1)
    else:
        text1 = ''

    if number_p2 > 0:
        text2 = num2words(number_p2,lang='pt_BR') + str(aux2) 
    else: 
        text2 = ''

    if (number_p1 > 0 and number_p2 > 0):
        result = text1 + ' e ' + text2
    else:
        result = text1 + text2

    return result