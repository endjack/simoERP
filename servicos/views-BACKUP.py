from django.contrib import messages
from servicos.models import Servico
from django.shortcuts import render
from .forms import *
from decimal import Decimal
from django.views.generic import TemplateView

# Create your views here.

ordemAtual = None
servicoAtual = None
itensAtuais = []
funcionariosAtuais = []
listaitensAtuais = []


class InserirOrdemView(TemplateView):
    template_name = 'servicos/inserir-ordem.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form_s = OrdemServicoForm(self.request.POST or None)              
        context["form"] = form_s
        return context 

class InserirServicoView(TemplateView):
    template_name = 'servicos/inserir-servico.html'
    

    def post(self, request):
        global ordemAtual
        form_s = ServicoForm(self.request.POST or None)
             
        id_encarregado = request.POST.get('encarregado')
        id_obra = request.POST.get('obra')
        id_local = request.POST.get('local')
        data =  request.POST.get('data')

        ordemAtual = OrdemServico(encarregado = Funcionario.objects.get(pk=id_encarregado),
                                 obra = Obra.objects.get(pk=id_obra),
                                 local = Local.objects.get(pk=id_local),
                                 data = str(data), 
                                )                 
        context = {
            "ordem_serv_atual": ordemAtual,
            "form": form_s
        }
        print("---------------------->>> ORDEM - "+str(ordemAtual.data))

        return render(request, 'servicos/inserir-servico.html', context)
    
class InserirFuncionarioServicoView(TemplateView):
    template_name = 'servicos/inserir-funcionario.html'
      
    def post(self, request):
        global ordemAtual
        global funcionariosAtuais 
        global servicoAtual
    
        # recebendo os dados de Serviço e colocando na pagina
        servicoAtual = Servico( descricao= request.POST.get('descricao'), 
                                prazo= request.POST.get('prazo'),
                                situacao=request.POST.get('situacao'),
                                obs=request.POST.get('obs')
                                )

        context = {}
        func_atual = ""
        funcionario_matricula = request.POST.get('matricula')

        if funcionario_matricula != None and funcionario_matricula != "":
            try:
                funcionario_matricula = funcionario_matricula.split('COD: ')[1] #fatia a string, deixando apenas a matricula
                func_atual = Funcionario.objects.get(matricula=funcionario_matricula) 
            except IndexError:
                messages.add_message(
                                    self.request, 
                                    messages.WARNING,
                                    'Funcionário Não Encontrado ou Não Válido!'
                                    )  
                func_atual = None 

        if func_atual !=None and func_atual != "":
            if func_atual not in funcionariosAtuais:
                funcionariosAtuais.append(func_atual)
                context['funcionarios_atuais'] = funcionariosAtuais
                messages.add_message(
                                        self.request, 
                                        messages.SUCCESS,
                                        'Funcionário '+ func_atual.nome +' adicionado com Sucesso!'
                                        )   
            else:
                messages.add_message(
                                    self.request, 
                                    messages.WARNING,
                                    'Funcionário já adicionado!'
                                    )
        context['funcionarios_atuais'] = funcionariosAtuais    
        context['serv_atual'] = servicoAtual
        context['ordem_serv_atual'] = ordemAtual
        
     
        return render(request, 'servicos/inserir-funcionario.html', context)

class InserirItensServicoView(TemplateView):
    template_name = 'servicos/inserir-itens-servico.html'

    def post(self, request):
        global ordemAtual
        global servicoAtual 
        global funcionariosAtuais 
        global itensAtuais

        
        item_post = request.POST.get('item_selecionado')
        quantidade_post = request.POST.get('quantidade')
        
        context = {}
        item_id = ''
                
        if quantidade_post != None and quantidade_post != "":
            quantidade_atual = quantidade_post

        if item_post != None and item_post != "":
            try:
                item_id = item_post.split('COD: ')[1] #fatia a string, deixando apenas a matricula
                item_atual = ItensServico(item = Item.objects.get(pk=item_id),
                                          qnt = quantidade_atual)
            except:
                messages.add_message(
                                    self.request, 
                                    messages.WARNING,
                                    'Material Não Encontrado ou Não Válido!'
                                    )  
                item_atual = None 
            
                
            if item_atual !=None and item_atual != "":
                if item_atual not in itensAtuais:
                    itensAtuais.append(item_atual)

                    context['itens_atuais'] = itensAtuais
                    messages.add_message(
                                    self.request, 
                                    messages.SUCCESS,
                                    str(item_atual.qnt) + ' ' + str(item_atual.item.unid_medida)+ ' ' + str(item_atual.item.descricao) +' adicionado com Sucesso!'
                                    ) 

                else:
                    messages.add_message(
                                        self.request, 
                                        messages.WARNING,
                                        'Material já adicionado!'
                                        )         
        
        context['itens_atuais'] = itensAtuais
        context['ordem_serv_atual'] = ordemAtual
        context['serv_atual'] = servicoAtual
        context['funcionarios_atuais'] = funcionariosAtuais
          
        return render(request, 'servicos/inserir-itens-servico.html', context)

class SalvarServicoView(TemplateView):
    template_name = "servicos/salvar-servico.html"
    
    def post(self, request):
        global ordemAtual
        global servicoAtual 
        global funcionariosAtuais 
        global itensAtuais
        context = {}
        
        # SALVANDO SERVICO NO BANCO   
        servico_salvo = Servico.objects.create(
                               descricao = servicoAtual.descricao,
                               prazo = servicoAtual.prazo,
                               situacao = servicoAtual.situacao,
                               obs = servicoAtual.obs,
                               ) 
        
        servico_salvo.funcionarios.set(funcionariosAtuais)
        
        # SALVANDO ITENS NO BANCO  
        for item in itensAtuais:
            iten_salvo = ItensServico.objects.create(
                                        item = item.item,
                                        qnt = Decimal((item.qnt).replace(',', '.')) 
                                        )                                   
            servico_salvo.itens.add(iten_salvo) 
          
        # SALVANDO ORDEM NO BANCO 
        ordem_salva = OrdemServico.objects.create(
                            encarregado = ordemAtual.encarregado,
                            obra = ordemAtual.obra,
                            local = ordemAtual.local,
                            data = toDBFormat(ordemAtual.data),
                            )                       
        
        ordem_salva.servicos.add(servico_salvo)  
                           
        
        context['ordem_salva'] = ordem_salva 
        
        #resetando os objetos
        ordemAtual = None
        servicoAtual = None
        funcionariosAtuais = []
        itensAtuais = []

        return render(request, 'servicos/salvar-servico.html', context)
    
def toDBFormat(dateString):
    dataBD = dateString.split('/')
    return str(dataBD[2])+'-'+str(dataBD[1])+'-'+str(dataBD[0])
    

