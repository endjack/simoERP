from django.urls import path
from funcionarios.views import *


urlpatterns = [
    path('procurar/', procurar_pessoal, name='procurar_pessoal'),
    path('novo/funcionario/', cadastrar_funcionarios_pessoal, name='cadastrar_funcionarios_pessoal'),
    path('novo/funcionario/add', add_funcionario_v2, name='add_funcionario_v2'),
    path('novo/cargo/', cadastrar_cargo_pessoal, name='cadastrar_cargo_pessoal'),
    path('impressoes/', impressoes_pessoal, name='impressoes_pessoal'),
    path('relatorios/', relatorios_pessoal, name='relatorios_pessoal'),
    
    
    
    path('htmx/add_inputs_dependente/<int:id>/', add_inputs_dependente, name='add_inputs_dependente'),
    path('htmx/clear_element/', clear_element, name='clear_element'),
    
]