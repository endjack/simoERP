from django.contrib import admin

from estoque_v2.models import *

# Register your models here.
admin.site.register(CategoriaFerramenta)
admin.site.register(Ferramenta)
admin.site.register(Cautela)
admin.site.register(CautelaFerramenta)