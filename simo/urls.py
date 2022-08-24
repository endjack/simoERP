from simo.utils import limpar_cache
from tarefas.views import *
import debug_toolbar
from recibos.views import *
from simo.settings import STATIC_URL
from funcionarios.views import *
from estoque.views import *
from requisicao.views import *
from financeiro.views import *
from servicos.views import *
from dashboard.views import *
from obras.views import *
from faturamento.views import *
from fornecedores.views import *
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from financeiro.ajax import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    
    #url DashBoard
    path('', TarefasView.as_view(), name='dashboard'),
    path('tarefa/excluir/<pk>', DeleteTarefaView.as_view(), name='excluir-tarefa'),
    path('tarefa/editar/<pk>', EditarTarefaView.as_view(), name='editar-tarefa'),
   
    #urls Estoque
    path('ver-estoque', InicioEstoque.as_view(), name='ver-estoque'),
    path('ver-estoque/varios', VerEstoqueVarios.as_view(), name='ver-estoque-varios'),
    path('add-varios/', add_filtro_varios, name='add-varios'),
    path('remover-item-selecionado/', remover_filtro_varios, name='remover-item-selecionado'),
    path('remover-lista-selecionada/', remover_lista_selecionada, name='remover-lista-selecionada'),
    path('mov-estoque/', MovimentacaoEstoqueView.as_view(), name='mov-estoque'),
    path('buscar-estoque/', BuscaEstoqueView.as_view(), name='buscar-estoque'),
    path('categorias-estoque/', CategoriasEstoque.as_view(), name='categorias-estoque'),
    path('categorias-estoque/editar/<pk>', EditarCategoriaEstoque.as_view(), name='editar-categoria'),
    path('categorias-estoque/excluir/<pk>', ExcluirCategoriaEstoque.as_view(), name='excluir-categoria'),
    path('inserir-item/', InserirItemView.as_view(), name='inserir-item'),
    path('excluir-item/<pk>', ExcluirItemView.as_view(), name='excluir-item'),
    path('detalhar-item/<pk>', DetalharItemView.as_view(), name='detalhar-item'),
    path('editar-item/<pk>', EditarItemView.as_view(), name='editar-item'),
    path('imprimir-resultados', ImprimirResultadosEstoqueView.as_view(), name='imprimir-resultados'),
    path('imprimir-lista-itens', ImprimirListaItensView.as_view(), name='imprimir-lista-itens'),
    path('filtrar-estoque', estoque_filter, name='estoque-filter'),
    
    #urls Requisição
    path('gerar-requisicao/', GerarRequisicaoView.as_view(), name='gerar-requisicao'),
