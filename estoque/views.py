from estoque.filters import EstoqueFilter
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.urls.base import reverse
from django.views.generic.edit import DeleteView, UpdateView
from django.views.generic.list import ListView
import pyqrcode
from abc import abstractmethod
from estoque.models import Estoque
from estoque.forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView


# INSERE ITENS NO SISTEMA E NÃO NO ESTOQUE
class InserirItemView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    selected_categoria ='0'
    
    model = Item
    template_name = 'estoque/inserir-item.html'
    success_url = reverse_lazy('inserir-item')
    form_class = InserirItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itensEstoque'] =  Item.objects.order_by('pk').all()   
        context['inserir'] =  True
        context['selected_categoria'] =  self.selected_categoria
        return context

    def form_valid(self, form): 
        f = super().form_valid(form)
             
        # GERANDO O QR CODE
        qr_code = gerar_qrcode(f"#ID#{self.object.pk}")
        self.object.qr_code = f'{qr_code}'
        
        self.object.save()
        messages.add_message(
            self.request, 
            messages.SUCCESS,
            'ITEM  adicionado com SUCESSO!'
        )
        return f

    def post(self, request, *args, **kwargs):
        new_categoria = request.POST.get("new_categoria")
        if new_categoria:
            try:
                categoria = Categoria.objects.create(categoria=new_categoria)
                self.selected_categoria = categoria.pk
                messages.add_message(
                        self.request, 
                        messages.SUCCESS,
                        'Categoria Adicionada!'
                    )    
            except IntegrityError:
                if 'unique constraint':
                    messages.add_message(
                        self.request, 
                        messages.WARNING,
                        f'CATEGORIA: {request.POST.get("new_categoria")} Já Adicionada!'
                    )     
          
        
        return super().post(request, *args, **kwargs)

# DETALHA OS DADOS DO ITEM INDIVIDUALMENTE
class DetalharItemView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "estoque/detalhar-item.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)         
        context["item_atual"] = Item.objects.get(pk=self.kwargs.get('pk'))
        return context

# EDITA OS ITENS NO MESMO TEMPLATE DE CRIAÇÃO
class EditarItemView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    
    template_name = 'estoque/inserir-item.html'
    model = Item
    form_class = InserirItemForm
        
    def get_success_url(self):
        return reverse('detalhar-item', kwargs = {'pk': self.kwargs.get('pk')})
    
# EXCLUI ITEM DO ESTOQUE
class ExcluirItemView(LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('login')
    
    model = Item
    success_url = reverse_lazy("inserir-item")

#         
class InicioEstoque(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    
    model = Estoque
    template_name= 'estoque/ver-estoque.html'
    success_url = reverse_lazy('ver-estoque')
    form_class = EstoqueModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        objects = Estoque.objects.select_related('item') 
        filter_list = EstoqueFilter(self.request.GET, queryset = objects )
        context["filter"] = filter_list
        # context["contas_list"] = Estoque.objects.filter()
        
        return context

#
class MovimentacaoEstoqueView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = MovimentacaoEstoque
    template_name= 'estoque/mov-estoque.html'
    success_url = reverse_lazy('mov-estoque')
    form_class = MovimentacaoModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itensEstoque'] =  Estoque.objects.order_by('pk').all()   
        return context


    def form_valid(self, form): 
        response = super().form_valid(form)
        tipo = form.cleaned_data['tipo']
        
        #preenchendo Estoque
        estoque = Estoque()
        item_form = self.request.POST.get('item_selecionado')
        
        # Verificando se existe o COD: ou o item é valido!
        try:
            item_id = item_form.split('COD: ')[1] #fatia a string, deixando apenas a matricula
        except IndexError:
            messages.add_message(
                    self.request, 
                    messages.WARNING,
                    'Vazio ou Não existe!!'
                )    
        else:
            item_atual = Item.objects.get(pk=item_id)
            print('--------------------'+(str(item_atual)))
            estoque.quantidade = form.cleaned_data['qtd']
            
            # Verificando se a quantidade é somente positiva e maior que zero
            if(estoque.quantidade <= 0):
                 messages.add_message(
                    self.request, 
                    messages.WARNING,
                    'Valor Negativo ou Zerado - Favor inserir outro valor!'
                )  
            else:
                estoque.item = item_atual
                #verificando se é Entrada ou Saída
                if tipo == '1': #Caso seja Entrada
                    if not Estoque.objects.filter(item= item_atual).exists():
                        estoque.save()
                        print('Nome Item no Estoque: '+ estoque.item.descricao)
                    else: 
                        #somar quantidade
                        qnt_anterior = Estoque.objects.get(item= item_atual).quantidade
                        soma = quantidade=estoque.quantidade+qnt_anterior
                        Estoque.objects.filter(item= item_atual).update(quantidade=soma)
                        #print('Item atualizado: ENTRADA -'+ str(estoque.quantidade) +' itens: '+ estoque.item.descricao)   

                        messages.add_message(
                            self.request, 
                            messages.SUCCESS,
                            str(estoque.quantidade)+' '+str(estoque.item.unid_medida)+' - '+str(estoque.item.descricao)+' foi ACRESCENTADO ao Estoque - Total no Estoque: '+str(soma)
                        )
                else: #caso seja Saída
                    if not Estoque.objects.filter(item= item_atual).exists():
                        messages.add_message(
                            self.request, 
                            messages.WARNING,
                            'Item: '+str(item_atual)+' NÃO ENCONTRADO!'
                        )
                    else:
                        #diminuir quantidade
                        qnt_anterior = Estoque.objects.get(item= item_atual).quantidade
                        sobra = qnt_anterior-estoque.quantidade
                        if sobra >= 0:
                            Estoque.objects.filter(item= item_atual).update(quantidade=sobra)
                            messages.add_message(
                                self.request, 
                                messages.WARNING,
                                str(estoque.quantidade)+' '+str(estoque.item.unid_medida)+' - '+str(estoque.item.descricao)+' foi RETIRADO ao Estoque - Total no Estoque: '+str(sobra)
                            )
                        else:        
                            messages.add_message(
                                self.request, 
                                messages.WARNING,
                                'NÃO HÁ ITENS SUFICIENTES NO ESTOQUE!'
                            )
        
        return response

#   
class CategoriasEstoque(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Categoria
    template_name= 'estoque/categorias-estoque.html'
    success_url = reverse_lazy('categorias-estoque')
    form_class = CategoriaModelForm

    def get_context_data(self, **kwargs):
        context = super(CategoriasEstoque, self).get_context_data(**kwargs)
        context['categorias'] =  Categoria.objects.order_by('pk').all() 
        return context

#
class BuscaEstoqueView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Estoque
    template_name = 'estoque/buscar-estoque.html'

    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = ''
        if query != None:
            object_list = Estoque.objects.filter(Q(item__descricao__icontains=query))
        return  object_list

#
def autocompleteitens(request):
    query = request.GET.get('term')
    query_set = Item.objects.filter(descricao__icontains=query)
    myList=[]
    myList += [x.descricao+' - '+x.unid_medida+' - COD: '+str(x.pk) for x in query_set]
    return JsonResponse(myList,safe=False)    

#
def gerar_qrcode(text):  
    code = pyqrcode.create(text)
    code.png(f"simo/media/qrcodes/{text}.png", scale=6,)

    if code != 0:
        print(f"QRCode gerado com sucesso - {text}!")
        return f"qrcodes/{text}.png"
    else:
        print(f"ERRO ao gerar QRCode - {text}!")
        return False
    

        
    