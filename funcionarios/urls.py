from django.urls import path
from funcionarios.views import *


urlpatterns = [
    path('procurar/', procurar_pessoal, name='procurar_pessoal'),
    path('funcionario/novo', cadastrar_funcionarios_pessoal, name='cadastrar_funcionarios_pessoal'),
    path('funcionario/<int:pk>/editar', cadastrar_funcionarios_pessoal, name='editar_funcionarios_pessoal'),
    path('funcionario/<int:pk>/excluir', excluir_funcionarios_pessoal, name='excluir_funcionarios_pessoal'),
    path('funcionario/<int:pk>/dependente/<int:pkDep>/excluir', excluir_dependente, name='excluir_dependente'),
    path('funcionario/<int:pk>/salvar', add_funcionario_v2, name='add_funcionario_v2'),
    path('funcionario/salvar', add_funcionario_v2, name='add_funcionario_v2'),
    path('funcionario/<int:pk>/detalhar', detalhar_funcionario_v2, name='detalhar_funcionario_v2'),
    path('funcionario/buscar', filtrar_funcionariosV2, name='filtrar_funcionariosV2'),
    path('local_de_trabalho/', local_trabalho_pessoal, name='local_trabalho_pessoal'),
    path('local_de_trabalho/associar', associar_funcionario_local, name='associar_funcionario_local'),
    path('local_de_trabalho/imprimir', imprimir_locais_funcionarios, name='imprimir_locais_funcionarios'),
    path('novo/cargo/', cadastrar_cargo_pessoal, name='cadastrar_cargo_pessoal'),
    path('impressoes/', impressoes_pessoal, name='impressoes_pessoal'),
    path('relatorios/', relatorios_pessoal, name='relatorios_pessoal'),
    
    
    
    path('htmx/add_inputs_dependente/<int:id>/', add_inputs_dependente, name='add_inputs_dependente'),
    path('htmx/clear_element/', clear_element, name='clear_element'),
    
] 