#     path('gerar-requisicao/add-funcionario', add_funcionario_requisicao, name='add-funcionario-requisicao'),
#     path('gerar-requisicao/remove-funcionario', remove_funcionario_requisicao, name='remove-funcionario-requisicao'),
#     path('gerar-requisicao/add-obra-local', add_obra_local_requisicao, name='add-obra-local-requisicao'),
 

    #urls Obras
    path('inserir-obra/', InserirObraView.as_view(), name='inserir-obra'),
    path('ver-obras/', BuscarObraListView.as_view(), name='ver-obras'),
    path('inserir-local/', InserirLocalView.as_view(), name='inserir-local'),

    #urls Serviços
    path('os/', OrdemServicoCreateView.as_view(), name='inserir-ordem'),
    path('os/<pk>/excluir-ordem', ExcluirOrdemDeServicoView.as_view(), name='excluir-ordem'),
    path('os/<pk>/inserir-servico', ServicoCreateView.as_view(), name='inserir-servico'),
    path('os/<id_ordem>/<pk>/editar-servico', EditarServicoView.as_view(), name='editar-servico'), #VIEWS GENERICAS COMO UPDATEVIEW reservam o 'pk' para a id do objeto
    path('os/<id_ordem>/<pk>/excluir-servico', ExcluirServicoView.as_view(), name='excluir-servico'),
    path('os/<id_ordem>/<pk>/detalhar-servico', DetalharServicoView.as_view(), name='detalhar-servico'),
    path('os/<id_ordem>/<pk>/finalizar-servico', FinalizarServicoView.as_view(), name='finalizar-servico'),
    path('os/<id_ordem>/<pk>/imprimir-servico', ImprimirServicoView.as_view(), name='imprimir-os-servico'),
    path('os/<id_ordem>/<pk>/inserir-funcionario', InserirFuncionarioServicoView.as_view(), { 'editar': False }, name='inserir-funcionario-servico'),
    path('os/<id_ordem>/<pk>/editar-funcionario', InserirFuncionarioServicoView.as_view(), { 'editar': True }, name='editar-funcionario-servico'),
    path('os/<id_ordem>/<pk>/inserir-itens', ItensServicoCreateView.as_view(), name='inserir-itens-servico'),
    path('salvar-ordem-servico/os/<pk>', SalvarServicoView.as_view(), name='salvar-ordem-servico'),
    path('listar-servicos/', ListServicosView.as_view(), name='listar-servicos'),
    path('listar-servicos-funcionario/', ListFuncionarioServicosView.as_view(), name='listar-servicos-funcionario'),
    path('listar-ordens/', ListOrdensView.as_view(), name='listar-ordens'),
    path('anexar-imagens-servicos/os/<pk>/servico/<int:idServ>', AnexarImagensServicoView.as_view(), name='anexar-imagens-servicos'),
    path('deletar-imagem/os/<id_ordem>/servico/<idServ>/deletar-imagem/<pk>', DeletarImagemServicoView.as_view(), name='deletar-imagem'),
    path('imprimir-servicos/', ImprimirListaServicosView.as_view(), name='imprimir-servicos'),
    path('imprimir-servicos-funcionario/', ImprimirListaFuncionarioServicosView.as_view(), name='imprimir-servicos-funcionario'),

    #auto-completes
    path('autocomplete-funcionarios/', autocompletefuncionario, name='autocomplete-funcionarios'),
