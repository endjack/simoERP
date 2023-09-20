from django.urls import path
from funcionarios.views import *


urlpatterns = [
    path('procurar/', procurar_pessoal, name='procurar_pessoal'),
    path('novo/funcionario/', cadastrar_funcionarios_pessoal, name='cadastrar_funcionarios_pessoal'),
    path('novo/cargo/', cadastrar_cargo_pessoal, name='cadastrar_cargo_pessoal'),
    path('impressoes/', impressoes_pessoal, name='impressoes_pessoal'),
    path('relatorios/', relatorios_pessoal, name='relatorios_pessoal'),
    
]