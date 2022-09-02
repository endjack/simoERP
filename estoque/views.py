from cgitb import text
from urllib import request
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.cache import cache
from django.forms.models import model_to_dict
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
from braces.views import GroupRequiredMixin
from django.views.generic import TemplateView, CreateView
from datetime import date, datetime, timedelta
from django.contrib.auth.decorators import login_required
from usuarios.permissoes import group_required
from django.views.decorators.csrf import csrf_exempt


class InserirItemView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    selected_categoria ='0'
    
    model = Item
    template_name = 'estoque/inserir-item.html'
    success_url = reverse_lazy('inserir-item')
    form_class = InserirItemForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ultimos_dez'] =  Item.objects.all().order_by('-id')
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

class DetalharItemView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    template_name = "estoque/detalhar-item.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)         
        context["item_atual"] = Item.objects.get(pk=self.kwargs.get('pk'))
        return context

class EditarItemView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    template_name = 'estoque/inserir-item.html'
    model = Item
    form_class = InserirItemForm
        
    def get_success_url(self):
        return reverse('ver-estoque')
        # return reverse('detalhar-item', kwargs = {'pk': self.kwargs.get('pk')})

class ExcluirItemView(GroupRequiredMixin, LoginRequiredMixin,DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    model = Item
    success_url = reverse_lazy("inserir-item")
      
class InicioEstoque(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    template_name= 'estoque/ver-estoque.html'
    success_url = reverse_lazy('ver-estoque')
 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # objects = Estoque.objects.select_related('item') 
        
        
        #Ao iniciar o estoque não carrega todos os itens de primeira, somente quando usar o Form de filtragem
        if self.request.GET.get('filterStatus'):
            objects = Estoque.objects.all()
            filter_list = EstoqueFilter(self.request.GET, queryset = objects )
        else:
            objects = Estoque.objects.none()
            filter_list = EstoqueFilter(self.request.GET, queryset = objects )
                   
        
        context["filter"] = filter_list
        cache.set('filter_estoque_resultados', filter_list, 600)  
        
        return context

class VerEstoqueVarios(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    template_name= 'estoque/ver-estoque-varios.html'
    success_url = reverse_lazy('ver-estoque-varios')
 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # objects = Estoque.objects.select_related('item') 
        
        
        #Ao iniciar o estoque não carrega todos os itens de primeira, somente quando usar o Form de filtragem
        if self.request.GET.get('filterStatus'):
            objects = Estoque.objects.all()
            filter_list = EstoqueFilter(self.request.GET, queryset = objects )
        else:
            objects = Estoque.objects.none()
            filter_list = EstoqueFilter(self.request.GET, queryset = objects )
                   
        
        context["filter"] = filter_list
        cache.set('filter_estoque_resultados', filter_list, 600)  
        
        return context



class MovimentacaoEstoqueView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    model = MovimentacaoEstoque
    template_name= 'estoque/mov-estoque.html'
    success_url = reverse_lazy('mov-estoque')
    form_class = MovimentacaoModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['itensEstoque'] =  Estoque.objects.order_by('pk').all()   
        context["log_list"] = LogMovimentacao.objects.all().order_by('-pk')[:20]
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
                        
                        msg = str(estoque.quantidade)+' '+str(estoque.item.unid_medida)+' - '+str(estoque.item.descricao)+' foi ACRESCENTADO ao Estoque - Total no Estoque: '+str(soma)
                        log_item_updated(request = self.request, item = item_atual, qnt = estoque.quantidade, saldo = soma, adicionado= True)
                        

                        messages.add_message(
                            self.request, 
                            messages.SUCCESS,
                            msg
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
                            
                            msg = str(estoque.quantidade)+' '+str(estoque.item.unid_medida)+' - '+str(estoque.item.descricao)+' foi RETIRADO ao Estoque - Total no Estoque: '+str(sobra)

                            log_item_updated(request = self.request, item = item_atual, qnt = estoque.quantidade, saldo = sobra, adicionado= False)
                            messages.add_message(
                                self.request, 
                                messages.WARNING,
                                msg
                            )
                        else:        
                            messages.add_message(
                                self.request, 
                                messages.WARNING,
                                'NÃO HÁ ITENS SUFICIENTES NO ESTOQUE!'
                            )
        
        return response

class CategoriasEstoque(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    model = Categoria
    template_name= 'estoque/categorias-estoque.html'
    success_url = reverse_lazy('categorias-estoque')
    form_class = CategoriaModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] =  Categoria.objects.all().order_by('pk')
        return context

class EditarCategoriaEstoque(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    model = Categoria
    template_name= 'estoque/categorias-estoque.html'
    success_url = reverse_lazy('categorias-estoque')
    form_class = CategoriaModelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] =  Categoria.objects.all().order_by('pk')
        context['editar'] =  True
        return context

class ExcluirCategoriaEstoque(GroupRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    model = Categoria
    success_url = reverse_lazy("categorias-estoque")

class BuscaEstoqueView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    model = Estoque
    template_name = 'estoque/buscar-estoque.html'

    def get_queryset(self): 
        query = self.request.GET.get('q')
        object_list = ''
        if query != None:
            object_list = Estoque.objects.filter(Q(item__descricao__icontains=query))
        return  object_list
    
class ImprimirResultadosEstoqueView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    model = Categoria
    template_name= 'estoque/resultados-impressao.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_list'] = cache.get('filter_estoque_resultados')
        
        return context
    
class ImprimirListaItensView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    group_required = [u'Administrador', u'Estoque', u'Tecnico',]
    
    model = ItensSelecionados
    template_name= 'estoque/lista-itens-impressao.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter_list'] = ItensSelecionados.objects.all()
        
        return context

@group_required('Administrador', 'Estoque','Tecnico')
@login_required(login_url='login/')
@csrf_exempt
def autocompleteitens(request):
    query = request.GET.get('term')
    query_set = Item.objects.filter(descricao__icontains=query) | Item.objects.filter(pk__iexact=query)
    myList=[]
    myList += [x.descricao+' - '+x.unid_medida+' - COD: '+str(x.pk) for x in query_set]
    return JsonResponse(myList,safe=False)    

@group_required('Administrador', 'Estoque','Tecnico')
@login_required(login_url='login/')
@csrf_exempt
def gerar_qrcode(text):  
    code = pyqrcode.create(text)
    code.png(f"simo/media/qrcodes/{text}.png", scale=6,)

    if code != 0:
        print(f"QRCode gerado com sucesso - {text}!")
        return f"qrcodes/{text}.png"
    else:
        print(f"ERRO ao gerar QRCode - {text}!")
        return False
 
@group_required('Administrador', 'Estoque','Tecnico')
@login_required(login_url='login/')
@csrf_exempt 
def estoque_filter(request):
    if request.method == 'POST': 
        objects = Estoque.objects.all()
        
        filter_list = EstoqueFilter(request.POST, queryset = objects)
        lista_itens = list()
      
        
        for item in list(filter_list.qs.values()):
            lista_aux = list()
            obj = Item.objects.get(id=item['item_id'])
            lista_aux.append(item['id'])
            lista_aux.append(obj.id)
            lista_aux.append(obj.descricao)
            if obj.marca:
                lista_aux.append(obj.marca)
            else:
                lista_aux.append('-')
            if obj.categoria:    
                lista_aux.append(obj.categoria.categoria)
            else:
                lista_aux.append('-')
            if obj.fornecedor:
                lista_aux.append(obj.fornecedor.nome)
            else:
                lista_aux.append('-')
            lista_aux.append(obj.unid_medida)
            lista_aux.append(item['quantidade'])
            
            lista_itens.append(lista_aux)            
       
        return JsonResponse({'filter': lista_itens}, status=200)

@group_required('Administrador', 'Estoque','Tecnico')
@login_required(login_url='login/')
@csrf_exempt
def add_filtro_varios(request):
     
    carregar_itens = ItensSelecionados.objects.all()
    
    template_name = 'estoque/lista-itens-selecionados.html'
    if request.method == 'POST':
        tasks = request.POST.getlist('array[]')       
        print(tasks)     
        
        for item in tasks:
            if not carregar_itens.filter(estoque__item__pk=int(item)):
                aux = ItensSelecionados(estoque = Estoque.objects.get(item__pk=int(item)))
                aux.save()
        
        context = {
            'itens_selecionados': carregar_itens.order_by('-pk')
        }
        
        return render(request, template_name, context)
    else:
        return HttpResponse('Item Não Adicionado') #TODO FAZER UMA RESPOSTA EM HTML COM TABELA VAZIA
    
@group_required('Administrador', 'Estoque','Tecnico')
@login_required(login_url='login/')
@csrf_exempt
def remover_filtro_varios(request):
 
    template_name = 'estoque/lista-itens-selecionados.html'
    
    try:
        item_selecionado = ItensSelecionados.objects.get(estoque__item__pk=request.POST.get('id'))
        item_selecionado.delete()
        
        context = {
            'itens_selecionados': ItensSelecionados.objects.all().order_by('-pk')
        }
        return render(request, template_name, context )
        
    except: 
        
      return HttpResponse('Item Não Encontrado ou Já excluído!') #TODO FAZER UMA RESPOSTA EM HTML COM TABELA VAZIA

@group_required('Administrador', 'Estoque','Tecnico')
@login_required(login_url='login/')
@csrf_exempt     
def remover_lista_selecionada(request):
    template_name = 'estoque/lista-itens-selecionados.html'
    
    try:
        ItensSelecionados.objects.all().delete()
        
        return render(request, template_name)
        
    except: 
        
      return HttpResponse('Lista Não encontrada ou já excluída!') #TODO FAZER UMA RESPOSTA EM HTML COM TABELA VAZIA       

@group_required('Administrador', 'Estoque','Tecnico')
@login_required(login_url='login/')
@csrf_exempt  
def log_item_updated(request, item, qnt, saldo, adicionado):

   current_time = datetime.now()
   #formated_data = current_time.strftime("%d/%m/%Y - %H:%M")
   
   usuario = None
   if request.user.is_authenticated:
        usuario = request.user
   
   novo_log = LogMovimentacao(usuario=usuario, item=item, quantidade=qnt, saldo=saldo, adicionado=adicionado, data_inclusao=current_time)
   novo_log.save()

@group_required('Administrador', 'Estoque','Tecnico')
@login_required(login_url='login/')
@csrf_exempt
def estoque_busca_varios(request):
    if request.POST.get("descricao") == "":
        return render(request, template_name='estoque/fragmentos/itens_busca_varios.html', context={'error': 'Campos Vazios'})
    else:
        objects = Estoque.objects.all()
        filter_list = EstoqueFilter(request.POST, queryset = objects )
    
    return render(request, template_name='estoque/fragmentos/itens_busca_varios.html', context={'filter_list': filter_list})

@group_required('Administrador', 'Estoque','Tecnico')
@login_required(login_url='login/')
@csrf_exempt
def limpar_itens_lista(request): 
    return render(request, template_name='estoque/fragmentos/itens_busca_varios.html', context={'filter_list': ''})