#    path('gerar-requisicao/busca_funcionarios', autocomplete_funcionarios, name='autocomplete-funcionarios-requisicao'),
    path('autocomplete-itens/', autocompleteitens, name='autocomplete-itens'),
    
    #urls Usuários 
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    #urls Financeiro 
    path('contas-a-pagar/', ContasAPagarView.as_view(), name='contas-a-pagar'),
    path('contas-a-pagar/inserir', InserirContasAPagarView.as_view(), name='inserir-conta-a-pagar'),
    path('contas-a-pagar/editar/<pk>', EditarContasAPagarView.as_view(), name='editar-conta-a-pagar'),
    path('contas-a-pagar/excluir/<pk>', ExcluirContasAPagarView.as_view(), name='excluir-conta-a-pagar'),
    path('pagamento/<pk>', PagamentoView.as_view(), name='pagar-conta'),
    path('pagamento/editar/<pk>', EditarPagamentoView.as_view(), name='editar-pagamento'),
    path('pagamento/excluir/<pk>', ExcluirPagamentoView.as_view(), name='excluir-pagamento'),
    path('relatorios/financeiro/contas-a-pagar', RelatoriosCostasAPagarView.as_view(), name='relatorios-contas-a-pagar'),
    path('relatorio-contas/imprimir', ImprimirRelatoriosCostasAPagarView.as_view(), name='imprimir-relatorio-contas'),
    path('contas-a-receber/', ContasAReceberView.as_view(), name='contas-a-receber'),
    path('contas-a-receber/editar/<pk>', EditarRecebimentoView.as_view(), name='editar-conta-a-receber'),
    path('contas-a-receber/excluir/<pk>', ExcluirRecebimentoView.as_view(), name='excluir-conta-a-receber'),
    path('recibos/', InserirReciboFornecedorView.as_view(), name='inserir-recibo'),
    path('recibos/editar/<pk>', EditarReciboFornecedorView.as_view(), name='editar-recibo'),
    path('recibos/excluir/<pk>', ExcluirReciboFornecedorView.as_view(), name='excluir-recibo'),
    path('recibos/imprimir/<pk>',ImprimirReciboFornecedorView.as_view(), name='imprimir-recibo'),
    path('contas-pagas/', ContasPagasView.as_view(), name='contas-pagas'),
    path('ajax/fornecedor/contas-a-pagar', getContasAPagar, name = "ajax-fornecedor-contas-a-pagar"),

    
    #urls Fornecedores
     path('fornecedores/', ListarFornecedorView.as_view(), name='listar-fornecedores'),
     path('fornecedor/<pk>', DetalharFornecedorView.as_view(), name='detalhar-fornecedor'),
     path('fornecedores/inserir', InserirFornecedorView.as_view(), name='inserir-fornecedor'),
     path('fornecedores/<pk>/editar', EditarFornecedorView.as_view(), name='editar-fornecedor'),
     path('fornecedores/<pk>/excluir', ExcluirFornecedorView.as_view(), name='excluir-fornecedor'),

     #urls Funcionários
     path('funcionarios/', InserirFuncionarioView.as_view(), name='inserir-funcionario'),
     path('funcionarios/<pk>/editar', EditarFuncionarioView.as_view(), name='editar-funcionario'),
     path('funcionarios/<pk>/excluir', ExcluirFuncionarioView.as_view(), name='excluir-funcionario'),
     path('funcionario/<pk>', DetalharFuncionarioView.as_view(), name='detalhar-funcionario'),
     path('cargos/', InserirCargoView.as_view(), name='inserir-cargo'),
     path('cargos/<pk>/editar', EditarCargoView.as_view(), name='editar-cargo'),
     path('cargos/<pk>/excluir', ExcluirCargoView.as_view(), name='excluir-cargo'),
     path('cargo/<pk>', DetalharCargoView.as_view(), name='detalhar-cargo'),

      #urls Faturamento
     path('faturamentos/', FaturamentoView.as_view(), name='listar-faturamentos'),
     path('faturamentos/inserir', InserirFaturamentoView.as_view(), name='inserir-faturamento'),
     path('faturamentos/editar/<pk>', EditarFaturamentoView.as_view(), name='editar-faturamento'),
     path('faturamentos/excluir/<pk>', ExcluirFaturamentoView.as_view(), name='excluir-faturamento'),
     path('faturamentos/imprimir', ImprimirFaturamentoView.as_view(), name='imprimir-faturamento'),
]

htmlx_urlpatterns = [              
    path('requisicao/requerente', requisicao_search_funcionario, name='requisicao-search-funcionario'),                 
    path('requisicao/add-requerente/<pk>', requisicao_add_funcionario, name='requisicao-add-funcionario'),                 
    path('requisicao/add-obra', requisicao_add_obra, name='requisicao-add-obra'),                 
    path('requisicao/add-local', requisicao_add_local, name='requisicao-add-local'),                 
    path('requisicao/add-itens-selecionados/<pk>', requisicao_add_itens_selecionados, name='requisicao-add-itens-selecionados'),                 
    path('requisicao/excluir-itens-selecionados/<pk>', requisicao_excluir_item_lista_selecionada, name='excluir-item-lista-selecionada'),                 
    path('requisicao/verificar-qnt/<pk>', requisicao_verificar_qnt, name='requisicao-verificar-qnt'),                 
    path('estoque/busca-varios', estoque_busca_varios, name='buscar-estoque-varios'),
    
    #utils
    path('hx/limpar', limpar_cache, name='limpar-cache'),                

]

urlpatterns += htmlx_urlpatterns


if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)