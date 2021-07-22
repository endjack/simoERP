from estoque.models import Categoria
from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Categoria)
admin.site.register(Item)
admin.site.register(MovimentacaoEstoque)
admin.site.register(Estoque)

