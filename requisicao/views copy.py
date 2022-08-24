from django.views.generic.list import ListView
from estoque.filters import EstoqueFilter
from estoque.models import *
from .models import *
from django.http.response import HttpResponse
from requisicao.forms import GerarRequisicaoForm
from django.urls.base import reverse, reverse_lazy
from requisicao.models import ItemRequisicao, Requisicao
from django.shortcuts import render
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import CreateView
from weasyprint import HTML, CSS
from django.db.models import Q
import os
from django.contrib import messages
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

estoque_add = []

class GerarRequisicaoView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Requisicao
    template_name = 'requisicao/gerar-requisicao.html'
    form_class = GerarRequisicaoForm

    def get_success_url(self):
        return reverse('inserir-item-requisicao', args=(self.object.id,))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
           
        context['objects_by'] =  Requisicao.objects.order_by('pk').all()  #TODO filtrar pelos últimos ou por data
        return context

class InserirItensView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'requisicao/inserir-itens-requisicao.html'

class InserirRequisicaoView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'requisicao/inserir-item-requisicao.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["obj"] =  Requisicao.objects.filter(pk=self.kwargs.get('pk'))
        context["numId"] = self.kwargs.get('pk')
        objects = Estoque.objects.all()

        filter_list = EstoqueFilter(self.request.GET, queryset = objects )
        context["filter"] = filter_list 
        return context 


    def post(self, request, *args, **kwargs):
        requisicao_atual = Requisicao.objects.get(pk=self.kwargs.get('pk'))
        if 'addReq' in self.request.POST:
            global contextPDF

            contextPDF = {
                "reqID": self.kwargs.get('pk'),
                "list_itens": estoque_add,
                "req_solicitante": requisicao_atual.solicitante,
                "req_obra": requisicao_atual.obra,
                "req_local": requisicao_atual.local,
                "req_almoxarife": requisicao_atual.almoxarife,
                "modo_aba": "_blank"
            }

            #salvando ItensRequisicao no Banco
            for elemento in estoque_add:
                item_req = ItemRequisicao.objects.create(requisicao=requisicao_atual, quantidade=elemento[3])
                item_req.item.add(Item.objects.get(pk = elemento[0]))
                item_req.save()
                
            return render(request, 'requisicao/detalhar-requisicao.html', contextPDF)
                
class DetalharRequisicaoView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'requisicao/detalhar-requisicao.html'
  
class ListarRequisicoesView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    template_name = 'requisicao/listar-requisicoes.html'
    queryset = Requisicao.objects.all()
    context_object_name = 'objects_by'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    

        # #buscar requisição
        # query = self.request.GET.get('q')
        # query2 = self.request.GET.get('q2')
        # query3 = self.request.GET.get('q3')
        
        # if query != "" and query2 == "":
        #    if query != None: 
        #         objects_by_data = Requisicao.objects.filter(Q(data__icontains=query))
        #         context["objects_by"] = objects_by_data
        #         print("-----------------------------ENTREI query     " + str(objects_by_data))

        # elif query2 != '' and query == "":
        #     if query2 != None:
        #         objects_by_solicitante = Requisicao.objects.filter(Q(solicitante__icontains=query2))
        #         context["objects_by"] = objects_by_solicitante
        #         print("-----------------------------ENTREI query2    " + str(objects_by_solicitante))

        # elif query3 != "" and query2 == "" and query == "":
        #     if query3 != None:
        #         objects_ = ItemRequisicao.objects.filter(Q(item__descricao__icontains=query3))
        #         print("-----------------------------ENTREI query3    " + str(objects_))
        #         objects_by_item = ""
        #         for item in objects_:
        #             objects_by_item = Requisicao.objects.filter(pk=item.requisicao.pk)   


        #         context["objects_by"] = objects_by_item
        #         print("-----------------------------ENTREI query3    " + str(objects_by_item))

        # elif query != "" and query2 != "" and query3 != "":
        #     if query != None and query2 != None and query3 != None:
        #         objects_by_all = Requisicao.objects.filter(Q(data__icontains=query), Q(solicitante__icontains=query2))
        #         context["objects_by"] = objects_by_all 
        #         print("-----------------------------ENTREI" + str(objects_by_all )) 
        # else:
        #     pass


        return context

class DetalharItensDeRequisicaoView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'requisicao/detalhar-itens.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_req = self.kwargs.get('pk')
        requisicao_atual = Requisicao.objects.get(pk=id_req)
        objects_req = ItemRequisicao.objects.filter(Q(requisicao__pk=id_req))
        itens_req = objects_req.values_list('item__pk','item__descricao','item__unid_medida')

        zip_list_itens = zip(objects_req,itens_req)
        
           
        context['reqID'] =id_req
        context['req_solicitante'] = requisicao_atual.solicitante
        context['req_obra'] = requisicao_atual.obra
        context['req_local'] = requisicao_atual.local
        context['req_almoxarife'] = requisicao_atual.almoxarife
        context['req_data'] = requisicao_atual.data
        context['objects_itens'] = zip_list_itens

        
        context['size_list'] = len(objects_req)

        return context

class BuscaRequisicaoView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = 'requisicao/buscar-requisicao.html'

class GerarPdfRequisicao(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')  
    def get(self, request, *args, **kwargs):             
        #template  = get_template('requisicao/detalhar-requisicao.html')        
        try:
            print(contextPDF)
        except:
            context = {"modo_aba": "",}
            messages.warning(self.request, "ERRO: Não foi possível gerar o PDF")
            return render(request, 'requisicao/detalhar-requisicao.html', context) 
        
        html = render_to_string("requisicao/gerar-pdf-requisicao.html", contextPDF)
    
        css_url = os.path.join(settings.PROJECT_ROOT, 'static\\css\\bootstrap.min.css')
        pdf = HTML(string=html,base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(css_url)])

        return HttpResponse(pdf, content_type='application/pdf')

